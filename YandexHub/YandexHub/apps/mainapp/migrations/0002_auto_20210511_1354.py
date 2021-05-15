# Generated by Django 3.1.7 on 2021-05-11 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='actor_id',
            field=models.CharField(blank=True, default='keqhSDSpF1mzCabwvMawpqasQX4CduUq', max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_id',
            field=models.CharField(blank=True, max_length=24, null=True),
        ),
        migrations.AlterField(
            model_name='producer',
            name='producer_id',
            field=models.CharField(blank=True, default='XK7zBZCHmqcuuBnvRPB3WckcGg5Tzw8p', max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='writer',
            name='writer_id',
            field=models.CharField(blank=True, default='mJBLp1QRzaxUrZeZju5qgjp7PsA1vYGe', max_length=32, null=True),
        ),
    ]
