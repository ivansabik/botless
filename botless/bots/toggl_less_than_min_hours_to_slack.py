import calendar
import datetime
import unidecode

from botless.integrations.slack import Slack
from botless.integrations.toggl import Toggl
from botless.models import Bot


class TogglLessThanMinHoursToSlack(Bot):
    """
    Gets users in Toggl that have registered less than X hours for a given time
    period (week, month, year, etc). Then it notifies in a slack channel with the
    users that have less than the X hours specified.
    """
    user_ids = None

    def run(self, start_date=None, frequency='week', min_hours=37):
        """
        @param start_date: String with a date YYYYMMDD to be used for the check.
                           Defaults to last week since this bot is intended to run on Monday.
        @param frequency: String with the date range interval frequency (week, month, year are currently supported).
        @param min_hours: Int with the minimum hours required, if a user has less
                          than this hours in Toggle they will be included in the
                          Slack notification.
        """
        today_last_week = datetime.datetime.today() - datetime.timedelta(weeks=1)
        if frequency == 'week':
            if not start_date:
                start_date = today_last_week - datetime.timedelta(days=(datetime.datetime.today().isoweekday() - 1) % 7)
            end_date = start_date + datetime.timedelta(days=6)
        elif frequency == 'month':
            if not start_date:
                start_date = datetime.datetime(today_last_week.year, today_last_week.month, 1)
            last_day_of_month = calendar.monthrange(today_last_week.year, today_last_week.month)[1]
            end_date = datetime.datetime(today_last_week.year, today_last_week.month, last_day_of_month)
        if frequency == 'year':
            if not start_date:
                start_date = datetime.datetime(today_last_week.year, 1, 1)
            end_date = datetime.datetime(today_last_week.year, 12, 31)
        toggl = Toggl()
        print('Getting detailed report from Toggl from {} until {}'.format(start_date, end_date))
        details_df = toggl.get_detailed_report(
            since=start_date.strftime('%Y-%m-%d'),
            until=end_date.strftime('%Y-%m-%d'),
            user_ids=self.user_ids,
            as_df=True
        )
        if details_df.empty:
            # TODO: Log no results were found
            print('No results from Toggl')
            return
        details_df = details_df.fillna({'client': 'No Client', 'project': 'No Project', 'task': 'No Task'})
        details_df['durationHours'] = details_df['dur'] / (1000 * 60 * 60)
        summary_df = details_df.pivot_table(index=['user'], values=['durationHours'], aggfunc='sum').reset_index()
        summary_df = summary_df[summary_df.durationHours < min_hours]
        summary_df['durationHours'] = summary_df['durationHours'].round(2)
        summary_df['user'] = summary_df['user'].map(lambda x: unidecode.unidecode(x))
        summary_df = summary_df.sort_values(by='durationHours', ascending=True)

        # Post to slack
        slack = Slack()
        base_message = 'The following users have registered less than {0} hours from {1} to {2}:\n{3}'
        message = base_message.format(
            min_hours,
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d'),
            summary_df.to_string(index=False, header=False, justify='left')
        )
        slack.post_message(channel='ops_managers_bots', text=message)
