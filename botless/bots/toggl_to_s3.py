import datetime

import pandas as pd

from botless.integrations.s3 import S3
from botless.integrations.toggl import Toggl
from botless.models import Bot


class TogglToS3(Bot):
    """
    Creates one CSV with detailed info by month and one with summary by user
    """
    user_ids = None

    def run(self):
        toggl = Toggl()
        current_year, current_month = datetime.datetime.today().year, datetime.datetime.today().month
        start_date = '{}/1/1'.format(current_year)
        end_date = '{}/{}/1'.format(current_year, current_month + 1)
        dates_current_year = pd.date_range(start=start_date, end=end_date, freq='M')
        for date_cy in dates_current_year:
            start_month, start_year = date_cy.month, date_cy.year
            details_df = toggl.get_detailed_report(since='{}-{}-01'.format(start_year, str(start_month).zfill(2)), until=date_cy.strftime('%Y-%m-%d'), user_ids=self.user_ids, as_df=True)
            if details_df.empty:
                continue
            details_df = details_df.fillna({'client': 'No Client', 'project': 'No Project', 'task': 'No Task'})
            details_df['durationHours'] = details_df['dur'] / (1000 * 60 * 60)
            details_df = details_df.rename(columns={'billable': 'billableAmount'})
            summary_df = details_df.pivot_table(
                index=['user'],
                values=['billableAmount', 'durationHours'],
                aggfunc='sum'
            ).reset_index()
            summary_df['year'] = date_cy.year
            summary_df['month'] = date_cy.month
            details_df.to_csv('/tmp/{}_details.csv'.format(date_cy.strftime('%Y-%m')), index=False, encoding='utf-8')
            summary_df.to_csv('/tmp/{}_summary.csv'.format(date_cy.strftime('%Y-%m')), index=False, encoding='utf-8')
