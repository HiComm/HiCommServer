# Generated by Django 2.2.12 on 2021-04-22 07:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('q_and_a', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='comments',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='q_and_a.Comment'),
        ),
        migrations.AlterField(
            model_name='diary',
            name='comments',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='diary_comment', to='q_and_a.Comment'),
        ),
        migrations.AlterField(
            model_name='diary',
            name='related_to',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='diary_related_to', to='q_and_a.PostItem'),
        ),
        migrations.AlterField(
            model_name='postitem',
            name='date_created',
            field=models.TimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='postitem',
            name='date_modified',
            field=models.TimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='postitem',
            name='date_published',
            field=models.TimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='comments',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='q_and_a.Comment'),
        ),
    ]
