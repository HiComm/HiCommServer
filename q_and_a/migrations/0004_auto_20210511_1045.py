# Generated by Django 2.2.12 on 2021-05-11 01:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('q_and_a', '0003_auto_20210511_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='good_posted_by',
            field=models.ManyToManyField(blank=True, related_name='a_good_posted_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='diary',
            name='good_posted_by',
            field=models.ManyToManyField(blank=True, related_name='d_good_posted_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='good_posted_by',
            field=models.ManyToManyField(blank=True, related_name='q_good_posted_by', to=settings.AUTH_USER_MODEL),
        ),
    ]