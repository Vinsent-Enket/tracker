from datetime import datetime, date, timedelta, time

import requests
from celery import shared_task
from django.conf import settings

from tracker.models import Addiction
from datetime import datetime


@shared_task
def reminder():
    """
    Отправка пользователю в Телеграм напоминания о привычке
    """
    URL = 'https://api.telegram.org/bot'
    TOKEN = settings.BOT_TOKEN  # данные для отправки сообщения

    today = datetime.today()
    day_of_week = today.weekday()  # сегодняшняя дата, день недели и время
    time_now = datetime.now().time()

    addictions = Addiction.objects.all()
    for addiction in addictions:
        if (day_of_week in addiction.periodicity.int_weeks) and (addiction.last_send < today.time()) and (
                addiction.time.hour == time_now.hour):  # проверка соответствия дня недели и времени и отправлялось ли сегодня
            timer = addiction.time.minute - time_now.minute

            text = (
                f'{addiction.proprietor.name},сегодня время для привычки {addiction.activity_name} в {addiction.time}'
                f' в месте {addiction.location}, осталось {timer} минут, вас ждет ')
            if addiction.nice_addiction:
                text += f'приятное занятие {addiction.nice_addiction.activity_name}'
            else:
                text += f'приз {addiction.prize}'
            response = requests.post(
                url=f"{URL}{TOKEN}/sendMessage",
                data={
                    "chat_id": addiction.proprietor.chat_id,
                    "text": text
                }
            )
            addiction.last_send = datetime.now().time()
            addiction.save()
            print(response)
            return response.status_code
        else:
            return False

