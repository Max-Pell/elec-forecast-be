# Aide-mémoire — Git

Organisé par intention. Tu pars de ce que tu veux faire, tu trouves la commande.

---

## Le modèle mental : les zones

```
Dossier de travail --git add--> Staging --git commit--> Historique local --git push--> origin (GitHub)
   (tes fichiers)               (préparé)               (commits)                       (distant)
        ^                                                                                   |
        +----------------------------- git pull / git fetch --------------------------------+
```

Git ne contacte le réseau que sur `push`, `pull`, `fetch`. Le reste est local.

---

## Configuration et authentification (une seule fois)

| Intention | Commande |
|---|---|
| Voir la version de Git | `git --version` |
| Définir ton nom | `git config --global user.name "Ton Nom"` |
| Définir ton email | `git config --global user.email "email"` |
| Fixer la branche par défaut à main | `git config --global init.defaultBranch main` |
| Voir ta configuration globale | `git config --global --list` |
| Générer une clé SSH | `ssh-keygen -t ed25519 -C "email"` |
| Afficher ta clé publique (à coller sur GitHub) | `cat ~/.ssh/id_ed25519.pub` |
| Tester l'accès SSH à GitHub | `ssh -T git@github.com` |

---

## La boucle quotidienne

| Intention | Commande |
|---|---|
| Initialiser un dépôt local | `git init` |
| Voir l'état des fichiers | `git status` |
| Préparer des fichiers précis (recommandé) | `git add fichier1 fichier2` |
| Tout préparer d'un coup | `git add .` ou `git add -A` |
| Voir les changements non préparés | `git diff` |
| Voir les changements préparés | `git diff --staged` |
| Enregistrer un commit | `git commit -m "message"` |
| Voir l'historique condensé | `git log --oneline` |
| Voir l'historique en graphe, toutes branches | `git log --oneline --graph --all` |
| Voir l'historique sans ouvrir le pager | `git --no-pager log --oneline` |

Astuce : pour sortir du pager (le `(END)` en bas), touche `q`.

---

## Branches et navigation

`switch` est la commande moderne et claire pour les branches. `checkout` est l'ancienne, plus large, qui fait aussi d'autres choses.

| Intention | Commande |
|---|---|
| Créer une branche et basculer dessus | `git switch -c nom` (ou `git checkout -b nom`) |
| Basculer sur une branche existante | `git switch nom` (ou `git checkout nom`) |
| Revenir à la branche précédente | `git switch -` |
| Lister les branches locales | `git branch` |
| Lister locales et distantes | `git branch -a` |
| Supprimer une branche locale (si mergée) | `git branch -d nom` |
| Forcer la suppression d'une branche locale | `git branch -D nom` |
| Supprimer une branche distante | `git push origin --delete nom` |

Schéma d'une branche créée depuis main :

```
A---B---C  (main)
         \
          D---E  (feature, HEAD)
```

### HEAD

HEAD, c'est « l'endroit où je travaille ».

```
Normal :   A---B---C  (main, HEAD)        HEAD -> branche -> commit
```

Si tu fais `git checkout <commit>`, tu te retrouves en HEAD détaché : HEAD pointe un commit directement, tu n'es plus sur une branche.

```
Détaché :  A---B---C---D  (main)
               ^
              HEAD                         HEAD -> commit directement
```

Un commit fait en HEAD détaché risque d'être perdu. Si tu veux le garder, crée une branche : `git switch -c nouvelle-branche`.

---

## Distant (remote) et synchronisation

| Intention | Commande |
|---|---|
| Relier le local à un dépôt distant existant | `git remote add origin URL_SSH` |
| Voir les remotes configurés | `git remote -v` |
| Corriger l'URL d'un remote | `git remote set-url origin URL_SSH` |
| Renommer la branche courante en main | `git branch -M main` |
| Pousser et lier la branche (premier push) | `git push -u origin nom` |
| Pousser ensuite | `git push` |
| Pousser explicitement | `git push origin nom` |
| Récupérer et intégrer | `git pull` |
| Récupérer sans intégrer (juste rafraîchir) | `git fetch` |
| Nettoyer les branches distantes disparues | `git fetch --prune` |

`git remote add` ne crée pas le dépôt sur GitHub : tu crées le dépôt vide sur le site, puis cette commande relie ton local à ce distant.

Différence push / pull selon l'argument :

| Commande | Effet |
|---|---|
| `git push` | Pousse vers l'upstream déjà configuré |
| `git push origin main` | Pousse explicitement vers `origin/main` |
| `git push -u origin main` | Pousse vers `origin/main` et configure l'upstream |
| `git pull` | Tire depuis l'upstream configuré |
| `git pull origin main` | Tire explicitement depuis `origin/main` |

Note : une pull request s'ouvre et se merge sur l'interface GitHub, pas en ligne de commande.
