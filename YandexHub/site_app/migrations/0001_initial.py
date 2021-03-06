# Generated by Django 3.2.3 on 2021-06-21 21:24

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_id', models.CharField(blank=True, max_length=24, null=True)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('username', models.CharField(blank=True, max_length=50, null=True)),
                ('avatar', models.ImageField(blank=True, default='avatars/default/default_avatar.png', null=True, upload_to='avatars/')),
                ('banner', models.ImageField(blank=True, null=True, upload_to='users_banners/')),
                ('all_auditions', models.BigIntegerField(default=0)),
                ('all_views', models.BigIntegerField(default=0)),
                ('all_comments', models.BigIntegerField(default=0)),
                ('all_likes', models.BigIntegerField(default=0)),
                ('all_dislikes', models.BigIntegerField(default=0)),
                ('all_subscribers', models.BigIntegerField(default=0)),
                ('all_notifications', models.BigIntegerField(default=0)),
                ('all_posts_likes', models.BigIntegerField(default=0)),
                ('all_posts_dislikes', models.BigIntegerField(default=0)),
                ('description', models.TextField(blank=True, max_length=5000, null=True)),
                ('contact_email', models.CharField(blank=True, max_length=75, null=True)),
                ('location', models.CharField(blank=True, max_length=50, null=True)),
                ('vk_link', models.CharField(blank=True, max_length=150, null=True)),
                ('instagram_link', models.CharField(blank=True, max_length=150, null=True)),
                ('facebook_link', models.CharField(blank=True, max_length=150, null=True)),
                ('reddit_link', models.CharField(blank=True, max_length=150, null=True)),
                ('telegram_link', models.CharField(blank=True, max_length=150, null=True)),
                ('twitter_link', models.CharField(blank=True, max_length=150, null=True)),
                ('website_link', models.CharField(blank=True, max_length=150, null=True)),
                ('telegram', models.CharField(blank=True, max_length=150, null=True)),
                ('wallet', models.CharField(blank=True, max_length=16, null=True)),
                ('donat_text', models.CharField(blank=True, default='Support the author ??????', max_length=60, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actor_id', models.CharField(blank=True, default='DEAD0DB99F1D47629D15D5759BB515E8', max_length=32, null=True)),
                ('name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=50, null=True)),
                ('photo', models.ImageField(default='avatars/default/man.png', upload_to='avatars/')),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_id', models.CharField(blank=True, max_length=32, null=True)),
                ('likes', models.BigIntegerField(default=0)),
                ('dislikes', models.BigIntegerField(default=0)),
                ('text', models.TextField(blank=True, max_length=1000000, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_created_without_time', models.DateField(auto_now_add=True, db_index=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_id', models.CharField(blank=True, max_length=32, null=True)),
                ('likes', models.BigIntegerField(default=0)),
                ('dislikes', models.BigIntegerField(default=0)),
                ('replies', models.BigIntegerField(default=0)),
                ('comment_text', models.TextField(max_length=5000)),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_created_without_time', models.DateField(auto_now_add=True, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('film_id', models.CharField(blank=True, max_length=32, null=True)),
                ('film', models.FileField(upload_to='films/')),
                ('trailer', models.FileField(upload_to='trailers/')),
                ('film_poster', models.ImageField(upload_to='film_posters/')),
                ('film_banner', models.ImageField(upload_to='film_banners/')),
                ('likes', models.BigIntegerField(default=0)),
                ('dislikes', models.BigIntegerField(default=0)),
                ('title', models.CharField(max_length=150)),
                ('price', models.FloatField(default=0)),
                ('running_time', models.CharField(default='0:00', max_length=150)),
                ('rating', models.CharField(choices=[('0+', '0+'), ('6+', '6+'), ('12+', '12+'), ('16+', '16+'), ('18+', '18+')], max_length=50, null=True)),
                ('release_date', models.DateField()),
                ('release_year', models.CharField(default='2021', max_length=4)),
                ('description', models.TextField(blank=True, max_length=1000000, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Producer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producer_id', models.CharField(blank=True, default='4512A993AF134B31BB1183BADF3558D2', max_length=32, null=True)),
                ('name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=50, null=True)),
                ('photo', models.ImageField(default='avatars/default/man.png', upload_to='avatars/')),
            ],
        ),
        migrations.CreateModel(
            name='ReplyComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply_comment_id', models.CharField(blank=True, max_length=32, null=True)),
                ('likes', models.BigIntegerField(default=0)),
                ('dislikes', models.BigIntegerField(default=0)),
                ('comment_text', models.TextField(max_length=5000)),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_created_without_time', models.DateField(auto_now_add=True, db_index=True)),
                ('comment_parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_parent', to='site_app.comment')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_comment_creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track_id', models.CharField(blank=True, max_length=32, null=True)),
                ('track', models.FileField(upload_to='tracks/')),
                ('track_poster', models.ImageField(upload_to='track_posters/')),
                ('title', models.CharField(max_length=150)),
                ('auditions', models.BigIntegerField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_created_without_time', models.DateField(auto_now_add=True, db_index=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='track_creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_id', models.CharField(blank=True, max_length=32, null=True)),
                ('video', models.FileField(upload_to='videos/')),
                ('video_banner', models.ImageField(upload_to='video_banners/')),
                ('views', models.BigIntegerField(default=0)),
                ('likes', models.BigIntegerField(default=0)),
                ('dislikes', models.BigIntegerField(default=0)),
                ('comments', models.BigIntegerField(default=0)),
                ('coefficient', models.FloatField(default=0)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True, max_length=1000000, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_created_without_time', models.DateField(auto_now_add=True, db_index=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Writer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('writer_id', models.CharField(blank=True, default='73DF7660938B4E099778D357CB76D119', max_length=32, null=True)),
                ('name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=50, null=True)),
                ('photo', models.ImageField(default='avatars/default/man.png', upload_to='avatars/')),
            ],
        ),
        migrations.CreateModel(
            name='VideoViewModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_created_without_time', models.DateField(auto_now_add=True, db_index=True)),
                ('watched_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watched_user', to=settings.AUTH_USER_MODEL)),
                ('watched_video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watched_video', to='site_app.video')),
            ],
        ),
        migrations.CreateModel(
            name='TrackListenModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_created_without_time', models.DateField(auto_now_add=True, db_index=True)),
                ('listened_track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listened_track', to='site_app.track')),
                ('listening_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listening_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribers', to=settings.AUTH_USER_MODEL)),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriber', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SavedVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('saved_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_user', to=settings.AUTH_USER_MODEL)),
                ('saved_video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_video', to='site_app.video')),
            ],
        ),
        migrations.CreateModel(
            name='ReplyCommentLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('liked_reply_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_reply_comment', to='site_app.replycomment')),
                ('liked_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_reply_comment_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReplyCommentDislike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('disliked_reply_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disliked_reply_comment', to='site_app.replycomment')),
                ('disliked_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disliked_reply_comment_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='replycomment',
            name='reply_commented_video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_commented_video', to='site_app.video'),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('notification_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_channel', to=settings.AUTH_USER_MODEL)),
                ('notification_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_created_without_time', models.DateField(auto_now_add=True, db_index=True)),
                ('liked_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_video_user', to=settings.AUTH_USER_MODEL)),
                ('liked_video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_video', to='site_app.video')),
            ],
        ),
        migrations.CreateModel(
            name='FilmWriter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='writer', to='site_app.writer')),
                ('writer_film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='writer_film', to='site_app.film')),
            ],
        ),
        migrations.CreateModel(
            name='FilmProducer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producer', to='site_app.producer')),
                ('producer_film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producer_film', to='site_app.film')),
            ],
        ),
        migrations.CreateModel(
            name='FilmLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('liked_film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_film', to='site_app.film')),
                ('liked_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_film_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FilmGenre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genre', to='site_app.genre')),
                ('genre_film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genre_film', to='site_app.film')),
            ],
        ),
        migrations.CreateModel(
            name='FilmDislike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('disliked_film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disliked_film', to='site_app.film')),
                ('disliked_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disliked_film_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FilmActor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actor', to='site_app.actor')),
                ('actor_film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actor_film', to='site_app.film')),
            ],
        ),
        migrations.AddField(
            model_name='film',
            name='main_genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site_app.genre'),
        ),
        migrations.CreateModel(
            name='Dislike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_created_without_time', models.DateField(auto_now_add=True, db_index=True)),
                ('disliked_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disliked_video_user', to=settings.AUTH_USER_MODEL)),
                ('disliked_video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disliked_video', to='site_app.video')),
            ],
        ),
        migrations.CreateModel(
            name='CommentLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('liked_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_comment', to='site_app.comment')),
                ('liked_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_comment_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CommentDislike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('disliked_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disliked_comment', to='site_app.comment')),
                ('disliked_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disliked_comment_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='commented_video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commented_video', to='site_app.video'),
        ),
        migrations.AddField(
            model_name='comment',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='BuyFilm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buy_film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buy_film', to='site_app.film')),
                ('buy_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buy_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_created_without_time', models.DateField(auto_now_add=True, db_index=True)),
                ('liked_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_article', to='site_app.article')),
                ('liked_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_article_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleDislike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_created_without_time', models.DateField(auto_now_add=True, db_index=True)),
                ('disliked_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disliked_article', to='site_app.article')),
                ('disliked_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disliked_article_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
