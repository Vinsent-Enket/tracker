from datetime import datetime, date, timedelta

import requests
from celery import shared_task
from django.conf import settings

from tracker.models import Addiction


@shared_task
def reminder():
    """
    Отправка пользователю в Телеграм напоминания о привычке
    """

    URL = 'https://api.telegram.org/bot'
    TOKEN = settings.BOT_TOKEN
    weekdays_in_int = {1: 'periodicity__on_Monday', 2: 'on_Tuesday', 3: 'on_Wednesday', 4: 'on_Thursday', 5: 'on_Friday',
                       6: 'on_Saturday', 7: 'on_Sunday'}

    time_now = datetime.now().time().replace(second=0, microsecond=0)
    date_now = date.today()

    today = datetime.today()
    day_of_week = today.weekday()

    addictions = Addiction.objects.all()
    for addiction in addictions:
        if day_of_week in addiction.periodicity.int_weeks:
            text = (f'{addiction.proprietor.name},сегодня время для привычки {addiction.activity_name} в {addiction.time}'
                    f' в месте {addiction.location}, вас ждет ')
            if addiction.nice_addiction:
                text += f'приятное занятие {addiction.nice_addiction.activity_name}'
            else:
                text += f'приз {addiction.prize}'
            requests.post(
                url=f"{URL}{TOKEN}/sendMessage",
                data={
                    "chat_id": addiction.proprietor.chat_id,
                    "text": text
                }
            )



