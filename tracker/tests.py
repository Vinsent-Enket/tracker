from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, force_authenticate
from rest_framework import status

from tracker.models import Addiction, Periodicity
from users.models import User

# Create your tests here.
data = {
    "location": "Каэр МоргенШтерн",
    "time": "18.00",
    "activity_name": "Готовить зелье из накера",
    "nice_addiction_data": {
        "location": "Каэр морхен",
        "time": "20.00",
        "activity_name": "Подшутить над дядькой Весемиром"

    },
    "periodicity": {
        "on_Monday": False,
        "on_Tuesday": False,
        "on_Wednesday": True,
        "on_Thursday": True,
        "on_Friday": False,
        "on_Saturday": False,
        "on_Sunday": True
    },
    "prize": "Кружка пива",
    "run_time": "300",
    "is_public": True

}


class AddictionViewSetTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email='test@test.test')
        self.client.force_authenticate(user=self.user)

        self.periodicity = Periodicity.objects.create(
            on_Monday=False,
            on_Tuesday=False,
            on_Wednesday=True,
            on_Thursday=True,
            on_Friday=False,
            on_Saturday=False,
            on_Sunday=True
        )
        self.addiction = Addiction.objects.create(
            location="Тестовый Каэр",
            time="18.00",
            activity_name="Готовить самогон",
            prize="Кружка самогона",
            run_time="60",
            is_public=True,
            periodicity=self.periodicity,
            proprietor=self.user

        )

    def test_index_view(self):
        response = self.client.get(reverse('tracker:index'))
        self.assertEqual(response.status_code, 200)

    def test_addiction_viewset_list(self):
        response = self.client.get('http://127.0.0.1:8000/addict/')  # проблема с реверсе,
        # 'tracker:addict' не работает
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_addiction_viewset_create(self):
        data = {
            "location": "Каэр МоргенШтерн",
            "time": "18.00",
            "activity_name": "Готовить зелье из накера",
            "nice_addiction_data": {
                "location": "Каэр морхен",
                "time": "20.00",
                "activity_name": "Подшутить над дядькой Весемиром"

            },
            "periodicity": {
                "on_Monday": False,
                "on_Tuesday": False,
                "on_Wednesday": True,
                "on_Thursday": True,
                "on_Friday": False,
                "on_Saturday": False,
                "on_Sunday": True
            },

            "run_time": "60",
            "is_public": True

        }
        response = self.client.post('http://127.0.0.1:8000/addict/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data['prize'] = 'Кружка пива'
        response = self.client.post('http://127.0.0.1:8000/addict/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['run_time'] = 300
        response = self.client.post('http://127.0.0.1:8000/addict/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_addiction_viewset_retrieve(self):
        response = self.client.get(f'http://127.0.0.1:8000/addict/{self.addiction.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_addiction_viewset_update(self):
        data = {
            "location": "Каэр МоргенШтерн",
            "time": "18.00",
            "activity_name": "Готовить зелье из накера",
            "periodicity": {
                "on_Monday": False,
                "on_Tuesday": False,
                "on_Wednesday": True,
                "on_Thursday": False,
                "on_Friday": False,
                "on_Saturday": False,
                "on_Sunday": True
            },
            "prize": "Кружка пива",
            "run_time": "80",
            "is_public": True

        }

        response = self.client.put(f'http://127.0.0.1:8000/addict/{self.addiction.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_addiction_viewset_partial_update(self):
        data = {
            "location": "Каэр МоргенШтерн",
            "time": "18.00",
            "activity_name": "Готовить зелье из накера",
            "periodicity": {
                "on_Monday": False,
                "on_Tuesday": False,
                "on_Wednesday": True,
                "on_Thursday": False,
                "on_Friday": False,
                "on_Saturday": False,
                "on_Sunday": True
            },
            "prize": "Кружка пива",
            "run_time": "80",
            "is_public": False

        }
        response = self.client.patch(f'http://127.0.0.1:8000/addict/{self.addiction.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_addiction_viewset_destroy(self):
        response = self.client.delete(f'http://127.0.0.1:8000/addict/{self.addiction.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_periodicity_update(self):
        data = {
            "periodicity_id": self.addiction.periodicity.id,
            "on_Monday": True,
            "on_Tuesday": True,
            "on_Wednesday": True,
            "on_Thursday": True,
            "on_Friday": True,
            "on_Saturday": True,
            "on_Sunday": True

        }
        response = self.client.put(reverse('tracker:periodicity'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
