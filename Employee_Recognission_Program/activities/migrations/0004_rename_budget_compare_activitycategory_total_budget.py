# Generated by Django 4.0.6 on 2022-10-30 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_activityrequest_is_archived'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activitycategory',
            old_name='budget_compare',
            new_name='total_budget',
        ),
    ]