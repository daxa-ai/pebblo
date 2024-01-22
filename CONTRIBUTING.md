
# Daxa ai

Description

<hr>

## Clone
```bash
git clone https://github.com/daxa-ai/langchain-2.3-rc1.git -b main
```

## Prerequisites for build
 - create a virtual environment, activate it and install `poetry` module
```bash
python3 -m venv .venv; source .venv/bin/activate
pip install poetry
```

## Resolving dependencies

It will use pyproject.toml to create a `.whl` and a `.tar.gz` under `dist/` directory.

Note: poetry.lock file is used to define & lock dependencies, dont delete it. To lock dependencies to their later releases, use below command and commit poetry.lock file
```bash
poetry install
```

## Build

Below command will create a build under `dist/` directory.
```bash
poetry build
```

## Install python dependencies

```bash
poetry install
```
## Install locally

```bash
cd dist/
pip install <package-name>
```

## Uninstallation

```bash
pip uninstall daxa
```

## Update new dependency package

- Add package in `pyproject.toml` under `[tool.poetry.dependencies]` and rerun below:
  ```bash
  poetry install
  ```
Note: dont forget to push updated poetry.lock along with it

<hr>

## Usage
may define usages.
