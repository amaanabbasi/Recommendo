# Generated by Django 2.1.5 on 2019-01-08 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ideal_event', '0002_auto_20190108_1033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appuser',
            name='friends',
        ),
    ]
