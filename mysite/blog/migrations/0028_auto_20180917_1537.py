# Generated by Django 2.0.5 on 2018-09-17 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0027_auto_20180917_1521'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detalleprog',
            old_name='programa',
            new_name='programma',
        ),
    ]
