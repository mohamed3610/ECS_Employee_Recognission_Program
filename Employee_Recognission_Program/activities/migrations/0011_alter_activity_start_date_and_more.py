# Generated by Django 4.0.6 on 2022-11-22 13:44

import activities.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0010_alter_activitycategory_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='start_date',
            field=models.DateField(default=datetime.date(2022, 11, 22), validators=[activities.models.validate_year]),
        ),
        migrations.AlterField(
            model_name='activitycategory',
            name='start_date',
            field=models.DateField(default=datetime.date(2022, 11, 22), validators=[activities.models.validate_year]),
        ),
    ]
