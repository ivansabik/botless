import argparse

from botless.bots.toggl_less_than_min_hours_to_slack import TogglLessThanMinHoursToSlack


# TODO: make somehow more dynamic
POSSIBLE_ARGS = ['start_date', 'frequency', 'min_hours', 'channel']


def run_bot(**kwargs):
    TogglLessThanMinHoursToSlack().run(**kwargs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for possible_arg in POSSIBLE_ARGS:
        parser.add_argument('--' + possible_arg)
    args = parser.parse_args()
    for _, key in enumerate(args.__dict__.copy()):
        if args.__dict__[key] is None:
            delattr(args, key)
    run_bot(**vars(args))
