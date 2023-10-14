
## running the container (the hard way)


`docker run`

* This is the basic command used to create and start a container from a specified Docker image.

```sh
docker run --rm -v $PWD:/code -p 8000:8000 --name plebnet-container plebnet-compose
```

`--rm`

* This option tells Docker to automatically remove the container when it exits, which helps to keep your system clean by removing containers you no longer need.

`-v $PWD:/code`

* The `-v` option is used to create a volume, which allows you to share files between your host system and the container.
* `$PWD` is an environment variable that holds the current working directory on your host system.
* `:/code` specifies the path inside the container where the host system's current working directory will be mounted.

So, `-v $PWD:/code` maps the current working directory on your host system to /code inside the container, allowing files to be shared between the two.

`-p 8000:8000:`

* The `-p` option is used to map a port on your host system to a port on the container.
* `8000:8000` maps port `8000` on your host system to port `8000` on the container, allowing network traffic to be forwarded between them.

`--name plebnet-container`

* The `--name` option allows you to specify a name for the container, making it easier to identify and manage.
plebnet-container is the name you've chosen for this container.

`plebnet-compose`

This is the name of the Docker image from which you want to create the container.
The docker run command will create a new container from the plebnet-compose image, using the options specified.


Together, this command will create and start a new container named plebnet-container from the plebnet-compose image, with the current working directory on your host system mounted to /code inside the container, and port 8000 on your host system mapped to port 8000 on the container. The container will be automatically removed when it exits due to the --rm option.

### stopping the container

```sh
docker stop plebnet-container
```
