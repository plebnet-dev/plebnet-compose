
Docker compose simplifies the process of building and running containers by putting all the run options in a single `docker-compose.yml` config file.

As an example, here's this project's docker-compose.yml

```yaml
{! ../docker-compose.yaml !}
```


This allows us to run (or build) the container with a single command:

```sh
docker compose up docs
# container running at localhost:8000 or 0.0.0.0:8000
```

The above command will automatically build the image if it hasn't already been built.

We can also force a rebuild like this:

```sh
docker compose build docs
```
