# Generated by Django 5.0.6 on 2024-05-13 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('input_queue', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inputqueue',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Время создания'),
        ),
    ]
