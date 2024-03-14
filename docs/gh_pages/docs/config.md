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

- `anonymizeSnippets`: Flag to anonymize snippet in report.

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
  anonymizeSnippets: false
```

`Note`:
Users have the option to maintain any section or even a single field within a section. For instance, the `config` file might appear as follows:

```yaml
logging:
  level: info
```
This flexibility empowers users to tailor configurations to their specific needs while retaining default values for other sections or fields.