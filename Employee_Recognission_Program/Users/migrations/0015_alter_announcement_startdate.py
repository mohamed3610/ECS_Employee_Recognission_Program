# Generated by Django 4.1.3 on 2022-12-06 08:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0014_alter_announcement_startdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='StartDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 6, 10, 39, 25, 338761)),
        ),
    ]
