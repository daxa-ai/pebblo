# Installation

> **Note**  
> Please note that Pebblo requires Python version 3.9 or above to function optimally.

### Pre-requisites

#### Mac OSX

```
brew install pango
```

#### Linux (debian/ubuntu)

```
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0
```

### Pebblo Server

```
pip install pebblo
```

# Run Pebblo server

```
pebblo
```

Pebblo server now listens to `localhost:8000` to accept Gen-AI application data snippets for inspection and reporting. 
Pebblo UI interface would be available on `http://localhost:8000/pebblo`

see [troubeshooting](troubleshooting.md) if you face any issues.

#### Pebblo Optional Flags

- `--config <file>`: Specifies a custom configuration file in yaml format.

```bash
pebblo --config [PATH TO CONFIG FILE]
```
