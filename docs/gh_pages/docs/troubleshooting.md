# Troubleshooting Guide

## Issues found while running pebblo server, in conda virtual env.
### 1. OSError: cannot load library 'pango-1.0-0'
  Install pango package in conda env

  `conda install -c anaconda pango`

### 2. OSError: cannot load library 'gobject-2.0-0': gobject-2.0-0: cannot open shared object file
  Install libpango binaries

  ```bash
  sudo apt-get update
  sudo apt-get install libpango1.0-0
  ```

<img referrerpolicy="no-referrer-when-downgrade" src="https://static.scarf.sh/a.png?x-pxid=4f6e05d7-1d73-45dc-abc9-244ee4d905ff" />
