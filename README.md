## Agno Demo App

This repo contains the code for running agno demo app in 2 environments:

1. **dev**: A development environment running locally on docker
2. **prd**: A production environment running on AWS ECS

## Setup Workspace

1. Clone the git repo

> from the `agno-demo-app` dir:

2. Install workspace and activate the virtual env:

```sh
./scripts/install.sh
source .venv/bin/activate
```

3. Setup workspace:

```sh
ag ws setup
```

4. Copy `workspace/example_secrets` to `workspace/secrets`:

```sh
cp -r workspace/example_secrets workspace/secrets
```

5. Optional: Create `.env` file:

```sh
cp example.env .env
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
