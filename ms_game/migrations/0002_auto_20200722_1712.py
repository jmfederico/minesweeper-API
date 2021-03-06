# Generated by Django 3.0.8 on 2020-07-22 17:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ms_game', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='timelog',
        ),
        migrations.AddField(
            model_name='game',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='finished_at',
            field=models.DateTimeField(null=True, verbose_name='finished'),
        ),
    ]
