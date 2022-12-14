# Generated by Django 4.0.6 on 2022-12-04 13:37

import activities.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0019_remove_activityrequest_is_archived'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='start_date',
            field=models.DateField(default=datetime.date(2022, 12, 4), validators=[activities.models.validate_year]),
        ),
        migrations.AlterField(
            model_name='activitycategory',
            name='start_date',
            field=models.DateField(default=datetime.date(2022, 12, 4), validators=[activities.models.validate_year]),
        ),
        migrations.AlterField(
            model_name='activitysuggestion',
            name='start_date',
            field=models.DateField(default=datetime.date(2022, 12, 4), validators=[activities.models.validate_year]),
        ),
    ]
