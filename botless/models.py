import os

from botless.exceptions import MissingParam


def get_config_var(name):
    try:
        import dotenv
    except ImportError:
        pass  # Using .venv file is optional, if not available environment vars can be used
    else:
        # Load environment variables from .env file for local development or usage
        dotenv.load_dotenv(dotenv.find_dotenv())
    return os.getenv(name)


class AppIntegration:
    actions = None
    triggers = None

    def __init__(self, **kwargs):
        self.config_vars = kwargs.get('config_vars', [])
        self.name = kwargs.get('name')

        if not self.name:
            if not kwargs.get('name'):
                raise NotImplementedError('name attribute is required for all data sources')
        else:
            self.name = kwargs.get('name')

        # Validate all config_vars specified exist as environment variables
        for config_var in self.config_vars:
            if not os.getenv(config_var):
                raise MissingParam('{} is required'.format(config_var))
            else:
                setattr(self, config_var, os.getenv(config_var))


class Bot:
    name = None
    repetitions = None
    periodicity = None
    start_time = None
    input_vars = {}
    trigger = None
    steps = 2  # By default intended for simple 1 Data Source to 1 Data Target flows

    def run(self):
        # Start time, end time, log and save
        pass
