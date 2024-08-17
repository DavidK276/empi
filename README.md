# empi

Systém pre správu obsahu pre predmet `Účasť na empirickom výskume`.

# Spustenie

Pre otestovanie systému na lokálnom systéme je možné použiť príkaz

```shell
docker compose up -f docker-compose.yml -f docker-compose.debug.yml up
```

Na nasadenie do prevádzky slúži príkaz

```shell
docker compose up -d docker-compose.yml -f docker-compose.production.yml up -d
```

# Konfigurácia

Pred spustením do prevádzky bude v súbore `docker-compose.production.yml` potrebné nastaviť hodnoty.

`ALLOWED_HOSTS`: zoznam hostnames oddelených čiarkami, pomocou ktorých môže byť otvorené API, napr. `api.example.com`

`WEB_URL`: URL na web CMS, napr. `https://example.com` alebo `https://example.com/empi`

`FROM_EMAIL`: emailová adresa, ktorá bude uvádzaná ako odosielateľ systémových emailov, napr. `noreply@example.com`

`REPLY_TO_EMAILS`: zoznam emailových adries oddelených čiarkami, ktoré budú uvedené ako adresy pre odpoveď na systémové
emaily, napr. `admin@example.com`

`ORIGIN`: rovnaká hodnota ako `WEB_URL`

`EXT_SERVER_URL`: URL, cez ktorú je dostupné API, napr. `https://api.example.com`

`COOKIE_SECRET`: **bezpečne** vygenerovaný náhodný reťazec dlhý presne 32 znakov

# Vytvorenie prvého konta vyučujúceho

Prvé konto pre vyučujúceho sa vytvorí automaticky, pokiaľ budú pre kontajner `api` nastavené hodnoty pre premenné
prostredia `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD`