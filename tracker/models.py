from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


# Create your models here.

class Periodicity(models.Model):
    """
    Модель для периодичности, выведена в отдельную модель так как при масштабировании проекта потребуется каждой
    модели добавлять поля для периодичности
    """
    on_Monday = models.BooleanField(verbose_name='В понедельник', default=False)
    on_Tuesday = models.BooleanField(verbose_name='Во вторник', default=False)
    on_Wednesday = models.BooleanField(verbose_name='В среду', default=False)
    on_Thursday = models.BooleanField(verbose_name='В четверг', default=False)
    on_Friday = models.BooleanField(verbose_name='В пятницу', default=False)
    on_Saturday = models.BooleanField(verbose_name='В субботу', default=False)
    on_Sunday = models.BooleanField(verbose_name='В воскресенье', default=False)

    @property
    def int_weeks(self):
        """
        Необходим для удобной работы с периодичностью в модуле отправки сообщений в телеграмм
        :return:
        """
        int_weeks = []
        if self.on_Monday:
            int_weeks.append(1)
        elif self.on_Tuesday:
            int_weeks.append(2)
        elif self.on_Wednesday:
            int_weeks.append(3)
        elif self.on_Thursday:
            int_weeks.append(4)
        elif self.on_Friday:
            int_weeks.append(5)
        elif self.on_Saturday:
            int_weeks.append(6)
        elif self.on_Sunday:
            int_weeks.append(7)

        return int_weeks

    def __str__(self):
        return f'Периодичность привычки - {Periodicity.objects.get(pk=self.pk).addiction_set}'

    class Meta:
        verbose_name = 'Периодичность'
        verbose_name_plural = 'Периодичности'


class NiceAddiction(models.Model):
    """
    Отдельная модель для приятной привычки
    """
    location = models.CharField(max_length=50, verbose_name='Где делаю', default="Где-то")
    time = models.TimeField(verbose_name='Когда делаю', auto_now=True)
    activity_name = models.TextField(verbose_name="Что делаю", default="балду гоняю")

    def __str__(self):
        return f'Приятная привычка {self.activity_name} связанная с - {NiceAddiction.objects.get(pk=self.pk).addiction_set}'

    class Meta:
        verbose_name = 'Приятная привычка'
        verbose_name_plural = 'Приятные привычки'


class Addiction(models.Model):
    """
    Модель привычки содержащая в себе собственные аттрибуты, а также связанная с объектом периодичность и приятная привычка
    """
    proprietor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                                   verbose_name='Владелец')
    location = models.CharField(max_length=50, verbose_name='Где делаю', default="Где-то")
    time = models.TimeField(verbose_name='Когда делаю')
    activity_name = models.TextField(verbose_name="Что делаю", default="балду гоняю")
    nice_addiction = models.ForeignKey(NiceAddiction, on_delete=models.CASCADE,
                                       verbose_name='Связанная полезная привычка', blank=True, null=True, default=None)
    periodicity = models.ForeignKey(Periodicity, on_delete=models.CASCADE, verbose_name='Периодичность')
    prize = models.TextField(verbose_name='Награда', **NULLABLE)
    run_time = models.IntegerField(verbose_name='Длительность в секундах', default=120)
    is_public = models.BooleanField(verbose_name='Публичная привычка')
    last_send = models.TimeField(verbose_name='Дата последнего отправки', auto_now=True)

    def __str__(self):
        return f'Полезная привычка {self.activity_name}'

    class Meta:
        verbose_name = 'Полезная привычка'
        verbose_name_plural = 'Полезные привычки'
