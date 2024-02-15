# Pebblo Configuration File

### Introduction

This configuration file specifies settings for various components of the Pebblo application.

### Configuration Details

#### Daemon

- `port`: Specifies the port number on which the Pebblo daemon listens for incoming connections.
- `host`: Specifies the host address on which the Pebblo daemon is running.

### Logging

- `level`: Sets the logging level for the Pebblo application. Possible values are 'info', 'debug', 'error', 'warning', and 'critical'.

### Reports

- `format`: Specifies the format of generated reports. Available options include 'pdf', 'html', etc.
- `renderer`: Specifies the rendering engine for generating reports.
- `outputDir`: Defines the directory where generated reports will be saved.

### Configuration Example

```commandline
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

### Validation

- The Pebblo application validates the configuration file upon startup.
- If the configuration file contains errors or invalid values, Pebblo will log appropriate error messages and may use default values for parameters.
