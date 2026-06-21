# Aide-mémoire — Shell et environnement Python

Les commandes système et Python qui n'appartiennent ni à Git ni à Docker.

---

## Fichiers et dossiers

| Intention | Commande | Note |
|---|---|---|
| Créer un dossier | `mkdir nom` | `-p` crée aussi les dossiers parents manquants |
| Créer un fichier vide | `touch nom` | sert par exemple à créer `__init__.py` |
| Afficher le contenu d'un fichier | `cat fichier` | |
| Afficher le début d'un fichier | `head -c 500 fichier` | les 500 premiers caractères |
| Exécuter un script dans le shell courant | `source script` | les effets persistent dans le shell, d'où son usage pour activer un venv |

---

## Environnement virtuel Python

| Intention | Commande |
|---|---|
| Créer un environnement virtuel | `python3 -m venv .venv` |
| Activer l'environnement | `source .venv/bin/activate` |
| Désactiver l'environnement | `deactivate` |
| Voir la version de Python | `python --version` |

Une fois activé, ton invite affiche `(.venv)`, et `python` comme `pip` pointent vers la bulle, pas vers le système. Le venv est une bulle isolée par projet : ses dépendances n'entrent pas en conflit avec les autres.

---

## pip et dépendances

| Intention | Commande |
|---|---|
| Installer un paquet | `pip install nom_du_paquet` |
| Figer les dépendances installées | `pip freeze > requirements.txt` |
| Réinstaller depuis le fichier figé | `pip install -r requirements.txt` |

`requirements.txt` liste les paquets et leurs versions exactes, pour recréer le même environnement ailleurs. On le commite.
