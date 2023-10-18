
## Volumes

Docker volumes are used to persist data from the host to the container.
Volumes are necessary when

* Host files need to be passed into and modified by the container
* Databases need to persist accross multiple runs of the same container
* In development mode, when code needs to be modified on the host (to avoid rebuilding constantly)


## Volume Mounts

"Volume Mounts" are used to mount directories from the host into the container.

For instance, our documentation image doesn't actually contain this project's code until run time.
This is accomplished by the following line in our `docker-compose.yml`

```yaml
    volumes:
      - .:/code
```

This means mount `.` (the current working directory) into the container's `/code` directory.
When the container starts, it uses `/code` as the working directory so that `mkdocs` will automatically refresh any changes to the documentation. You can test this by modifying this file on your host system.

## Named Volumes

Named volumes are used to persist and share data between containers in a Docker Compose environment.
A typical use case is when you have a database running in one service that another service needs to access.

todo: example

