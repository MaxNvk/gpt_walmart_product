import logging

def configure_logging():
    logging.basicConfig(level=logging.INFO)  # Set to DEBUG for more verbosity
    logger = logging.getLogger(__name__)
    return logger