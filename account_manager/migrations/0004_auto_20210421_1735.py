# Generated by Django 2.2.12 on 2021-04-21 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_manager', '0003_auto_20210421_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=128, unique=True, verbose_name='username'),
        ),
    ]