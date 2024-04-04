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
        URL = 'https://api.telegram.org/bot'
        TOKEN = settings.BOT_TOKEN
        weekdays_in_int = {1: 'periodicity__on_Monday', 2: 'on_Tuesday', 3: 'on_Wednesday', 4: 'on_Thursday',
                           5: 'on_Friday',
                           6: 'on_Saturday', 7: 'on_Sunday'}

        time_now = datetime.now().time().replace(second=0, microsecond=0)
        date_now = date.today()

        today = datetime.today()
        day_of_week = today.weekday()
        # надо получить список дней недели как словарь дэй оф вик выдает интовое значение
        #

        addictions = Addiction.objects.all()

        for addiction in addictions:
            if day_of_week in addiction.periodicity.int_weeks:
                text = (f'{addiction.proprietor.name}, время для привычки {addiction.activity_name} в'
                        f' {addiction.location}, вас ждет ')
                if addiction.nice_addiction:
                    text += f'приятное занятие {addiction.nice_addiction.activity_name}'
                else:
                    text += f'приз {addiction.prize}'
                print(text)
                print(addiction.proprietor.chat_id, 'должен быть айди')
                requests.get(f'{URL}{TOKEN}/sendMessage?chat_id={addiction.proprietor.chat_id}&text={text}')
                requests.post(
                    url=f"{URL}{TOKEN}/sendMessage",
                    data={
                        "chat_id": addiction.proprietor.chat_id,
                        "text": text
                    }
                )






        # API_URL = 'https://api.telegram.org/bot'
        # BOT_TOKEN = '6908027614:AAHCULVVrZBd7zKKK_2A9_weqXgY7rcR8to'
        # TEXT = 'Ура! Классный апдейт!'
        # MAX_COUNTER = 100
        #
        # offset = -2
        # counter = 0
        # chat_id: int
        #
        # while counter < MAX_COUNTER:
        #
        #     print('attempt =', counter)  # Чтобы видеть в консоли, что код живет
        #
        #     updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()
        #
        #     if updates['result']:
        #         for result in updates['result']:
        #             offset = result['update_id']
        #             chat_id = result['message']['from']['id']
        #             requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={TEXT}')
        #
        #     time.sleep(1)
        #     counter += 1
        # from datetime import datetime
        #
        # today = datetime.today()
        # day_of_week = today.weekday()
        #
        #
        # addictions = Addiction.objects.all()
        #
        # for addiction in addictions:
        #     if day_of_week in addiction.periodicity.int_weeks:
        #         text = (f'{addiction.proprietor.name}, время для привычки {addiction.activity_name} в'
        #                 f' {addiction.location}, вас ждет ')
        #         if addiction.nice_addiction:
        #             text += f'приятное занятие {addiction.nice_addiction.activity_name}'
        #         else:
        #             text += f'приз {addiction.prize}'
        #         print(text)


