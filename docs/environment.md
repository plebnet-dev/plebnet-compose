
Environment variables are used to pass information into the container at run time.

This allows you to build an image once but run it with different configurations (API Keys, passwords, etc) or for different environments (development vs production).

Typically, environment variables flow like this:

`.env` --> `docker-compose.yml` --> `container` --> `application`

## .env

Environment variables are typically placed in a `.env` file at the base of the repo. Docker automatically looks for `.env` when running the compose configuration. Here are the contents of this project's `.env`:


```sh

{! ../.env !}

```


!!! warning
    `.env` contains sensitive information, you should **NEVER add a .env file to git control.** `.env` files are often included in `.gitignore` to prevent accidental upload.

## docker-compose.yml

You can pass environment variables to your services using curly braces `${MY_ENV_VAR}`, like this:

```yaml
# docker-compose.yml
	...
    environment:
      SITE_NAME: ${SITE_NAME}

```

## container

Once provisioned by the compose file, the container's environment variables have been set. You can log in and verify these values for the `docs` service:

```sh
docker compose run docs bash

(base) root@4abd4921d273:/code# echo $SITE_NAME
Plebnet Compose (Oct 21 '03)
```


## application

Your application can (finally) access these values. How this is done depends on the language your app is written in. For example, in python it would be

```py
import os

print(os.environ['SITE_NAME'])

```

For this project, `SITE_NAME` is picked up by this secion of `mkdocs.yml` (in the base of this repo):

```yaml
# Project information
site_name: !ENV [SITE_NAME, "Plebnet Compose"] # if SITE_NAME is undefined, use Plebnet Compose
```

!!! note
    Your app needs to handle cases where an environment variable is missing



