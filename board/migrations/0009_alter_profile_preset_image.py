# Generated by Django 4.1.4 on 2023-02-26 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0008_profile_preset_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='preset_image',
            field=models.CharField(blank=True, default='default1.jpg', max_length=50, null=True),
        ),
    ]
