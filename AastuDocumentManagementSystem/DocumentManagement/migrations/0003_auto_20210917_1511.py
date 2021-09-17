# Generated by Django 3.2.5 on 2021-09-17 12:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DocumentManagement', '0002_auto_20210917_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_receiver',
            field=models.ManyToManyField(related_name='receiver', to='DocumentManagement.ReceiverUser'),
        ),
        migrations.AlterField(
            model_name='message',
            name='message_sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='replymessage',
            name='reply_receiver',
            field=models.ManyToManyField(related_name='reply_receiver', to='DocumentManagement.ReceiverUser'),
        ),
        migrations.AlterField(
            model_name='replymessage',
            name='reply_sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_sender', to=settings.AUTH_USER_MODEL),
        ),
    ]
