# Generated by Django 2.0.5 on 2018-09-12 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_pruebamod_ultrafile'),
    ]

    operations = [
        migrations.CreateModel(
            name='PruebaTabla',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item1', models.CharField(default='vacio', max_length=200)),
                ('item2', models.CharField(default='vacio', max_length=200)),
                ('item3', models.TextField(default='vacio', max_length=200)),
            ],
        ),
    ]
