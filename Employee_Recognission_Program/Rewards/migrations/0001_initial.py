# Generated by Django 4.0.6 on 2022-10-23 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('budget', models.IntegerField()),
                ('point', models.IntegerField(null=True)),
                ('EGP', models.IntegerField(null=True)),
                ('budget_compare', models.IntegerField()),
                ('year', models.IntegerField(default=2022)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('Archived_at', models.DateTimeField(null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Redemption_Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accpeted'), ('REJECTED', 'Rejected'), ('WITHDRAWN', 'Withdrawn')], default='Pending', max_length=10)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('approved_date', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_day', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('points_equivalent', models.IntegerField()),
                ('is_archived', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Suggest_vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor', models.CharField(max_length=30)),
                ('website', models.CharField(max_length=255)),
                ('reason', models.CharField(max_length=1024)),
                ('is_archived', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accpeted'), ('REJECTED', 'Rejected'), ('WITHDRAWN', 'Withdrawn')], default='Pending', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('vendor_policy', models.CharField(max_length=5000, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(null=True)),
                ('img', models.ImageField(blank=True, upload_to='images/')),
                ('accepts_voucher', models.BooleanField(default=False)),
                ('accepts_procurement', models.BooleanField(default=False)),
                ('accepts_direct', models.BooleanField(default=False)),
                ('is_archived', models.BooleanField(default=False)),
            ],
        ),
    ]
