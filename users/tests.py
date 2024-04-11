from django.test import TestCase
import unittest
from unittest.mock import patch

from rest_framework import status

from config import settings
from tracker.models import Addiction, Periodicity
from datetime import datetime, timedelta

from users.models import User
from users.tasks import reminder
from rest_framework.test import APITestCase, force_authenticate


# Create your tests here.


class ReminderTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email='test@test.test', chat_id=1305224364)
        self.client.force_authenticate(user=self.user)

        self.periodicity = Periodicity.objects.create(
            on_Monday=True,
            on_Tuesday=False,
            on_Wednesday=True,
            on_Thursday=True,
            on_Friday=True,
            on_Saturday=True,
            on_Sunday=True
        )
        self.addiction = Addiction.objects.create(
            location="Тестовый Каэр",
            time="17.00",
            activity_name="Готовить самогон",
            prize="Кружка самогона",
            run_time="60",
            is_public=True,
            periodicity=self.periodicity,
            proprietor=self.user

        )

    def test_reminder(self):
        res = reminder()
        self.assertEqual(res, False)

