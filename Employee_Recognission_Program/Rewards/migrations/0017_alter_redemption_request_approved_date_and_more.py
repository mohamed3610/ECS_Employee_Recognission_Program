# Generated by Django 4.0.6 on 2022-12-05 09:39

import Rewards.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rewards', '0016_alter_redemption_request_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redemption_request',
            name='approved_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 5, 11, 39, 35, 555291), editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='reward',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 5, 11, 39, 35, 555291), validators=[Rewards.models.validate_year]),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 5, 11, 39, 35, 554294), validators=[Rewards.models.validate_year]),
        ),
    ]
