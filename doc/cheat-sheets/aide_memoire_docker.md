# Aide-mémoire — Docker

Organisé par intention. Les commandes compose se lancent depuis la racine du projet, là où vit `compose.yaml`.

---

## Le modèle mental : host, conteneur, volume

```
   Ta machine (host)                        Conteneur "db"
  ┌────────────────────┐                  ┌──────────────────────────────────┐
  │ Python (psycopg)   │── localhost ────▶│ Postgres + TimescaleDB           │
  │   se connecte :5432│   port 5432:5432 │   écoute sur :5432               │
  └────────────────────┘                  │   écrit dans /var/lib/postgresql/data
                                          └───────────────┬──────────────────┘
                                                          │
                         Volume nommé "pgdata" ◀──────────┘
                         (vit en dehors du conteneur, fait survivre les données)
```

Le port `5432:5432` relie ta machine au conteneur. Le volume garde les données même si le conteneur disparaît.

---

## Vérifier l'installation

| Intention | Commande |
|---|---|
| Voir la version de Docker | `docker --version` |
| Voir la version de Compose | `docker compose version` |
| Test rapide de Docker | `docker run hello-world` |

---

## Cycle de vie des services

| Intention | Commande |
|---|---|
| Démarrer les services en arrière-plan | `docker compose up -d` |
| Voir l'état des services | `docker compose ps` |
| Arrêter et supprimer les conteneurs (garde les données) | `docker compose down` |
| Arrêter et supprimer aussi le volume (efface les données) | `docker compose down -v` |

```
docker compose up -d    ->  conteneur EN MARCHE
docker compose down     ->  conteneur supprimé,  volume CONSERVÉ   (données gardées)
docker compose down -v  ->  conteneur supprimé,  volume SUPPRIMÉ   (données effacées)
```

Le `-v` est le geste à connaître et à manier avec prudence : c'est lui qui efface ta base.

---

## Inspecter

| Intention | Commande |
|---|---|
| Voir les logs d'un service et les suivre | `docker compose logs -f db` |
| Voir les logs sans suivre (affiche et rend la main) | `docker compose logs db` |

Astuce : pour arrêter le suivi des logs, `Ctrl-C`. Ça n'arrête pas le conteneur, juste l'affichage.

---

## Exécuter une commande dans le conteneur

| Intention | Commande |
|---|---|
| Ouvrir psql interactif dans le conteneur | `docker compose exec db psql -U elec -d elec` |
| Exécuter un fichier SQL dans le conteneur | `docker compose exec -T db psql -U elec -d elec < schema.sql` |

`exec` lance une commande dans un conteneur déjà en marche. Le `-T` est nécessaire quand on redirige un fichier avec `<`.

---

## psql (une fois connecté, invite `elec=#`)

| Intention | Commande |
|---|---|
| Lister les tables | `\dt` |
| Lister les bases | `\l` |
| Quitter psql | `\q` |
