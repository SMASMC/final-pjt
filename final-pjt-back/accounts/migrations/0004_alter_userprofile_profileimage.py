# Generated by Django 4.2.1 on 2025-05-24 11:30

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_userprofile_deletedat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profileImage',
            field=models.ImageField(blank=True, null=True, upload_to=accounts.models.user_profile_upload_path),
        ),
    ]
