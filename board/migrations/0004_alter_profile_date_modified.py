# Generated by Django 4.1.4 on 2023-02-09 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_rename_date_modiefied_profile_date_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
