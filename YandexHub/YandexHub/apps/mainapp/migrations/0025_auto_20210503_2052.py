# Generated by Django 3.1.7 on 2021-05-03 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0024_auto_20210503_2051'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filmlike',
            old_name='likedfilm',
            new_name='liked_film',
        ),
        migrations.AlterField(
            model_name='actor',
            name='actor_id',
            field=models.CharField(blank=True, default='dW99r2554GN81eQRA5dQ2Z67RLGbakrK', max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='producer',
            name='producer_id',
            field=models.CharField(blank=True, default='YnRn6kFuKQ5HwDTe5ZnTp9tnJPzXkzbb', max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='writer',
            name='writer_id',
            field=models.CharField(blank=True, default='1CyuafqHBH7JxhUTrieVCb2r4s3Ds8E9', max_length=32, null=True),
        ),
    ]