# Pebblo

## Build

```sh
git clone https://github.com/daxa-ai/pebblo.git
pip3 install build
python3 -m build --wheel
```

Build artifact as wheel package will be available in `dist/pebblo-<version>-py3-none-any.whl`. See the instruction below on how to install.

## Installation

### Pre-requisites

#### Mac OSX

```sh
brew install pango
```

#### Linux (debian/ubuntu)

```sh
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0
```

### Pebblo Daemon

### From wheel distribution
```sh
# copy wheel pkg pebblo-<version>-py3-none-any.whl from the build location to the target machine / location
pip install pebblo-<version>-py3-none-any.whl
```

### From TestPyPi

```sh
pip install -i https://test.pypi.org/simple/ pebblo
```

Note: above step will install a runnable python script named `pebblo`


## Run Pebblo daemon

```sh
pebblo
```