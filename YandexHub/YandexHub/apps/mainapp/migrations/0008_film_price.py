# Generated by Django 3.1.7 on 2021-05-02 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_auto_20210502_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]