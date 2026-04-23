from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel, Field
from typing import Optional, List
import os
from datetime import datetime

app = FastAPI()

# Autoriser le frontend à parler avec l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connexion à MongoDB
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = MongoClient(MONGO_URL)

db = client["user_profiles_db"]
users = db["users"]


# ───────────── MODELES ─────────────

class Address(BaseModel):
    street: str
    city: str
    country: str = "France"
    zip_code: str


class Preferences(BaseModel):
    theme: str = "light"
    notifications: bool = True
    language: str = "fr"


class User(BaseModel):
    name: str = Field(..., min_length=2)
    email: str
    addresses: List[Address] = []
    preferences: Preferences = Preferences()


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    addresses: Optional[List[Address]] = None
    preferences: Optional[Preferences] = None


# ───────────── OUTILS ─────────────

def format_user(user):
    user["id"] = str(user.pop("_id"))
    return user


def find_user(user_id):
    try:
        oid = ObjectId(user_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="id invalide")

    user = users.find_one({"_id": oid})

    if not user:
        raise HTTPException(status_code=404, detail="user introuvable")

    return user


# ───────────── ROUTES ─────────────

@app.get("/")
def home():
    return {"msg": "API users OK"}


# créer user
@app.post("/users")
def create_user(user: User):
    if users.find_one({"email": user.email}):
        raise HTTPException(status_code=409, detail="email déjà utilisé")

    data = user.model_dump()
    data["created_at"] = datetime.utcnow().isoformat()
    data["premium"] = False

    result = users.insert_one(data)
    data["_id"] = result.inserted_id

    return format_user(data)


# tous les users
@app.get("/users")
def get_users():
    data = users.find()
    return [format_user(u) for u in data]


# un user
@app.get("/users/{user_id}")
def get_one_user(user_id: str):
    user = find_user(user_id)
    return format_user(user)


# update user
@app.put("/users/{user_id}")
def update_user(user_id: str, updates: UserUpdate):
    find_user(user_id)

    data = {k: v for k, v in updates.model_dump().items() if v is not None}

    if not data:
        raise HTTPException(status_code=400, detail="rien à modifier")

    users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": data}
    )

    return format_user(users.find_one({"_id": ObjectId(user_id)}))


# delete user
@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    find_user(user_id)
    users.delete_one({"_id": ObjectId(user_id)})
    return {"msg": "user supprimé"}


# ───────────── REQUÊTE AVANCÉE 1 ─────────────
# users avec notif + plusieurs adresses
@app.get("/users/filter")
def filter_users():
    data = users.find({
        "preferences.notifications": True,
        "addresses.1": {"$exists": True}
    })

    return [format_user(u) for u in data]


# ───────────── REQUÊTE AVANCÉE 2 ─────────────
# tri sans email
@app.get("/users/sorted")
def sorted_users():
    data = users.find({}, {"email": 0}).sort("name", 1)
    return [format_user(u) for u in data]


# ───────────── REQUÊTE AVANCÉE 3 ─────────────
# mettre premium aux users avec 2+ adresses
@app.post("/users/premium")
def give_premium():
    result = users.update_many(
        {"addresses.1": {"$exists": True}},
        {"$set": {"premium": True}}
    )

    return {
        "updated": result.modified_count,
        "msg": "premium ajouté"
    }