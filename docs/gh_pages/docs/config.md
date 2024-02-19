# Pebblo Configuration File

### Introduction

This configuration file specifies settings for various components of the Pebblo.

### Configuration Details

#### Daemon

- `port`: Specifies the port number on which the Pebblo daemon listens for incoming connections.
- `host`: Specifies the host address on which the Pebblo daemon to run.

Note: By default `Pebblo Daemon` runs at `localhost:8000`. When we changes values of `port` and/or `host` , the `Pebblo Safe DataLoader` env variable `PEBBLO_CLASSIFIER_URL` needs to set to the correct URL.

### Logging

- `level`: Sets the logging level for the Pebblo application. Possible values are 'info', 'debug', 'error', 'warning', and 'critical'.

### Reports

- `format`: Specifies the format of generated reports. Available options include 'pdf'.
- `renderer`: Specifies the rendering engine for generating reports.
- `outputDir`: Defines the directory where generated reports will be saved.

### Default Configuration

```yaml
daemon:
  port: 8000
  host: localhost
logging:
  level: info
reports:
  format: pdf
  renderer: weasyprint
  outputDir: ~/.pebblo

```