# Generated by Django 4.0.6 on 2022-11-01 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0004_rename_budget_compare_activitycategory_total_budget'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'verbose_name_plural': 'Activities'},
        ),
        migrations.AlterModelOptions(
            name='activitycategory',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='points',
            options={'verbose_name_plural': 'Points'},
        ),
        migrations.AlterField(
            model_name='activitycategory',
            name='total_budget',
            field=models.IntegerField(null=True),
        ),
    ]
