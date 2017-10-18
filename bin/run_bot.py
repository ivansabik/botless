from botless.bots.toggl_less_than_min_hours_to_slack import TogglLessThanMinHoursToSlack


def run_bot():
    TogglLessThanMinHoursToSlack().run()


if __name__ == '__main__':
    run_bot()
