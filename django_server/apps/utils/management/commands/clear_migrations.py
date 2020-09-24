import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import os


class Command(BaseCommand):
    help = 'clear_migrations'

    def handle(self, *args, **options):
        apps_floder = os.path.join(settings.BASE_DIR, 'apps')
        floders = [_ for _ in os.listdir(apps_floder) if '.' not in _]
        types = ['auto', 'initial']
        for floder in floders:
            if not os.path.exists(os.path.join(apps_floder, floder, 'migrations')):
                continue
            files = os.listdir(os.path.join(apps_floder, floder, 'migrations'))
            all_files = [os.remove(os.path.join(apps_floder, floder, 'migrations', name))
                         for _ in types for name in files if _ in name and os.path.exists(os.path.join(apps_floder, floder, 'migrations', name))]
        # return super().handle(*args, **options)
