# Generated by Django 4.1.4 on 2022-12-25 11:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0023_alter_announcement_startdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='StartDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
