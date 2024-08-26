from pebblo.app.config.config import (
    ClassifierConfig,
    Config,
    LoggingConfig,
    PortConfig,
    ReportConfig,
    StorageConfig,
    var_server_config,
)

# Initialize global server config with default values
config = Config(
    daemon=PortConfig(host="localhost", port=8000),
    logging=LoggingConfig(),
    reports=ReportConfig(format="pdf", renderer="xhtml2pdf", cacheDir="~/.pebblo"),
    classifier=ClassifierConfig(anonymizeSnippets=False),
    storage=StorageConfig(type="db"),
)
var_server_config.set(config)
