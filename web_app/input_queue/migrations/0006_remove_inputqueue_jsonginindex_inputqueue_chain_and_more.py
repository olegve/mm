# Generated by Django 5.0.6 on 2024-05-22 08:13

import django.contrib.postgres.indexes
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('input_queue', '0005_alter_inputqueue_message'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='inputqueue',
            name='JSONGinIndex',
        ),
        migrations.AddField(
            model_name='inputqueue',
            name='chain',
            field=models.JSONField(default=dict, verbose_name='Цепочка задач'),
        ),
        migrations.AddIndex(
            model_name='inputqueue',
            index=django.contrib.postgres.indexes.GinIndex(fields=['message', 'meta', 'chain'], name='JSONGinIndex'),
        ),
    ]