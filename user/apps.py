import sys
from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user"

    def ready(self):
        if 'celery' in sys.argv and 'beat' in sys.argv:
            import user.signals  # noqa
