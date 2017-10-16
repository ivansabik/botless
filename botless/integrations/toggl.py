import datetime
import time

import requests

from botless.models import AppIntegration

TOGGL_REPORTS_DETAILS_URL = 'https://toggl.com/reports/api/v2/details'


class Toggl(AppIntegration):
    def __init__(self):
        self.since = datetime(datetime.now().year, 1, 1).strftime('%Y-%m-%d')
        self.until = datetime.now().strftime('%Y-%m-%d')
        AppIntegration.__init__(self, name='toggl', config_vars=['TOGGL_API_KEY', 'TOGGL_WORKSPACE_ID'])

    def get_detailed_report(self, since=None, until=None, user_ids=None, billable='both'):
        """
        Example successful response:
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
