# Sydel CRM — Module Odoo v19

Module CRM sur mesure pour le cabinet Sydel, développé pour Odoo.sh v19.

## Prérequis

- Un projet Odoo.sh actif connecté à un dépôt GitHub
- Odoo v19 (Enterprise ou Community)
- Modules dépendants : `crm`, `contacts`, `mail` (installés automatiquement)

## Déploiement sur Odoo.sh

### Première installation

```bash
# 1. Cloner le dépôt de votre projet Odoo.sh
git clone git@github.com:votre-org/votre-repo.git
cd votre-repo

# 2. Créer une branche de développement
git checkout -b sydel-crm-dev

# 3. Copier le dossier sydel_crm/ à la racine du dépôt
#    (le dossier doit être au même niveau que les autres addons)
cp -r /chemin/vers/sydel_crm .

# 4. Committer et pusher
git add sydel_crm/
git commit -m "[ADD] sydel_crm: module CRM complet pour le cabinet Sydel"
git push -u origin sydel-crm-dev

# 5. Dans l'interface Odoo.sh :
#    - Attendre que le build se termine
#    - Cliquer sur "Connect" pour accéder à la base de développement
#    - Aller dans Apps → Rechercher "Sydel" → Installer
```

### Mise à jour du module

```bash
# 1. Faire les modifications dans le code
# 2. Incrémenter la version dans __manifest__.py
#    Exemple : '19.0.1.0.0' → '19.0.1.0.1' (patch)
# 3. Committer et pusher
git add -A
git commit -m "[IMP] sydel_crm: description du changement"
git push

# Odoo.sh détecte le changement de version et met à jour le module automatiquement
```

### Passage en production

```bash
# 1. Tester en staging d'abord (drag & drop dans l'interface Odoo.sh)
# 2. Vérifier que tout fonctionne avec les données de production
# 3. Merger dans la branche de production
git checkout production
git merge sydel-crm-dev
git push
```

## Structure du module

```
sydel_crm/
├── models/          7 fichiers Python (modèles + logique métier)
├── views/           8 fichiers XML (formulaires, listes, menus)
├── security/        2 fichiers (groupes + droits CRUD)
├── data/            3 fichiers XML (stages pipeline, tags, types relations)
├── tests/           5 fichiers (24 tests unitaires)
├── i18n/            1 fichier (traduction française)
├── static/          2 fichiers (icône + description)
├── doc/             1 fichier (changelog)
└── racine           4 fichiers (__init__, manifest, gitignore, README)
```

## Fonctionnalités

- Contacts personnes physiques : état civil, RPPS, filiation, revenus
- Contacts personnes morales : forme juridique, SIREN/SIRET/NAF, capital social
- Répartition du capital avec calcul automatique des montants
- Dirigeants de société avec fonction et dates de mandat
- Relations professionnelles avec création automatique du miroir
- Documents classés par catégorie avec recherche et tri
- Pipeline CRM en 6 étapes (appel découverte → lettre de mission)
- Attribution multi-utilisateurs et filtre "Mes contacts"
- Tags et source d'acquisition pour la segmentation

## Licence

LGPL-3
