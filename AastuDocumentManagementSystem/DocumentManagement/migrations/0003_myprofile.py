# Generated by Django 3.0.7 on 2021-09-17 05:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DocumentManagement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyProfile',
            fields=[
                ('prof_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('profile_image', models.ImageField(upload_to='images/')),
                ('profile_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]