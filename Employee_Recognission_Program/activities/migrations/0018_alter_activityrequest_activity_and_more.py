# Generated by Django 4.0.6 on 2022-11-29 10:16

import activities.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0017_rename_emp_activityrequest_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityrequest',
            name='activity',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='activities.activity'),
        ),
        migrations.AlterField(
            model_name='activityrequest',
            name='activity_approval_date',
            field=models.DateTimeField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='activityrequest',
            name='approved_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approver_of_upload', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='activityrequest',
            name='category',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='activities.activitycategory'),
        ),
        migrations.AlterField(
            model_name='activityrequest',
            name='date_of_action',
            field=models.DateTimeField(editable=False, validators=[activities.models.validate_date_of_action]),
        ),
        migrations.AlterField(
            model_name='activityrequest',
            name='employee',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='original_uploader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='activityrequest',
            name='proof_of_action',
            field=models.FileField(editable=False, upload_to='proofs/'),
        ),
        migrations.AlterField(
            model_name='activityrequest',
            name='submitter',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submitter', to=settings.AUTH_USER_MODEL),
        ),
    ]
