# Generated by Django 5.0.3 on 2024-04-03 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='chat_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='ID чата в телеграмм'),
        ),
    ]
