# Generated by Django 5.0.3 on 2024-04-09 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0011_alter_addiction_nice_addiction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addiction',
            name='time',
            field=models.TimeField(verbose_name='Когда делаю'),
        ),
    ]
