import requests
from django.core.management import BaseCommand
from celery import shared_task
import django
from django.utils import timezone
from datetime import timedelta, datetime, date

from config import settings
from tracker.models import Addiction
from users.models import User
import time
import json


class Command(BaseCommand):

    def handle(self, *args, **options):

        today = datetime.today()
        day_of_week = today.weekday()
        time_now = datetime.now().time()

        addictions = Addiction.objects.all()
        for addiction in addictions:
            if addiction.time.hour == time_now.hour:
                addiction_all_seconds = addiction.time.second + addiction.time.minute*60 + addiction.time.hour*3600
                now_all_seconds = time_now.second + time_now.minute * 60 + time_now.hour * 3600
                print(f'секунд в привычке - {addiction_all_seconds}, секунд сейчас - {now_all_seconds}')
                print(now_all_seconds-addiction_all_seconds)
