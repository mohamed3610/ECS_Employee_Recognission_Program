# Generated by Django 4.0.6 on 2022-10-16 14:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
            name='Vendors',
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
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendor_creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rewards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_day', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('points_equivalent', models.IntegerField()),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reward_creator', to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Rewards.vendors')),
            ],
        ),
        migrations.CreateModel(
            name='Redemption_Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accpeted'), ('REJECTED', 'Rejected'), ('WITHDRAWN', 'Withdrawn')], default='Pending', max_length=10)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('approved_date', models.DateTimeField(null=True)),
                ('is_rejected', models.BooleanField(default=False)),
                ('approved_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin', to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee', to=settings.AUTH_USER_MODEL)),
                ('voucher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Rewards.rewards')),
            ],
        ),
        migrations.CreateModel(
            name='OldDataVendors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('vendor_policy', models.CharField(max_length=5000, null=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(null=True)),
                ('img', models.ImageField(blank=True, upload_to='images/')),
                ('update_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('accepts_voucher', models.BooleanField()),
                ('accepts_procurement', models.BooleanField()),
                ('accepts_direct', models.BooleanField()),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('original_vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Rewards.vendors')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendor_updater', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OldDataSuggest_Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor', models.CharField(max_length=30)),
                ('website', models.CharField(max_length=255)),
                ('reason', models.CharField(max_length=1024)),
                ('edit_delete_date', models.DateTimeField(null=True)),
                ('edited', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('update_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accpeted'), ('REJECTED', 'Rejected'), ('WITHDRAWN', 'Withdrawn')], default='Pending', max_length=20)),
                ('original_suggestion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Rewards.suggest_vendor')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendorsuggestion_updater', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OldDataRewards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_day', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('points_equivalent', models.IntegerField()),
                ('update_date', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('original_voucher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Rewards.rewards')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reward_updater', to=settings.AUTH_USER_MODEL)),
            ],
        ),
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
                ('admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ArchiveRewards',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('creation_day', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('points_equivalent', models.IntegerField()),
                ('archived_date', models.DateTimeField(auto_now_add=True)),
                ('archived_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='archiver_reward', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ArchivedVendors',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30, unique=True)),
                ('vendor_policy', models.CharField(max_length=5000, null=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(null=True)),
                ('img', models.ImageField(blank=True, upload_to='images/')),
                ('accepts_voucher', models.BooleanField()),
                ('accepts_procurement', models.BooleanField()),
                ('accepts_direct', models.BooleanField()),
                ('update_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('archived_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendor_archiver', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('original_vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Rewards.vendors')),
            ],
        ),
    ]
