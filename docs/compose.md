
[Compose](https://docs.docker.com/compose/) is a Docker utility that allows you to `build` and `run` containers in a reproducible manner, based on a configuration file named `docker-compose.yml`.

!!! note
    `docker-compose` (hyphenated) is a standalone python tool which is gradually being replaced by `docker compose`. You may see it in older tutorials, but it behaves similarly.

## docker-compose.yml

Docker compose simplifies the process of building and running containers by putting all the run options in a single `docker-compose.yml` config file.

As an example, here's this project's `docker-compose.yml` (we'll cover each section in more detail)

```yaml
{! ../docker-compose.yaml !}
```

## Build

We can specify which service to build like this:

```sh
docker compose build docs
```

Or we can build all services at once

```sh
docker compose build
```

## Run

This allows us to run the container like this

```sh
docker compose up docs
# container running at localhost:8000 or 0.0.0.0:8000
```

The above command will automatically build the image if it hasn't already been built.

