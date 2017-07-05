from freezegun import freeze_time
import pytest
import responses

from botless.data_sources import DataSource, TogglDataSource
from botless.exceptions import MissingParam


def test_data_source():
    with pytest.raises(NotImplementedError):
        DataSource()
    with pytest.raises(MissingParam):
        DataSource(name='test_data_source', env_vars=['var_one'])


@freeze_time('2017-12-31')
def test_toggl_since_until_defaults(monkeypatch):
    monkeypatch.setenv('TOGGL_API_KEY', 'SECRET_API_KEY')
    monkeypatch.setenv('TOGGL_WORKSPACE_ID', '649573')

    toggl = TogglDataSource()

    assert toggl.since == '2017-01-01'
    assert toggl.until == '2017-12-31'


@responses.activate
def test_toggl(monkeypatch):
    monkeypatch.setenv('TOGGL_API_KEY', 'SECRET_API_KEY')
    monkeypatch.setenv('TOGGL_WORKSPACE_ID', '649573')

    mock_response = {
        'total_grand': 30149000,
        'total_billable': 0,
        'total_currencies': [
            {
                'currency': 'USD',
                'amount': 0
            }
        ],
        'total_count': 1,
        'per_page': 50,
        'data': [
            {
                'id': 632804082,
                'pid': 5860998,
                'tid': 10906376,
                'uid': 2879549,
                'description': 'Working hard',
                'start': '2017-07-03T08:05:49-05:00',
                'end': '2017-07-03T16:28:18-05:00',
                'updated': '2017-07-03T16:28:20-05:00',
                'dur': 30149000,
                'user': 'Luigi Brian',
                'use_stop': True,
                'client': None,
                'project': 'Support',
                'project_color': '0',
                'project_hex_color': '#c56bff',
                'task': 'VIT (Very Important Task)',
                'billable': 0,
                'is_billable': False,
                'cur': 'USD',
                'tags': [
                    'Laser Tag'
                ]
            }
        ]
    }
    responses.add(responses.GET, TogglDataSource.TOGGL_REPORTS_DETAILS_URL, json=mock_response, status=200)

    toggl = TogglDataSource()
    report = toggl.get_detailed_report(user_ids='2879549', since='2017-07-01', until='2017-07-04')

    assert report[0] == {
        'billable': 0.0,
        'client': None,
        'cur': 'USD',
        'description': 'Working hard',
        'dur': 30149000,
        'end': '2017-07-03T16:28:18-05:00',
        'id': 632804082,
        'is_billable': False,
        'pid': 5860998,
        'project': 'Support',
        'project_color': '0',
        'project_hex_color': '#c56bff',
        'start': '2017-07-03T08:05:49-05:00',
        'tags': ['Laser Tag'],
        'task': 'VIT (Very Important Task)',
        'tid': 10906376,
        'uid': 2879549,
        'updated': '2017-07-03T16:28:20-05:00',
        'use_stop': True,
        'user': 'Luigi Brian'
    }
