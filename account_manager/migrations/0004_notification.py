# Generated by Django 2.2.12 on 2021-05-27 05:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account_manager', '0003_auto_20210511_1044'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('body', models.TextField(default='')),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('is_expired', models.BooleanField(default=False)),
                ('post_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]