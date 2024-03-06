# Pebblo Configuration File

### Introduction

This configuration file specifies settings for various components of the Pebblo.

### Configuration Details

#### Server

- `port`: Specifies the port number on which the Pebblo server listens for incoming connections.
- `host`: Specifies the host address on which the Pebblo server to run.

Notes:
1. By default `Pebblo Server` runs at `localhost:8000`. When we change values of `port` and/or `host` , the `Pebblo Safe DataLoader` env variable `PEBBLO_CLASSIFIER_URL` needs to set to the correct URL.
2. By default `Pebblo UI` runs at `localhost:8000/pebblo`. When we change values of `port` and/or `host`, the Pebblo UI would be running on the respective `host:port/pebblo`.

### Logging

- `level`: Sets the logging level for the Pebblo application. Possible values are 'info', 'debug', 'error', 'warning', and 'critical'.

### Reports

- `format`: Specifies the format of generated reports. Available options include 'pdf'.
- `renderer`: Specifies the rendering engine for generating reports. Options include 'weasyprint', 'xhtml2pdf'.
- `outputDir`: Defines the directory where generated reports will be saved.

### Classifier

- `anonymize_all_entities`: Condition to anonymize all entities in document.

### Default Configuration

```yaml
daemon:
  port: 8000
  host: localhost
logging:
  level: info
reports:
  format: pdf
  renderer: xhtml2pdf
  outputDir: ~/.pebblo
classifier:
  anonymize_all_entities: true
```
