# Troubleshooting Pebblo

## Issued found in conds virtual env.
### OSError: cannot load library 'pango-1.0-0'
#### Sol
  Install pango package in conda env

  `conda install -c anaconda pango`
### OSError: cannot load library 'gobject-2.0-0': gobject-2.0-0: cannot open shared object file
  Install libpango binaries
  ```bash
  sudo apt-get update
  sudo apt-get install libpango1.0-0
  ```
