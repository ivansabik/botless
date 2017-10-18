import responses

from botless.integrations.slack import Slack, SLACK_POST_MESSAGE_URL


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
    responses.add(responses.POST, SLACK_POST_MESSAGE_URL, json=mock_response, status=200)

    slack = Slack()
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
