# Generated by Django 2.1.5 on 2019-01-08 10:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ideal_event', '0003_remove_appuser_friends'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interest2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest_level', models.DecimalField(decimal_places=1, default=0, max_digits=6, validators=[django.core.validators.MaxValueValidator(5.0), django.core.validators.MinValueValidator(0.0)])),
                ('interest_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ideal_event.Interest')),
            ],
        ),
        migrations.AlterField(
            model_name='appuser',
            name='interests',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ideal_event.Interest2'),
        ),
    ]
