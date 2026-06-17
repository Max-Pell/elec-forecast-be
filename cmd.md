## Mkdir

Créer un dossier.

- -p -> Crée les dossiers parents si ils n'existent pas

## Source

Lance un scripte

## Python -m venv ...

Crée un dossier qui  contient un environnement virtuel. On l'active avec le script {nom du dossier}/bin/activate

Par exemple : source .venv/bin/activate

Ensuite on le désactive avec deactivate (sans source)

# git

git diff --staged

git add .

git log --online -> Permet de voir l'historique des commits

git remote add origin git@github.com:TON_PSEUDO/elec-forecast-be.git -> créer le repo


| Commande                    | Effet                                                         |
| --------------------------- | ------------------------------------------------------------- |
| `git push`                | Pousse vers l'upstream déjà configuré                      |
| `git push origin main`    | Pousse explicitement vers `origin/main`                     |
| `git push -u origin main` | Pousse vers `origin/main` **et configure l'upstream** |
| `git pull`                | Tire depuis l'upstream configuré                             |
| `git pull origin main`    | Tire explicitement depuis `origin/main`                     |


# Git Branch Navigation Cheat Sheet

## Voir où on est

```bash
git branch
```

Affiche les branches locales.

```text
* feature/login
  main
  hotfix
```

Le `*` indique la branche courante.

---

## Voir l'historique

```bash
git log --oneline --graph --all
```

Exemple :

```text
* e5f6g7h (feature/login)
* d4e5f6g
| * z9y8x7w (hotfix)
|/
* c3d4e5f
* b2c3d4e
* a1b2c3d (main)
```

---

## Changer de branche

```bash
git checkout main
```

ou (moderne)

```bash
git switch main
```

Avant :

```text
main            A---B---C
                     \
feature/login         D---E (HEAD)
```

Après :

```text
main            A---B---C (HEAD)
                     \
feature/login         D---E
```

---

## Créer une branche depuis la branche courante

```bash
git checkout -b feature/payment
```

ou

```bash
git switch -c feature/payment
```

Avant :

```text
A---B---C (main, HEAD)
```

Après :

```text
A---B---C (main)
         \
          (feature/payment, HEAD)
```

---

## Aller sur un commit précis

```bash
git checkout a1b2c3d
```

Avant :

```text
A---B---C---D (main, HEAD)
```

Après :

```text
A---B---C---D (main)
    ^
    HEAD
```

⚠️ HEAD est détaché ("detached HEAD").

Tu n'es plus sur une branche.

---

## Revenir à la dernière branche utilisée

```bash
git checkout -
```

Exemple :

```text
main  <-> feature/login
```

Très pratique pour alterner entre deux branches.

---

## Créer une branche depuis un ancien commit

```bash
git checkout -b hotfix a1b2c3d
```

Avant :

```text
A---B---C---D (main)
```

Après :

```text
A---B---C---D (main)
 \
  (hotfix, HEAD)
```

---

## Voir toutes les branches

```bash
git branch -a
```

Locales :

```text
main
feature/login
```

Distantes :

```text
remotes/origin/main
remotes/origin/develop
```

---

## Supprimer une branche locale

```bash
git branch -d feature/login
```

Force la suppression :

```bash
git branch -D feature/login
```

⚠️ Impossible de supprimer la branche sur laquelle tu te trouves.

---

## Revenir au dernier commit d'une branche

```bash
git checkout main
```

Si tu étais dans un ancien commit :

```text
A---B---C---D (main)
    ^
    HEAD
```

Puis :

```bash
git checkout main
```

Résultat :

```text
A---B---C---D (main, HEAD)
```

---

## Comprendre HEAD

HEAD = "l'endroit où je travaille actuellement".

```text
A---B---C (main, HEAD)
```

HEAD pointe sur la branche `main`.

---

### Detached HEAD

```text
A---B---C---D (main)
    ^
    HEAD
```

HEAD pointe directement sur un commit.

Si tu fais un commit :

```text
A---B---C---D (main)
    \
     E (HEAD)
```

Pense à créer une branche :

```bash
git switch -c nouvelle-branche
```

Sinon le commit `E` risque d'être perdu plus tard.

---

## Les 4 commandes à retenir

```bash
git switch <branche>
```

Changer de branche.

```bash
git switch -c <nouvelle-branche>
```

Créer et changer de branche.

```bash
git checkout <commit>
```

Explorer un ancien commit.

```bash
git switch -
```

Revenir à la branche précédente.
