# Generated by Django 5.0.6 on 2024-06-06 15:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
        ('users', '0003_rename_organisation_user_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='organizations.organization', verbose_name='Организация'),
        ),
    ]
