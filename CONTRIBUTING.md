# Contributing to Pebblo

We are an open community. We welcome and appreciate all kinds of contributions that improve `pebblo`.

## Setting up your development environment

Pebblo is currently supported in MacOS and Linux.

The following instructions are **tested on Mac OSX and Linux (Debian).**

### Prerequisites

Install the following prerequisites. This is needed for PDF report generation.

#### Mac OSX

```sh
brew install pango
```

#### Linux (debian/ubuntu)

```sh
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0
```

## Build, Install and Run

Fork and clone the pebblo repo. From within the pebblo directory create a virtual-env, build pebblo package (in `wheel` format), install and run.

### Build

```bash

# Fork and clone the pebblo repo
git clone https://github.com/<your-github-userid>/pebblo.git
cd pebblo

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Build pebblo python package
pip3 install build
python3 -m build --wheel
```

Build artifact as wheel package will be available in `dist/pebblo-<version>-py3-none-any.whl`.

### Install

```bash
pip3 install dist/pebblo-<version>-py3-none-any.whl
```

Pebblo script will the install as `.venv/bin/pebblo`

### Run Pebblo Daemon

```bash
pebblo
```

Pebblo daemon now listens to `localhost:8000` to accept Gen-AI application document snippets for inspection and reporting.


## Code Formatting

Run these locally before submitting a PR; the CI system will check also.

Formatting for this project is done via [ruff](https://docs.astral.sh/ruff/).

To run formatting for the entire project, run the following command from the root directory of the project:

```bash
make format
```

Additionally, you can run the formatter only on the files that have been modified in your current branch as compared to the main branch using the format_diff command:

```bash
make format_diff
```

This is especially useful when you have made changes to a subset of the project and want to ensure your changes are properly formatted without affecting the rest of the codebase.


## Creating a pull request

See [these instructions](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork)
to open a pull request against the main Pebblo repo.

## Communication

Please join Discord server https://discord.gg/wyAfaYXwwv to reach out to the Pebblo maintainers, contributors and users.
