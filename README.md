1. Introduction

Dans ce projet, nous avons développé une API REST complète permettant la gestion d’utilisateurs avec FastAPI et MongoDB.

L’objectif est de créer une application backend capable de :
- gérer des utilisateurs (CRUD)
- stocker les données dans une base NoSQL (MongoDB)
- fournir des fonctionnalités avancées (filtrage, tri, mise à jour conditionnelle)


2. Technologies utilisées

- Python
- FastAPI
- MongoDB
- PyMongo
- Pydantic
- Uvicorn
- HTML (frontend simple optionnel)


3. Modélisation de la base de données

Base de données : user_profiles_db  
Collection : users  

Structure d’un document utilisateur :
{
  "name": "string",
  "email": "string",
  "addresses": [
    {
      "street": "string",
      "city": "string",
      "zip_code": "string",
      "country": "string"
    }
  ],
  "preferences": {
    "theme": "string",
    "notifications": true,
    "language": "string"
  },
  "created_at": "datetime",
  "premium": false
}

Screenshot 1 – Modélisation MongoDB / Schéma  
[INSÉRER ICI IMAGE DU SCHÉMA]


4. Architecture de l’API

Endpoints principaux :
- POST /users → créer un utilisateur
- GET /users → récupérer tous les utilisateurs
- GET /users/{id} → récupérer un utilisateur
- PUT /users/{id} → modifier un utilisateur
- DELETE /users/{id} → supprimer un utilisateur

Endpoints avancés :
- GET /users/filter → filtrage avancé
- GET /users/sorted → tri des utilisateurs
- POST /users/premium → mise à jour conditionnelle


5. Tests de l’API

Tous les tests ont été effectués via Swagger UI.

- POST /users (création)

- GET /users (récupération)


- PUT /users/{id} (mise à jour)

- DELETE /users/{id} (suppression)

- GET /users/filter (filtrage)

- GET /users/sorted (tri)

- POST /users/premium (premium)




6. Gestion des erreurs

- 400 → ID invalide
- 404 → utilisateur introuvable
- 409 → email déjà utilisé
- 422 → erreur de validation


7. Fonctionnalités avancées

- filtrage sur les notifications et adresses
- tri alphabétique des utilisateurs
- mise à jour conditionnelle (premium)


8. Frontend 

Interface simple pour tester l’API via HTTP.




9. Résultat final

- gestion complète des utilisateurs
- stockage NoSQL flexible
- API REST fonctionnelle
- requêtes avancées MongoDB


10. Conclusion

Ce projet a permis de comprendre :
- FastAPI et création d’API REST
- MongoDB et structure NoSQL
- CRUD et requêtes avancées


Améliorations possibles

- authentification JWT
- pagination
- frontend amélioré
- déploiement cloud (AWS )


