# Generated by Django 3.1.7 on 2021-04-25 13:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20210422_1823'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_id', models.CharField(blank=True, max_length=32, null=True)),
                ('likes', models.BigIntegerField(default=0)),
                ('dislikes', models.BigIntegerField(default=0)),
                ('text', models.TextField(blank=True, max_length=1000000, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('liked_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_article', to='mainapp.article')),
                ('liked_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_article_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleDislike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('disliked_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disliked_article', to='mainapp.article')),
                ('disliked_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disliked_article_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]