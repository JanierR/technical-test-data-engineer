# Réponses du test

## Utilisation de la solution (étape 1 à 3)

### Étape 1: Création de l'environnement virtuel
1. Créez un environnement virtuel avec l’outil de votre choix (par exemple, `venv`).
   ```bash
   python -m venv venv
   ```
2. Activez l’environnement virtuel :
   - Sous Windows :
     ```bash
     venv\Scripts\activate
     ```   
3. Installez les librairies listées dans `requirements.txt` :
   ```bash
   pip install -r requirements.txt
   ```

### Étape 2: Mise en place du flux de données
1. Lancer le serveur FastAPI :
   ```bash
   cd src/moovitamix_fastapi
   python -m uvicorn main:app
   ```
2. Créez un script Python pour le pipeline de données (voir le fichier `data_pipeline.py` fourni).
3. Le pipeline récupère les données des API et les sauvegarde au format CSV. Configurez la planification quotidienne avec `APScheduler`.

### Étape 3: Tests unitaires
1. Les tests unitaires sont localisés dans le fichier `test_data_pipeline.py`
2. Pour exécuter les tests, utilisez la commande suivante :
   ```bash
   pytest test_data_pipeline.py
   ```

## Questions (étapes 4 à 7)

### Étape 4: Schéma de la base de données et recommandations

#### Schéma de la base de données
La base de données contient trois tables principales :

1. **users** :
   - `id` (PK): Identifiant unique de l'utilisateur
   - `name`: Nom de l'utilisateur
   - `email`: Adresse email
   - `created_at`: Date de création du compte

2. **songs** :
   - `id` (PK): Identifiant unique de la chanson
   - `title`: Titre de la chanson
   - `artist`: Artiste
   - `genre`: Genre
   - `duration`: Durée (en secondes)
   - `release_date`: Date de sortie

3. **listening_history** :
   - `id` (PK): Identifiant unique
   - `user_id` (FK): Référence à `users.id`
   - `song_id` (FK): Référence à `songs.id`
   - `timestamp`: Date et heure d'écoute

#### Recommandation de la base de données
Je recommande l’utilisation de PostgreSQL pour sa robustesse, sa gestion avancée des relations et ses fonctionnalités étendues (comme les types JSON et l’indexation efficace).

### Étape 5: Surveillance du pipeline de données

#### Métriques clés
1. Temps d’exécution de chaque étape.
2. Nombre d’enregistrements traités.
3. Erreurs d'extraction ou de transformation.

#### Mise en place de la surveillance
- Utilisez Prometheus pour collecter les métriques du pipeline (exportées via un endpoint).
- Configurez Grafana pour une visualisation en temps réel des performances.
- Configurez des alertes via Slack ou Email en cas d'échec.

### Étape 6: Automatisation des recommandations

#### Architecture de recommandations
1. **Filtrage collaboratif** :
   - Utilisez une matrice utilisateur-chanson basée sur les écoutes passées.
   - Implémentez des algorithmes comme `KNN` ou `ALS` pour recommander des chansons écoutées par des utilisateurs similaires.

2. **Contenu basé sur les caractéristiques** :
   - Analysez les attributs des chansons (genre, artiste, etc.).
   - Utilisez des méthodes comme TF-IDF ou l’encodage de caractéristiques.

3. Automatisation :
   - Configurez un pipeline pour générer des recommandations quotidiennement.
   - Enregistrez les résultats dans une table de recommandations.

### Étape 7: Automatisation du réentrainement

#### Pipeline de réentrainement
1. **Extraction des nouvelles données** :
   - Collectez les écoutes récentes depuis la base de données.
2. **Mise à jour des données d’entraînement** :
   - Combinez les nouvelles données avec l’ancien ensemble.
3. **Réentrainement** :
   - Réexécutez l'entraînement avec les données mises à jour.
4. **Déploiement automatique** :
   - Utilisez des outils comme MLflow ou Docker pour déployer le modèle mis à jour.


