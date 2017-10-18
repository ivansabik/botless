import datetime

import requests

from botless.models import AppIntegration

SLACK_POST_MESSAGE_URL = 'http://slack.com/api/chat.postMessage'


class Slack(AppIntegration):
    """
    Currently using legacy tokens: https://api.slack.com/custom-integrations/legacy-tokens
    """
    config_vars = ['SLACK_API_TOKEN']
    name = 'slack'

    def __init__(self):
        self.since = datetime.datetime(datetime.datetime.now().year, 1, 1).strftime('%Y-%m-%d')
        self.until = datetime.datetime.now().strftime('%Y-%m-%d')
        AppIntegration.__init__(self)

    def post_message(self, channel=None, text=None):
        """
        Example successful response:
        {
            "ok": true,
            "channel": "CHANNELID",
            "ts": "1499232812.825733",
            "message": {
              "text": "This is botless",
              "username": "Slack API Tester",
              "bot_id": "BOTID",
              "type": "message",
              "subtype": "bot_message",
              "ts": "1499232812.825733"
            }
        }
        """
        params = {
            'token': self.SLACK_API_TOKEN,
            'channel': channel,
            'text': text
        }
        response = requests.post(SLACK_POST_MESSAGE_URL, params=params)
        response.raise_for_status()
        response_dict = response.json()
        # Slack is not giving the HTTP for failure but instead
        # {u'ok': False, u'error': u'invalid_auth'}
        if 'error' in response_dict:
            raise Exception(response_dict.get('error'))
        else:
            return response_dict
