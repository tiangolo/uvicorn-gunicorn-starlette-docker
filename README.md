## DEPRECATED 🚨

This Docker image is now deprecated. There's no need to use it, you can just use Uvicorn with `--workers`. ✨

Read more about it below.

---

[![Test](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/actions/workflows/test.yml/badge.svg)](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/actions/workflows/test.yml) [![Deploy](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/workflows/Deploy/badge.svg)](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/actions?query=workflow%3ADeploy)

## Supported tags and respective `Dockerfile` links

* [`python3.11`, `latest` _(Dockerfile)_](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/blob/master/docker-images/python3.11.dockerfile)
* [`python3.10`, _(Dockerfile)_](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/blob/master/docker-images/python3.10.dockerfile)
* [`python3.9`, _(Dockerfile)_](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/blob/master/docker-images/python3.9.dockerfile)
* [`python3.11-slim` _(Dockerfile)_](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/blob/master/docker-images/python3.11-slim.dockerfile)
* [`python3.10-slim` _(Dockerfile)_](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/blob/master/docker-images/python3.10-slim.dockerfile)
* [`python3.9-slim` _(Dockerfile)_](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/blob/master/docker-images/python3.9-slim.dockerfile)

## Deprecated tags

🚨 These tags are no longer supported or maintained, they are removed from the GitHub repository, but the last versions pushed might still be available in Docker Hub if anyone has been pulling them:

* `python-3.8`
* `python-3.8-slim`
* `python3.8-alpine3.10`
* `python3.9-alpine3.14`
* `python3.7`
* `python3.7-alpine3.8`
* `python3.6`
* `python3.6-alpine3.8`

The last date tags for these versions are:

* `python-3.8-2024-11-02`
* `python-3.8-slim-2024-11-02`
* `python3.8-alpine3.10-2024-03-17`
* `python3.9-alpine3.14-2024-03-17`
* `python3.7-2024-11-02`
* `python3.7-alpine3.8-2024-03-17`
* `python3.6-2022-11-25`
* `python3.6-alpine3.8-2022-11-25`

---

