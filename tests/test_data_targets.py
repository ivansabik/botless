import pytest
import responses

from botless.data_targets import DataTarget, SlackDataTarget
from botless.exceptions import MissingParam


def test_data_target():
    with pytest.raises(NotImplementedError):
        DataTarget()
    with pytest.raises(MissingParam):
        DataTarget(name='test_data_target', env_vars=['var_one'])


@responses.activate
def test_slack(monkeypatch):
    monkeypatch.setenv('SLACK_API_TOKEN', 'fake-token-for-slack')

    mock_response = {
        'ok': True,
        'channel': 'CHANNELID',
        'ts': '1499232812.825733',
        'message': {
            'text': 'This is botless',
            'username': 'Slack API Tester',
            'bot_id': 'BOTID',
            'type': 'message',
            'subtype': 'bot_message',
            'ts': '1499232812.825733'
        }
    }
    responses.add(responses.POST, SlackDataTarget.SLACK_POST_MESSAGE_URL, json=mock_response, status=200)

    slack = SlackDataTarget()
    assert slack.SLACK_API_TOKEN == 'fake-token-for-slack'
    response = slack.post_message(channel='afr_bc', text='This is botless')

    assert response['ok'] is True
    assert response['channel'] == 'CHANNELID'
    assert response['ts'] == '1499232812.825733'
    assert response['message']['text'] == 'This is botless'
    assert response['message']['username'] == 'Slack API Tester'
    assert response['message']['bot_id'] == 'BOTID'
    assert response['message']['type'] == 'message'
    assert response['message']['subtype'] == 'bot_message'
    assert response['message']['ts'] == '1499232812.825733'
