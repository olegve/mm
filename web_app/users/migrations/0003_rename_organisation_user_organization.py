# Generated by Django 5.0.6 on 2024-06-03 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='organisation',
            new_name='organization',
        ),
    ]