**Note**: There are [tags for each build date](https://hub.docker.com/r/tiangolo/uvicorn-gunicorn-starlette/tags). If you need to "pin" the Docker image version you use, you can select one of those tags. E.g. `tiangolo/uvicorn-gunicorn-starlette:python3.11-2024-11-02`.

# uvicorn-gunicorn-starlette

[**Docker**](https://www.docker.com/) image with [**Uvicorn**](https://www.uvicorn.org/) managed by [**Gunicorn**](https://gunicorn.org/) for high-performance [**Starlette**](https://www.starlette.io/) web applications in **[Python](https://www.python.org/)** with performance auto-tuning.

**GitHub repo**: [https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker)

**Docker Hub image**: [https://hub.docker.com/r/tiangolo/uvicorn-gunicorn-starlette/](https://hub.docker.com/r/tiangolo/uvicorn-gunicorn-starlette/)

## Description

**Starlette** has shown to be a Python web framework with [one of the best performances, as measured by third-party benchmarks](https://www.techempower.com/benchmarks/#section=test&runid=a979de55-980d-4721-a46f-77298b3f3923&hw=ph&test=fortune&l=zijzen-7).

The achievable performance is on par with (and in many cases superior to) **Go** and **Node.js** frameworks.

This image has an **auto-tuning** mechanism included to start a number of worker processes based on the available CPU cores. That way you can just add your code and get **high performance** automatically, which is useful in **simple deployments**.

## 🚨 WARNING: You Probably Don't Need this Docker Image

You are probably using **Kubernetes** or similar tools. In that case, you probably **don't need this image** (or any other **similar base image**). You are probably better off **building a Docker image from scratch** as explained in the docs for [FastAPI in Containers - Docker: Build a Docker Image for FastAPI](https://fastapi.tiangolo.com/deployment/docker/#replication-number-of-processes), the same process could be applied to Starlette.

### Cluster Replication

If you have a cluster of machines with **Kubernetes**, Docker Swarm Mode, Nomad, or other similar complex system to manage distributed containers on multiple machines, then you will probably want to **handle replication** at the **cluster level** instead of using a **process manager** (like Gunicorn with Uvicorn workers) in each container, which is what this Docker image does.

In those cases (e.g. using Kubernetes) you would probably want to build a **Docker image from scratch**, installing your dependencies, and running **a single Uvicorn process** instead of this image.

For example, your `Dockerfile` could look like:

```Dockerfile
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

You can read more about this in the [FastAPI documentation about: FastAPI in Containers - Docker](https://fastapi.tiangolo.com/deployment/docker/#replication-number-of-processes) as the same ideas would apply to Starlette.

### Multiple Workers

If you definitely want to have multiple workers on a single container, Uvicorn now supports handling subprocesses, including restarting dead ones. So there's no need for Gunicorn to manage multiple workers in a single container.

You could modify the example `Dockerfile` from above, adding the `--workers` option to Uvicorn, like:

```Dockerfile
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "4"]
```

That's all you need. You don't need this Docker image at all. 😅

You can read more about it in the [FastAPI Docs about Deployment with Docker](https://fastapi.tiangolo.com/deployment/docker/).

## Technical Details

Uvicorn didn't have support for managing worker processing including restarting dead workers. But now it does.

Before that, Gunicorn could be used as a process manager, running Uvicorn workers. This added complexity that is no longer necessary.

## Legacy Docs

The rest of this document is kept for historical reasons, but you probably don't need it. 😅

### `tiangolo/uvicorn-gunicorn-starlette`

This image will set a sensible configuration based on the server it is running on (the amount of CPU cores available) without making sacrifices.

It has sensible defaults, but you can configure it with environment variables or override the configuration files.

There is also a slim version. If you want that, use one of the tags from above.

### `tiangolo/uvicorn-gunicorn`

This image (`tiangolo/uvicorn-gunicorn-starlette`) is based on [**tiangolo/uvicorn-gunicorn**](https://github.com/tiangolo/uvicorn-gunicorn-docker).

That image is what actually does all the work.

This image just installs Starlette and has the documentation specifically targeted at Starlette.

If you feel confident about your knowledge of Uvicorn, Gunicorn and ASGI, you can use that image directly.

### `tiangolo/uvicorn-gunicorn-fastapi`

There is a sibling Docker image: [**tiangolo/uvicorn-gunicorn-fastapi**](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker)

If you are creating a new [**FastAPI**](https://fastapi.tiangolo.com/) web application you should use [**tiangolo/uvicorn-gunicorn-fastapi**](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker) instead.

**Note**: FastAPI is based on Starlette and adds several features on top of it. Useful for APIs and other cases: data validation, data conversion, documentation with OpenAPI, dependency injection, security/authentication and others.

## How to use

You don't need to clone the GitHub repo.

You can use this image as a base image for other images.

Assuming you have a file `requirements.txt`, you could have a `Dockerfile` like this:

```Dockerfile
FROM tiangolo/uvicorn-gunicorn-starlette:python3.11

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app
```

It will expect a file at `/app/app/main.py`.

Or otherwise a file at `/app/main.py`.

And will expect it to contain a variable `app` with your Starlette application.

Then you can build your image from the directory that has your `Dockerfile`, e.g:

```bash
docker build -t myimage ./
```

## Quick Start

* Go to your project directory.
* Create a `Dockerfile` with:

```Dockerfile
FROM tiangolo/uvicorn-gunicorn-starlette:python3.11

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app
```

* Create an `app` directory and enter in it.
* Create a `main.py` file with:

```Python
from starlette.applications import Starlette
from starlette.responses import JSONResponse

app = Starlette()


@app.route("/")
async def homepage(request):
    return JSONResponse({"message": "Hello World!"})
```

* You should now have a directory structure like:

```
.
├── app
│   └── main.py
└── Dockerfile
```

* Go to the project directory (in where your `Dockerfile` is, containing your `app` directory).
* Build your Starlette image:

```bash
docker build -t myimage .
```

* Run a container based on your image:

```bash
docker run -d --name mycontainer -p 80:80 myimage
```

Now you have an optimized Starlette server in a Docker container. Auto-tuned for your current server (and number of CPU cores).

You should be able to check it in your Docker container's URL, for example: http://192.168.99.100/ or http://127.0.0.1/ (or equivalent, using your Docker host).

You will see something like:

```JSON
{"message": "Hello World!"}
```

## Dependencies and packages

You will probably also want to add any dependencies for your app and pin them to a specific version, probably including Uvicorn, Gunicorn, and Starlette.

This way you can make sure your app always works as expected.

You could install packages with `pip` commands in your `Dockerfile`, using a `requirements.txt`, or even using [Poetry](https://python-poetry.org/).

And then you can upgrade those dependencies in a controlled way, running your tests, making sure that everything works, but without breaking your production application if some new version is not compatible.

### Using Poetry

Here's a small example of one of the ways you could install your dependencies making sure you have a pinned version for each package.

Let's say you have a project managed with [Poetry](https://python-poetry.org/), so, you have your package dependencies in a file `pyproject.toml`. And possibly a file `poetry.lock`.

Then you could have a `Dockerfile` using Docker multi-stage building with:

```Dockerfile
FROM python:3.9 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM tiangolo/uvicorn-gunicorn-starlette:python3.11

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app
```

That will:

* Install poetry and configure it for running inside of the Docker container.
* Copy your application requirements.
    * Because it uses `./poetry.lock*` (ending with a `*`), it won't crash if that file is not available yet.
* Install the dependencies.
* Then copy your app code.

It's important to copy the app code *after* installing the dependencies, that way you can take advantage of Docker's cache. That way it won't have to install everything from scratch every time you update your application files, only when you add new dependencies.

This also applies for any other way you use to install your dependencies. If you use a `requirements.txt`, copy it alone and install all the dependencies on the top of the `Dockerfile`, and add your app code after it.

## Advanced usage

### Environment variables

These are the environment variables that you can set in the container to configure it and their default values:

#### `MODULE_NAME`

The Python "module" (file) to be imported by Gunicorn, this module would contain the actual application in a variable.

By default:

* `app.main` if there's a file `/app/app/main.py` or
* `main` if there's a file `/app/main.py`

For example, if your main file was at `/app/custom_app/custom_main.py`, you could set it like:

```bash
docker run -d -p 80:80 -e MODULE_NAME="custom_app.custom_main" myimage
```

#### `VARIABLE_NAME`

The variable inside of the Python module that contains the Starlette application.

By default:

* `app`

For example, if your main Python file has something like:

```Python
from starlette.applications import Starlette
from starlette.responses import JSONResponse

api = Starlette()


@api.route("/")
async def homepage(request):
    return JSONResponse({"message": "Hello World!"})
```

In this case `api` would be the variable with the Starlette application. You could set it like:

```bash
docker run -d -p 80:80 -e VARIABLE_NAME="api" myimage
```

#### `APP_MODULE`

The string with the Python module and the variable name passed to Gunicorn.

By default, set based on the variables `MODULE_NAME` and `VARIABLE_NAME`:

* `app.main:app` or
* `main:app`

You can set it like:

```bash
docker run -d -p 80:80 -e APP_MODULE="custom_app.custom_main:api" myimage
```

#### `GUNICORN_CONF`

The path to a Gunicorn Python configuration file.

By default:

* `/app/gunicorn_conf.py` if it exists
* `/app/app/gunicorn_conf.py` if it exists
* `/gunicorn_conf.py` (the included default)

You can set it like:

```bash
docker run -d -p 80:80 -e GUNICORN_CONF="/app/custom_gunicorn_conf.py" myimage
```

You can use the [config file from the base image](https://github.com/tiangolo/uvicorn-gunicorn-docker/blob/master/docker-images/gunicorn_conf.py) as a starting point for yours.

#### `WORKERS_PER_CORE`

This image will check how many CPU cores are available in the current server running your container.

It will set the number of workers to the number of CPU cores multiplied by this value.

By default:

* `1`

You can set it like:

```bash
docker run -d -p 80:80 -e WORKERS_PER_CORE="3" myimage
```

If you used the value `3` in a server with 2 CPU cores, it would run 6 worker processes.

You can use floating point values too.

So, for example, if you have a big server (let's say, with 8 CPU cores) running several applications, and you have a Starlette application that you know won't need high performance. And you don't want to waste server resources. You could make it use `0.5` workers per CPU core. For example:

```bash
docker run -d -p 80:80 -e WORKERS_PER_CORE="0.5" myimage
```

In a server with 8 CPU cores, this would make it start only 4 worker processes.

**Note**: By default, if `WORKERS_PER_CORE` is `1` and the server has only 1 CPU core, instead of starting 1 single worker, it will start 2. This is to avoid bad performance and blocking applications (server application) on small machines (server machine/cloud/etc). This can be overridden using `WEB_CONCURRENCY`.

#### `MAX_WORKERS`

Set the maximum number of workers to use.

You can use it to let the image compute the number of workers automatically but making sure it's limited to a maximum.

This can be useful, for example, if each worker uses a database connection and your database has a maximum limit of open connections.

By default it's not set, meaning that it's unlimited.

You can set it like:

```bash
docker run -d -p 80:80 -e MAX_WORKERS="24" myimage
```

This would make the image start at most 24 workers, independent of how many CPU cores are available in the server.

#### `WEB_CONCURRENCY`

Override the automatic definition of number of workers.

By default:

* Set to the number of CPU cores in the current server multiplied by the environment variable `WORKERS_PER_CORE`. So, in a server with 2 cores, by default it will be set to `2`.

You can set it like:

```bash
docker run -d -p 80:80 -e WEB_CONCURRENCY="2" myimage
```

This would make the image start 2 worker processes, independent of how many CPU cores are available in the server.

#### `HOST`

The "host" used by Gunicorn, the IP where Gunicorn will listen for requests.

It is the host inside of the container.

So, for example, if you set this variable to `127.0.0.1`, it will only be available inside the container, not in the host running it.

It's is provided for completeness, but you probably shouldn't change it.

By default:

* `0.0.0.0`

#### `PORT`

The port the container should listen on.

If you are running your container in a restrictive environment that forces you to use some specific port (like `8080`) you can set it with this variable.

By default:

* `80`

You can set it like:

```bash
docker run -d -p 80:8080 -e PORT="8080" myimage
```

#### `BIND`

The actual host and port passed to Gunicorn.

By default, set based on the variables `HOST` and `PORT`.

So, if you didn't change anything, it will be set by default to:

* `0.0.0.0:80`

You can set it like:

```bash
docker run -d -p 80:8080 -e BIND="0.0.0.0:8080" myimage
```

#### `LOG_LEVEL`

The log level for Gunicorn.

One of:

* `debug`
* `info`
* `warning`
* `error`
* `critical`

By default, set to `info`.

If you need to squeeze more performance sacrificing logging, set it to `warning`, for example:

You can set it like:

```bash
docker run -d -p 80:8080 -e LOG_LEVEL="warning" myimage
```

#### `WORKER_CLASS`

The class to be used by Gunicorn for the workers.

By default, set to `uvicorn.workers.UvicornWorker`.

The fact that it uses Uvicorn is what allows using ASGI frameworks like Starlette, and that is also what provides the maximum performance.

You probably shouldn't change it.

But if for some reason you need to use the alternative Uvicorn worker: `uvicorn.workers.UvicornH11Worker` you can set it with this environment variable.

You can set it like:

```bash
docker run -d -p 80:8080 -e WORKER_CLASS="uvicorn.workers.UvicornH11Worker" myimage
```

#### `TIMEOUT`

Workers silent for more than this many seconds are killed and restarted.

Read more about it in the [Gunicorn docs: timeout](https://docs.gunicorn.org/en/stable/settings.html#timeout).

By default, set to `120`.

Notice that Uvicorn and ASGI frameworks like Starlette are async, not sync. So it's probably safe to have higher timeouts than for sync workers.

You can set it like:

```bash
docker run -d -p 80:8080 -e TIMEOUT="20" myimage
```

#### `KEEP_ALIVE`

The number of seconds to wait for requests on a Keep-Alive connection.

Read more about it in the [Gunicorn docs: keepalive](https://docs.gunicorn.org/en/stable/settings.html#keepalive).

By default, set to `2`.

You can set it like:

```bash
docker run -d -p 80:8080 -e KEEP_ALIVE="20" myimage
```

#### `GRACEFUL_TIMEOUT`

Timeout for graceful workers restart.

Read more about it in the [Gunicorn docs: graceful-timeout](https://docs.gunicorn.org/en/stable/settings.html#graceful-timeout).

By default, set to `120`.

You can set it like:

```bash
docker run -d -p 80:8080 -e GRACEFUL_TIMEOUT="20" myimage
```

#### `ACCESS_LOG`

The access log file to write to.

By default `"-"`, which means stdout (print in the Docker logs).

If you want to disable `ACCESS_LOG`, set it to an empty value.

For example, you could disable it with:

```bash
docker run -d -p 80:8080 -e ACCESS_LOG= myimage
```

#### `ERROR_LOG`

The error log file to write to.

By default `"-"`, which means stderr (print in the Docker logs).

If you want to disable `ERROR_LOG`, set it to an empty value.

For example, you could disable it with:

```bash
docker run -d -p 80:8080 -e ERROR_LOG= myimage
```

#### `GUNICORN_CMD_ARGS`

Any additional command line settings for Gunicorn can be passed in the `GUNICORN_CMD_ARGS` environment variable.

Read more about it in the [Gunicorn docs: Settings](https://docs.gunicorn.org/en/stable/settings.html#settings).

These settings will have precedence over the other environment variables and any Gunicorn config file.

For example, if you have a custom TLS/SSL certificate that you want to use, you could copy them to the Docker image or mount them in the container, and set [`--keyfile` and `--certfile`](http://docs.gunicorn.org/en/latest/settings.html#ssl) to the location of the files, for example:

```bash
docker run -d -p 80:8080 -e GUNICORN_CMD_ARGS="--keyfile=/secrets/key.pem --certfile=/secrets/cert.pem" -e PORT=443 myimage
```

**Note**: instead of handling TLS/SSL yourself and configuring it in the container, it's recommended to use a "TLS Termination Proxy" like [Traefik](https://docs.traefik.io/). You can read more about it in the [FastAPI documentation about HTTPS](https://fastapi.tiangolo.com/deployment/#https).

#### `PRE_START_PATH`

The path where to find the pre-start script.

By default, set to `/app/prestart.sh`.

You can set it like:

```bash
docker run -d -p 80:8080 -e PRE_START_PATH="/custom/script.sh" myimage
```

### Custom Gunicorn configuration file

The image includes a default Gunicorn Python config file at `/gunicorn_conf.py`.

It uses the environment variables declared above to set all the configurations.

You can override it by including a file in:

* `/app/gunicorn_conf.py`
* `/app/app/gunicorn_conf.py`
* `/gunicorn_conf.py`

### Custom `/app/prestart.sh`

If you need to run anything before starting the app, you can add a file `prestart.sh` to the directory `/app`. The image will automatically detect and run it before starting everything.

For example, if you want to add Alembic SQL migrations (with SQLALchemy), you could create a `./app/prestart.sh` file in your code directory (that will be copied by your `Dockerfile`) with:

```bash
#! /usr/bin/env bash

# Let the DB start
sleep 10;
# Run migrations
alembic upgrade head
```

and it would wait 10 seconds to give the database some time to start and then run that `alembic` command.

If you need to run a Python script before starting the app, you could make the `/app/prestart.sh` file run your Python script, with something like:

```bash
#! /usr/bin/env bash

# Run custom Python script before starting
python /app/my_custom_prestart_script.py
```

You can customize the location of the prestart script with the environment variable `PRE_START_PATH` described above.

### Development live reload

The default program that is run is at `/start.sh`. It does everything described above.

There's also a version for development with live auto-reload at:

```bash
/start-reload.sh
```

#### Details

For development, it's useful to be able to mount the contents of the application code inside of the container as a Docker "host volume", to be able to change the code and test it live, without having to build the image every time.

In that case, it's also useful to run the server with live auto-reload, so that it re-starts automatically at every code change.

The additional script `/start-reload.sh` runs Uvicorn alone (without Gunicorn) and in a single process.

It is ideal for development.

#### Usage

For example, instead of running:

```bash
docker run -d -p 80:80 myimage
```

You could run:

```bash
docker run -d -p 80:80 -v $(pwd):/app myimage /start-reload.sh
```

* `-v $(pwd):/app`: means that the directory `$(pwd)` should be mounted as a volume inside of the container at `/app`.
    * `$(pwd)`: runs `pwd` ("print working directory") and puts it as part of the string.
* `/start-reload.sh`: adding something (like `/start-reload.sh`) at the end of the command, replaces the default "command" with this one. In this case, it replaces the default (`/start.sh`) with the development alternative `/start-reload.sh`.

#### Development live reload - Technical Details

As `/start-reload.sh` doesn't run with Gunicorn, any of the configurations you put in a `gunicorn_conf.py` file won't apply.

But these environment variables will work the same as described above:

* `MODULE_NAME`
* `VARIABLE_NAME`
* `APP_MODULE`
* `HOST`
* `PORT`
* `LOG_LEVEL`

## 🚨 Alpine Python Warning

In short: You probably shouldn't use Alpine for Python projects, instead use the `slim` Docker image versions.

---

Do you want more details? Continue reading 👇

Alpine is more useful for other languages where you build a static binary in one Docker image stage (using multi-stage Docker building) and then copy it to a simple Alpine image, and then just execute that binary. For example, using Go.

But for Python, as Alpine doesn't use the standard tooling used for building Python extensions, when installing packages, in many cases Python (`pip`) won't find a precompiled installable package (a "wheel") for Alpine. And after debugging lots of strange errors you will realize that you have to install a lot of extra tooling and build a lot of dependencies just to use some of these common Python packages. 😩

This means that, although the original Alpine image might have been small, you end up with a an image with a size comparable to the size you would have gotten if you had just used a standard Python image (based on Debian), or in some cases even larger. 🤯

And in all those cases, it will take much longer to build, consuming much more resources, building dependencies for longer, and also increasing its carbon footprint, as you are using more CPU time and energy for each build. 🌳

If you want slim Python images, you should instead try and use the `slim` versions that are still based on Debian, but are smaller. 🤓

## Tests

All the image tags, configurations, environment variables and application options are tested.

## Release Notes

### Latest Changes

#### Upgrades

* ⬆ Bump starlette from 0.47.1 to 0.47.3. PR [#226](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/226) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump uvicorn[standard] from 0.34.3 to 0.35.0. PR [#222](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/222) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump starlette from 0.47.0 to 0.47.1. PR [#221](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/221) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump starlette from 0.46.0 to 0.47.0. PR [#219](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/219) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump uvicorn[standard] from 0.34.0 to 0.34.3. PR [#220](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/220) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump starlette from 0.41.2 to 0.46.0. PR [#213](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/213) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump uvicorn[standard] from 0.32.0 to 0.34.0. PR [#205](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/205) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump starlette from 0.27.0 to 0.41.2. PR [#199](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/199) by [@dependabot[bot]](https://github.com/apps/dependabot).
* Bump starlette from 0.27.0 to 0.40.0 in /docker-images. PR [#196](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/196) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump uvicorn[standard] from 0.20.0 to 0.32.0. PR [#197](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/197) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔥 Drop support for Python 3.7 and 3.8. PR [#200](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/200) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump gunicorn from 22.0.0 to 23.0.0. PR [#181](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/181) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Bump gunicorn from 21.2.0 to 22.0.0 in /docker-images. PR [#169](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/169) by [@dependabot[bot]](https://github.com/apps/dependabot).

#### Docs

* 📝 Deprecate this Docker image, use Uvicorn with `--workers` ✨. PR [#183](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/183) by [@tiangolo](https://github.com/tiangolo).

#### Internal

* ⬆ Bump peter-evans/dockerhub-description from 4 to 5. PR [#233](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/233) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/labeler from 5 to 6. PR [#228](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/228) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/setup-python from 5 to 6. PR [#227](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/227) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/checkout from 4 to 5. PR [#225](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/225) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump tiangolo/latest-changes from 0.3.2 to 0.4.0. PR [#224](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/224) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Update labeler rules. PR [#214](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/214) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump tiangolo/latest-changes from 0.3.1 to 0.3.2. PR [#202](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/202) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Add CI Labeler. PR [#212](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/212) by [@tiangolo](https://github.com/tiangolo).
* 🔥 Remove old unused files. PR [#201](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/201) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump tiangolo/issue-manager from 0.5.0 to 0.5.1. PR [#188](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/188) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Update `issue-manager.yml`. PR [#187](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/187) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update `latest-changes` GitHub Action. PR [#185](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/185) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump docker/build-push-action from 5 to 6. PR [#173](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/173) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Update issue-manager.yml GitHub Action permissions. PR [#178](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/178) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump peter-evans/dockerhub-description from 3 to 4. PR [#163](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/163) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump docker/build-push-action from 2 to 5. PR [#162](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/162) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump docker/login-action from 1 to 3. PR [#161](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/161) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump docker/setup-buildx-action from 1 to 3. PR [#160](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/160) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/setup-python from 4 to 5. PR [#159](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/159) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔧 Add GitHub templates for discussions and issues, and security policy. PR [#167](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/167) by [@alejsdev](https://github.com/alejsdev).
* 🔧 Update `latest-changes.yml`. PR [#158](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/158) by [@alejsdev](https://github.com/alejsdev).

### 0.8.0

#### Features

* ✨ Add support for multiarch builds, including ARM (e.g. Mac M1). PR [#156](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/156) by [@tiangolo](https://github.com/tiangolo).

#### Refactors

* 🔥 Remove Alpine support. PR [#155](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/155) by [@tiangolo](https://github.com/tiangolo).

#### Upgrades

* ⬆️ Bump starlette from 0.22.0 to 0.27.0 in /docker-images. PR [#118](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/118) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Bump starlette from 0.22.0 to 0.25.0. PR [#117](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/117) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Bump starlette from 0.22.0 to 0.25.0 in /docker-images. PR [#116](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/116) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Bump gunicorn from 20.1.0 to 21.2.0. PR [#128](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/128) by [@dependabot[bot]](https://github.com/apps/dependabot).

#### Docs

* 📝 Update test badge in `README.md`. PR [#157](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/157) by [@alejsdev](https://github.com/alejsdev).

#### Internal

* ⬆️ Update mypy requirement from ^0.991 to ^1.0. PR [#114](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/114) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Update black requirement from ^22.10 to ^23.1. PR [#113](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/113) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Bump actions/checkout from 3.1.0 to 3.3.0. PR [#112](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/112) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Update Latest Changes token. PR [#119](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/119) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add GitHub Action for Docker Hub description. PR [#108](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/108) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Update mypy requirement from ^0.971 to ^0.991. PR [#103](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/103) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/setup-python from 4 to 5. PR [#141](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/141) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump peter-evans/dockerhub-description from 3 to 4. PR [#151](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/151) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump tiangolo/issue-manager from 0.4.0 to 0.5.0. PR [#153](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/153) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/checkout from 3.3.0 to 4.1.1. PR [#137](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/137) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Update dependabot. PR [#136](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/136) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update latest-changes. PR [#135](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/135) by [@tiangolo](https://github.com/tiangolo).

### 0.7.0

Highlights of this release:

* Support for Python 3.10 and 3.11.
* Deprecation of Python 3.6.
    * The last Python 3.6 image tag was pushed and is available in Docker Hub, but it won't be updated or maintained anymore.
    * The last image with a date tag is `python3.6-2022-11-25`.
* Upgraded versions of all the dependencies.

#### Features

* ✨ Add support for Python 3.10 and 3.11. PR [#107](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/107) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add support for Python 3.9 and Python 3.9 Alpine. PR [#36](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/36) by [@tiangolo](https://github.com/tiangolo).

#### Breaking Changes

* 🔥 Deprecate and remove Python 3.6. PR [#98](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/98) by [@tiangolo](https://github.com/tiangolo).

#### Upgrades

* ⬆️ Upgrade Uvicorn. PR [#99](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/99) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Bump starlette from 0.14.2 to 0.22.0 in /docker-images. PR [#90](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/90) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Upgrade Uvicorn and Starlette to the latest versions that support Python 3.6. PR [#94](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/94) by [@tiangolo](https://github.com/tiangolo).

#### Docs

* 📝 Add note to discourage Alpine with Python. PR [#39](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/39) by [@tiangolo](https://github.com/tiangolo).
* 📝 Add Kubernetes warning, when to use this image. PR [#38](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/38) by [@tiangolo](https://github.com/tiangolo).
* ✏️ Fix typo duplicate "Note" in Readme. PR [#37](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/37) by [@tiangolo](https://github.com/tiangolo).

#### Internal

* ⬆️ Update docker requirement from ^5.0.3 to ^6.0.1. PR [#104](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/104) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Update black requirement from ^20.8b1 to ^22.10. PR [#102](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/102) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Update autoflake requirement from ^1.3.1 to ^2.0.0. PR [#101](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/101) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔥 Remove old Travis backup. PR [#106](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/106) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade CI OS. PR [#105](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/105) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update Dependabot config. PR [#100](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/100) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add scheduled CI. PR [#97](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/97) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Bump tiangolo/issue-manager from 0.2.0 to 0.4.0. PR [#29](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/29) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Add alls-green GitHub Action. PR [#96](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/96) by [@tiangolo](https://github.com/tiangolo).
* 👷 Do not run double CI for PRs, run on push only on master. PR [#95](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/95) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Update pytest requirement from ^5.4.1 to ^7.0.1. PR [#58](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/58) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Update isort requirement from ^4.3.21 to ^5.8.0. PR [#34](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/34) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Update black requirement from ^19.10b0 to ^20.8b1. PR [#32](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/32) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Bump actions/setup-python from 1 to 4.1.0. PR [#82](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/82) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Update docker requirement from ^4.2.0 to ^5.0.3. PR [#40](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/40) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Update mypy requirement from ^0.770 to ^0.971. PR [#83](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/83) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆️ Bump actions/checkout from 2 to 3.1.0. PR [#86](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/86) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Update Latest Changes GitHub Action. PR [#26](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/26) by [@tiangolo](https://github.com/tiangolo).
* 📌 Add external dependencies to get automatic Dependabot upgrade PRs. PR [#27](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/27) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add GitHub Action latest-changes, update issue-manager, add funding. PR [#22](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/22) by [@tiangolo](https://github.com/tiangolo).

### 0.6.0

* Add docs about installing and pinning dependencies. PR [#19](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/19).
* Add `slim` version. PR [#18](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/18).
* Fix testing race condition by sending the request first PR [#17](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/17).
* Update and refactor bringing all the new features from the base image. Includes:
    * Centralize, simplify, and deduplicate code and setup
    * Move CI to GitHub actions
    * Add Python 3.8 (and Alpine)
    * Add new configs and docs:
        * `WORKER_CLASS`
        * `TIMEOUT`
        * `KEEP_ALIVE`
        * `GRACEFUL_TIMEOUT`
        * `ACCESS_LOG`
        * `ERROR_LOG`
        * `GUNICORN_CMD_ARGS`
        * `MAX_WORKERS`
    * PR [#16](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/16).
* Disable pip cache during installation. PR [#15](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/15).
* Migrate local development from Pipenv to Poetry. PR [#14](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/14).
* Add docs for custom `PRE_START_PATH` env var. PR [#13](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/13).

### 0.5.0

* Refactor tests to use env vars and add image tags for each build date, like `tiangolo/uvicorn-gunicorn-starlette:python3.7-2019-10-15`. PR [#8](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/8).
* Upgrade Travis. PR [#5](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/5).

### 0.4.0

* Add support for live auto-reload with an additional custom script `/start-reload.sh`, check the [updated documentation](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker#development-live-reload). PR <a href="https://github.com/tiangolo/uvicorn-gunicorn-docker/pull/6" target="_blank">#6</a> in parent image.

### 0.3.0

* Set `WORKERS_PER_CORE` by default to `1`, as it shows to have the best performance on benchmarks.
* Make the default web concurrency, when `WEB_CONCURRENCY` is not set, to a minimum of 2 workers. This is to avoid bad performance and blocking applications (server application) on small machines (server machine/cloud/etc). This can be overridden using `WEB_CONCURRENCY`. This applies for example in the case where `WORKERS_PER_CORE` is set to `1` (the default) and the server has only 1 CPU core. PR <a href="https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker/pull/4" target="_blank">#4</a> and PR <a href="https://github.com/tiangolo/uvicorn-gunicorn-docker/pull/5" target="_blank">#5</a> in parent image.

### 0.2.0

* Make `/start.sh` run independently, reading and generating used default environment variables. And remove `/entrypoint.sh` as it doesn't modify anything in the system, only reads environment variables. PR <a href="https://github.com/tiangolo/uvicorn-gunicorn-docker/pull/4" target="_blank">#4</a> in parent image.

### 0.1.0

* Add support for `/app/prestart.sh`.

## License

This project is licensed under the terms of the MIT license.
