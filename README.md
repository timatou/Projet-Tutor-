# Système de Gestion Pédagogique

Application web de gestion d'établissement scolaire développée avec Django. Elle permet de gérer les étudiants, les modules, les notes, les absences et de visualiser des statistiques académiques.

---

## Fonctionnalités

- **Gestion des utilisateurs** : trois rôles distincts (Administrateur, Professeur, Étudiant)
- **Gestion des étudiants** : ajout, suppression, organisation par promotion et groupe
- **Gestion des modules** : création et assignation aux professeurs et promotions
- **Gestion des notes** : saisie individuelle ou en masse par les professeurs
- **Gestion des absences** : signalement, validation et suivi des justificatifs
- **Statistiques** : moyennes, distribution, médiane, écart-type, taux de réussite avec filtres
- **Tableau de bord** : KPIs, alertes étudiants à risque, évolution mensuelle des absences

---

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| Backend | Django 6.0.3 |
| Base de données | SQLite3 |
| Frontend | HTML/CSS/JavaScript (Fetch API) |
| Graphiques | Chart.js |
| Icônes | Font Awesome 6.5 |
| CORS | django-cors-headers |

---

## Installation

### Prérequis

- Python 3.12+
- pip

### Étapes

```bash
# Cloner le dépôt
git clone https://github.com/timatou/Projet-Tutor-.git
cd Projet-Tutor-

# Créer et activer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver
```

L'application est accessible sur [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Variables d'environnement

| Variable | Description | Valeur par défaut |
|----------|-------------|-------------------|
| `DJANGO_SECRET_KEY` | Clé secrète Django | valeur de développement |
| `DJANGO_DEBUG` | Mode debug | `true` |
| `DJANGO_ALLOWED_HOSTS` | Hôtes autorisés (séparés par virgule) | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | Origines CORS autorisées | `http://localhost:8000,http://127.0.0.1:8000` |

---

## Structure du projet

```
Projet-Tutor-/
├── application/        # Configuration principale (settings, urls)
├── utilisateurs/       # Gestion des comptes et rôles
├── etudiants/          # Promotions, groupes, étudiants
├── cours/              # Modules et matières
├── evaluation/         # Notes, épreuves, absences
├── statistique/        # API statistiques avec filtres
├── dashboard/          # Tableau de bord et KPIs
├── templates/          # Templates HTML partagés (base.html)
├── static/             # CSS et JS globaux
└── requirements.txt    # Dépendances Python
```

---

## Rôles et accès

| Rôle | Accès |
|------|-------|
| **Administrateur** | Accès complet : gestion des utilisateurs, modules, étudiants, notes, absences, statistiques |
| **Professeur** | Saisie des notes et appels pour ses modules assignés |
| **Étudiant** | Accès en lecture seule (non implémenté côté interface) |

---

## Interface d'administration Django

Accessible sur `/admin/` avec un compte superutilisateur. Permet la gestion complète de toutes les entités.

---

## Équipe

Projet tutoré — L3 Informatique

| Membre |
|--------|
| Abdallah Aboulkhassim |
| Fatimatou Barry |
| Annie Claudia Gacuti |
| Kady |
