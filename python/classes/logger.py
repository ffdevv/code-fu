import logging
from typing import Callable

# Define a type alias for the log hook function
# level, message -> None
LogHookFunction =  Callable[[int, str], None]

class Logger:
  """A logger class that provides logging functionality to a Python program.

  Attributes:
    logger (logging.Logger): The logging object that provides the logging functionality.
    _log_hook (Optional[LogHookFunction]): Optional hook function to execute before logging.

  Methods:
    __init__(name: str, level: int = logging.INFO, log_hook: Optional[LogHookFunction] = None):
      Initializes a new Logger object.
      name (str): The name of the logger.
      level (int): The logging level. The default value is logging.INFO.
      log_hook (Optional[LogHookFunction]): Optional hook function to execute before logging.
    log(level: int, message: str): Logs a message at the specified logging level.
      level (int): The logging level of the message.
      message (str): The message to be logged.
    debug(message: str): Logs a message at the DEBUG level.
      message (str): The message to be logged.
    info(message: str): Logs a message at the INFO level.
      message (str): The message to be logged.
    warning(message: str): Logs a message at the WARNING level.
      message (str): The message to be logged.
    error(message: str): Logs a message at the ERROR level.
      message (str): The message to be logged.
    critical(message: str): Logs a message at the CRITICAL level.
      message (str): The message to be logged.
  """

  def __init__(self, name: str, level: int = logging.INFO, log_hook: Optional[LogHookFunction] = None):
    """Initializes a new Logger object.

    Args:
      name (str): The name of the logger.
      level (int, optional): The logging level. The default value is logging.INFO.
    """
    self.logger = logging.getLogger(name)
    self.logger.setLevel(level)
    self._log_hook = log_hook

    # Add a console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # Create a formatter and add it to the console handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Add the console handler to the logger
    self.logger.addHandler(ch)

  def log(self, level: int, message: str):
    """Logs a message at the specified logging level.

    Args:
      level (int): The logging level of the message.
      message (str): The message to be logged.
    """
    if not self._log_hook is None:
      self._log_hook(level, message)

    self.logger.log(level, message)

  def debug(self, message: str):
    """Logs a message at the DEBUG level.

    Args:
      message (str): The message to be logged.
    """
    self.logger.log(logging.DEBUG, message)

  def info(self, message: str):
    """Logs a message at the INFO level.

    Args:
      message (str): The message to be logged.
    """
    self.logger.log(logging.INFO, message)

  def warning(self, message: str):
    """Logs a message at the WARNING level.

    Args:
      message (str): The message to be logged.
    """
    self.logger.log(logging.WARNING, message)

  def error(self, message: str):
    """Logs a message at the ERROR level.

    Args:
      message (str): The message to be logged.
    """
    self.logger.log(logging.ERROR, message)

  def critical(self, message: str):
    """Logs a message at the CRITICAL level.

    Args:
      message (str): The message to be logged.
    """
    self.logger.log(logging.CRITICAL, message)
