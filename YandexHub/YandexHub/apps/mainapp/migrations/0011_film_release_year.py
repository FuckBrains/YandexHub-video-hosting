# Generated by Django 3.1.7 on 2021-05-03 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_film_running_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='release_year',
            field=models.CharField(default='2021', max_length=4),
        ),
    ]
