from pebblo.app.config.config import Config, PortConfig, LoggingConfig, ReportConfig, ClassifierConfig, var_server_config

# Initialize global server config with default values
config = Config(
    daemon=PortConfig(host="localhost", port=8000),
    logging=LoggingConfig(),
    reports=ReportConfig(format="pdf", renderer="xhtml2pdf", outputDir="~/.pebblo"),
    classifier=ClassifierConfig(anonymizeSnippets=False)
)
var_server_config.set(config)