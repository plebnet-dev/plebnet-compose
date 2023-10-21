
We demonstrate how apps can connect to databases using the following config.

```sh
docker compose up app
# navigate to localhost:8050
```

## Defining a local SQL database

This service references the following `local_db` service


```yaml
  local_db:
    image: postgres
    restart: always
    volumes:
      - pgdata:/var/lib/postgresql/data/
    environment:
      POSTGRES_USER: ${DB_USER_LOCAL}
      POSTGRES_PASSWORD: ${DB_PASS_LOCAL}
      POSTGRES_DB: ${DB_NAME_LOCAL}
      TZ: ${TZ}
      POSTGRES_HOST_AUTH_METHOD: trust
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "${DB_HOST_LOCAL}"]
      interval: 5s
      timeout: 1s
      retries: 10
    healthcheck:
      test:
        [
          "CMD-SHELL",
          "pg_isready -U ${DB_USER_LOCAL} -d ${DB_NAME_LOCAL} -h ${DB_HOST_LOCAL} -p ${DB_PORT_LOCAL}",
        ]
      interval: 10s
      timeout: 5s
      retries: 5
    hostname: ${DB_HOST_LOCAL}

volumes:
  pgdata:

```

The `local_db` instance uses the named volume `pgdata`.
This way, changes to the database will persist whenever we restart the container.

!!! note
    Container data gets wiped every time you bring down a service!


## Connecting to the database

Docker compose's [DNS](network.md) allows the host name for the local database to automatically match the service name. This is super convenient because we don't need to keep track of ip addresses explicitly.

```yaml
  app:
    image: my-flask-app:latest
    build:
      context: app
      dockerfile: app.Dockerfile
    depends_on:
      - local_db
    environment:
      - DB_HOST=local_db
      - DB_PORT=${DB_PORT_LOCAL}
      - DB_USER=${DB_USER_LOCAL}
      - DB_PASS=${DB_PASS_LOCAL}
      - DB_NAME=${DB_NAME_LOCAL}
    volumes:
      - ./app:/usr/src/app
    depends_on:
      - local_db
    ports:
      - "8050:8050"
```


Here is how the app uses the environment variables to connect to the database 

```py
from sqlalchemy import create_engine
# Create an engine for connecting to the PostgreSQL database
engine = create_engine(
    f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
    pool_size=10,  # Adjust pool_size and max_overflow to your needs
    max_overflow=20
)
```

When you run the app, you'll see output in the terminal

```sh
connecting to db at: postgresql://postgres_user:****@local_db:5432/postgres
```


We can embed the dashboard as an iframe. Because we are accessing the app from the host, we need to use `localhost`:

```html
<iframe src="http://localhost:8050" width="1400" height="1200"></iframe>
```

<iframe src="http://localhost:8050" width="1400" height="1200"></iframe>
