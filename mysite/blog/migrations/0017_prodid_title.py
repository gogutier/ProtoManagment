# Generated by Django 2.0.5 on 2018-08-19 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_prodid'),
    ]

    operations = [
        migrations.AddField(
            model_name='prodid',
            name='title',
            field=models.CharField(default='orden', max_length=200),
        ),
    ]