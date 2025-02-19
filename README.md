## Agno Demo App

This repo contains the code for running agno demo app in 2 environments:

1. **dev**: A development environment running locally on docker
2. **prd**: A production environment running on AWS ECS

## Setup Workspace

1. Clone the git repo

> from the `agno-demo-app` dir:

2. Install workspace and activate the virtual env:

```sh
./scripts/dev_setup.sh
source .venv/bin/activate
```

Optional: Install agno-sdk in editable mode:

```sh
VIRTUAL_ENV=.venv
AGNO_DIR=../agno # Or wherever your agno-sdk is located
uv pip install -e ${AGNO_DIR}/libs/agno
uv pip install -e ${AGNO_DIR}/libs/infra/agno_docker
uv pip install -e ${AGNO_DIR}/libs/infra/agno_aws
```

3. Copy `workspace/example_secrets` to `workspace/secrets`:

```sh
cp -r workspace/example_secrets workspace/secrets
```

## Run Demo App locally

1. Install [docker desktop](https://www.docker.com/products/docker-desktop)

2. Set OpenAI Key

Set the `OPENAI_API_KEY` environment variable using

```sh
export OPENAI_API_KEY=sk-***
```

**OR** set in the `.env` file

3. Start the workspace using:

```sh
ag ws up dev
```

Open [localhost:8000/docs](http://localhost:8000/docs) to view the agno demo app.

4. Stop the workspace using:

```sh
ag ws down dev
```
