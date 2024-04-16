from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

"""
Настройки celery.py
"""

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')
print(app)

app.autodiscover_tasks()
# Load task modules from all registered Django apps.

app.autodiscover_tasks()
