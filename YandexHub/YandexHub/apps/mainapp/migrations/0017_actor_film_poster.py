# Generated by Django 3.1.7 on 2021-05-03 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0016_auto_20210503_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='actor',
            name='film_poster',
            field=models.ImageField(default='avatars/default/man.png', upload_to='avatars/'),
        ),
    ]
