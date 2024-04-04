from django.contrib.auth.models import AbstractUser
from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


# Create your models here.

class User(AbstractUser):
    """Модель пользователя"""
    username = None
    email = models.EmailField(unique=True, verbose_name='Личная почта')
    name = models.CharField(max_length=30, verbose_name='Имя пользователя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия пользователя')
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    chat_id = models.IntegerField(verbose_name='ID чата в телеграмм', **NULLABLE)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
