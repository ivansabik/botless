import os
from datetime import datetime

import requests

from botless.exceptions import MissingParam


class DataTarget():
    def __init__(self, **kwargs):
        self.env_vars = kwargs.get('env_vars', [])
        self.name = kwargs.get('name')

        if not self.name:
            if not kwargs.get('name'):
                raise NotImplementedError('name attribute is required for all data targets')
        else:
            self.name = kwargs.get('name')

        # Validate all env_vars specified exist as environment variables
        for env_var in self.env_vars:
            if not os.getenv(env_var):
                raise MissingParam('{} is required'.format(env_var))
            else:
                setattr(self, env_var, os.getenv(env_var))


# DataTarget definitions/implementations

class SlackDataTarget(DataTarget):
    SLACK_POST_MESSAGE_URL = 'http://slack.com/api/chat.postMessage'

    def __init__(self):
        self.since = datetime(datetime.now().year, 1, 1).strftime('%Y-%m-%d')
        self.until = datetime.now().strftime('%Y-%m-%d')
        DataTarget.__init__(self, name='slack', env_vars=['SLACK_API_TOKEN'])

    def post_message(self, channel=None, text=None):
        params = {
            'token': self.SLACK_API_TOKEN,
            'channel': channel,
            'text': text
        }
        response = requests.post(self.SLACK_POST_MESSAGE_URL, params=params)
        response.raise_for_status()

        return response.json()
