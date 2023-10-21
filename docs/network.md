

When you run a compose stack, docker sets up mini-network so the containers can communicate with to each other using web protocols.

## Ports

Services may include a `ports` section that maps a container's port to the host machine so it may be accessed over localhost

```yaml
    ports:
      - "8000:8000"
```

## DNS resolution

Services may contact each other using their host name, which automatically resolves to the container's ip address.

See the [Dashboard Example](dashboard.md#connecting-to-the-database) to see how this is utilized to connect to a local database.
