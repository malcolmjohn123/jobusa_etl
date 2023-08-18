import logging
import os

class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""
    
    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    reset = "\x1b[0m"
    fmt = "%(levelname)s - %(message)s"
    
    FORMATS = {
        logging.INFO: grey + fmt + reset,
        logging.WARNING: yellow + fmt + reset,
        logging.ERROR: red + fmt + reset,
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record with color coding based on log level.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log message.
        """
        log_fmt = self.FORMATS.get(record.levelno)
        if log_fmt:
            self._fmt = log_fmt
            self._style._fmt = log_fmt
        return super().format(record)


def get_logger(
    name: str,
    handler: logging.Handler = None,
    formatter: logging.Formatter = None,
    level: int = None,
) -> logging.Logger:
    """
    Initialize a logger with a custom formatter and specified settings.

    Args:
        name (str): Name of the logger.
        handler (logging.Handler, optional): Handler for the logger. Defaults to None.
        formatter (logging.Formatter, optional): Formatter for the logger. Defaults to None.
        level (int, optional): Logging level for the logger. Defaults to None.

    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger(name)
    if handler is None:
        handler = logging.StreamHandler()
    if formatter is None:
        formatter = CustomFormatter()
    for hdlr in logger.handlers:
        if isinstance(hdlr, logging.StreamHandler):
            hdlr.setFormatter(formatter)
            break
    else:  # nobreak
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level=level or (logging.DEBUG if os.environ.get("DEBUG") else logging.INFO))
    return logger
