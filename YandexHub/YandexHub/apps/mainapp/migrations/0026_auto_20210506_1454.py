# Generated by Django 3.1.7 on 2021-05-06 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0025_auto_20210503_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='all_notifications',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='actor',
            name='actor_id',
            field=models.CharField(blank=True, default='bGZA1e5Y7G3mD6fL38c5gAEaViytjbWM', max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='producer',
            name='producer_id',
            field=models.CharField(blank=True, default='j7gpvYVgTmv8AcgiKsuG2BVdbckw7N4Q', max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='writer',
            name='writer_id',
            field=models.CharField(blank=True, default='rryCPgDC8Dtgjgu2TPX9Er9eBCWh9qtk', max_length=32, null=True),
        ),
    ]
