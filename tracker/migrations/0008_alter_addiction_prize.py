# Generated by Django 5.0.3 on 2024-04-01 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0007_remove_goodaddiction_proprietor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addiction',
            name='prize',
            field=models.TextField(blank=True, null=True, verbose_name='Награда'),
        ),
    ]