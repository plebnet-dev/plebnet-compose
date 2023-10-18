## Build

Docker images are created using a `Dockerfile`, which is a text file containing instructions on how to build the image. 

The `docs.Dockerfile` (in the base of this repo) includes this container's build recipe


```docker

{! ../docs.Dockerfile !}

```

You can build a container from a single dockerfile like this:

```sh
docker build -f docs.Dockerfile -t plebnet-compose:v1 --load .
```

This builds the image and gives it the name `plebenet-compose` and tag `v1`

```sh
docker images

REPOSITORY          TAG       IMAGE ID       CREATED         SIZE
plebnet-compose     v1        6b50b5681519   4 minutes ago   475MB
...
```

This way of building is suitable when there is only one image, but it quickly becomes cumbersome when dealing with multiple related images and services. We'll see in a moment how to handle this with `compose` [Compose](compose.html).
