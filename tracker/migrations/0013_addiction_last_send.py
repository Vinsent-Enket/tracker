# Generated by Django 5.0.3 on 2024-04-10 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0012_alter_addiction_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='addiction',
            name='last_send',
            field=models.TimeField(auto_now=True, verbose_name='Дата последнего отправки'),
        ),
    ]