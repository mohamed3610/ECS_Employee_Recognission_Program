# Generated by Django 4.0.6 on 2022-12-13 09:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0020_alter_announcement_startdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='userregisterationrequest',
            name='accept_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='StartDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 13, 11, 3, 18, 419772)),
        ),
        migrations.AlterField(
            model_name='userregisterationrequest',
            name='password',
            field=models.CharField(default='123456Abc', editable=False, max_length=100),
        ),
    ]