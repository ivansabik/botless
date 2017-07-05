import os
import time
from datetime import datetime

import requests

from botless.exceptions import MissingParam


class DataSource():
    def __init__(self, **kwargs):
        self.env_vars = kwargs.get('env_vars', [])
        self.name = kwargs.get('name')

        if not self.name:
            if not kwargs.get('name'):
                raise NotImplementedError('name attribute is required for all data sources')
        else:
            self.name = kwargs.get('name')

        # Validate all env_vars specified exist as environment variables
        for env_var in self.env_vars:
            if not os.getenv(env_var):
                raise MissingParam('{} is required'.format(env_var))
            else:
                setattr(self, env_var, os.getenv(env_var))


# DataSource definitions/implementations

class TogglDataSource(DataSource):
    TOGGL_REPORTS_DETAILS_URL = 'https://toggl.com/reports/api/v2/details'

    def __init__(self):
        self.since = datetime(datetime.now().year, 1, 1).strftime('%Y-%m-%d')
        self.until = datetime.now().strftime('%Y-%m-%d')
        DataSource.__init__(self, name='toggl', env_vars=['TOGGL_API_KEY', 'TOGGL_WORKSPACE_ID'])

    def get_detailed_report(self, since=None, until=None, user_ids=None, billable='both'):
        """
        Example of an entry:
        {
            "id": 100,
            "pid": 200,
            "tid": null,
            "uid": 300,
            "description": "Work on stuff",
            "start": "2017-07-03T23:09:57+02:00",
            "end": "2017-07-03T23:22:59+02:00",
            "updated": "2017-07-03T23:23:01+02:00",
            "dur": 782000,
            "user": "Fred",
            "use_stop": true,
            "client": null,
            "project": "Project Name",
            "project_color": "0",
            "project_hex_color": "#1502e3",
            "task": null,
            "billable": 0,
            "is_billable": false,
            "cur": "USD",
            "tags": []
        }
        """
        if since:
            self.since = since
        if until:
            self.until = until
        self.user_ids = user_ids
        self.billable = billable

        fetched_records = 0
        to_fetch_records = 50
        page = 1
        entries = []

        while fetched_records < to_fetch_records:
            print('Fetching from Toggl {} of {}'.format(fetched_records, to_fetch_records))
            # There is rate limiting of 1 request per second (per IP per API token) so sleeping to make sure
            time.sleep(1)
            params = {
                'workspace_id': self.TOGGL_WORKSPACE_ID,
                'since': self.since,
                'until': self.until,
                'user_agent': 'botless',
                'user_ids': user_ids,
                'page': page,
                'billable': billable
            }
            response = requests.get(self.TOGGL_REPORTS_DETAILS_URL, auth=(self.TOGGL_API_KEY, 'api_token'), params=params)
            response.raise_for_status()

            response_dict = response.json()

            for entry in response_dict['data']:
                entries.append(entry)
            fetched_records += len(response_dict['data'])
            to_fetch_records = response_dict['total_count'] - fetched_records
            page += 1

        return entries
