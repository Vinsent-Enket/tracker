from rest_framework.serializers import ValidationError

from tracker.models import NiceAddiction, Periodicity


class RunTimeValidation:
    """
    Валидатор времени выполнения привычки
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        run_time = dict(value).get(self.field)
        if run_time > 120:
            raise ValidationError("Время выполенения должно быть не меньше 120 секунд")


class IsNiceAddictionValidation:
    """
    Если бы была одна модель привычки, был бы доп аттрибут
    is_nice_addiction который бы проверядся в этом валидаторе
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        nice_addiction = dict(value).get(self.field)
        if not nice_addiction.is_nice_addiction:
            raise ValidationError("Выбранная привычка не является приятной")

