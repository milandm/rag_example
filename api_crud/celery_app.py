from __future__ import absolute_import
import os, sys
from celery import Celery
from django.conf import settings
import django

#django.setup()

import logging

logger = logging.getLogger(__name__)


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_crud.settings')
app = Celery('api_crud')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
#app.autodiscover_tasks()
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.update(
        broker_transport_options={"confirm_publish": True},
    )

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
