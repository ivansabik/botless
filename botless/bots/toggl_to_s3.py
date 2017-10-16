from botless.integrations import S3, Toggl
from botless.models import Bot


class TogglToS3(Bot):
    input_vars = {
        'filters': ''
    }

    def run(self):
        pass
