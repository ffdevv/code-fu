# pip install python-dotenv
from dotenv import dotenv_values
import json

_MANDATORY_NO_DEFAULT = Ellipsis

class Config:
  """Represents a configuration for a program.

  The Config class provides a way to store and access configuration options
  for a program. The configuration options are loaded from a file, which can
  be either a .env file or a JSON file.

  Attributes:
      DEFAULTS (dict): A dictionary that contains the default values for
          the configuration options.
      
  Methods:
      __init__(filepath: str = '.env'): Initializes a new Config object.
          filepath (str): The path to the file containing the configuration
              values. If the file is a .env file, the values are loaded using
              the dotenv_values function from the dotenv module. If the file
              is a JSON file, the values are loaded using the json.load
              function. If no filepath is provided, the default value is
              '.env'.
  """

  # Define the default values for the configuration options
  DEFAULTS = {
    "dbHost": _MANDATORY_NO_DEFAULT,
    "dbPort": _MANDATORY_NO_DEFAULT,
    "dbUsername": _MANDATORY_NO_DEFAULT,
    "dbPassword": _MANDATORY_NO_DEFAULT
  }

  def __init__(self, filepath: str = '.env'):
    # Check if the provided filepath is a .env or .json file, and load the values accordingly
    if filepath.endswith('.env'):
      values = dotenv_values(filepath)
    elif filepath.endswith('.json'):
      with open(filepath, 'r', encoding='utf8') as fi:
        values = json.load(fi)
    else:
      raise TypeError("Unsupported filepath: provide a .env or .json file")

    # Set the configuration options for the object using the loaded values
    for k, v in self.DEFAULTS.items():
      v1 = values.get(k, v)
      if v1 == _MANDATORY_NO_DEFAULT:
        raise KeyError("config file missing mandatory field: " + k)
      setattr(self, k, v1)

  def __repr__(self):
    return f"Config<{self.__dict__}>"
