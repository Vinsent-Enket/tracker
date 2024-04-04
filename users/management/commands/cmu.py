from itertools import chain
from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    """Надо ли и тут прятать логины пароли в переменные окружения????"""

    def handle(self, *args, **options):
        manager_group = Group.objects.create(name='Moderator')  # а как удалять не в ручную?
        # Получение прав на просмотр всех категорий и моделей без возможности изменения
        add_permissions = Permission.objects.filter(codename__startswith='add_')
        change_permissions = Permission.objects.filter(codename__startswith='change_')
        view_permissions = Permission.objects.filter(codename__startswith='view_')
        all_permissions = chain(add_permissions, change_permissions, view_permissions)
        manager_group.permissions.set(all_permissions)


