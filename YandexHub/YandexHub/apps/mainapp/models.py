# MODELS
from django.db import models
from django.contrib.auth.models import AbstractUser

# HELPERS
from .helpers import generate_id

# User
class CustomUser(AbstractUser):
    # user id
    user_id = models.CharField(blank=True, null=True, max_length=24, default=generate_id(24))
    
    # email
    email = models.EmailField(null=True, unique=True)

    # username
    username = models.CharField(blank=True, null=True, max_length=50)

    # user media
    avatar = models.ImageField(blank=True, null=True, upload_to = 'avatars/', default='avatars/default/default_avatar.png')
    banner = models.ImageField(blank=True, null=True, upload_to='users_banners/')
    
    # video
    all_views = models.BigIntegerField(default=0)
    all_comments = models.BigIntegerField(default=0)
    all_likes = models.BigIntegerField(default=0)
    all_dislikes = models.BigIntegerField(default=0)

    # user
    all_subscribers = models.BigIntegerField(default=0)
    all_notifications = models.BigIntegerField(default=0)

    # posts
    all_posts_likes = models.BigIntegerField(default=0)
    all_posts_dislikes = models.BigIntegerField(default=0)
    
    # user info
    description = models.TextField(blank=True, null=True, max_length=5000)
    contact_email  = models.CharField(blank=True, null=True, max_length=75)
    location = models.CharField(blank=True, null=True, max_length=50)
    vk_link = models.CharField(blank=True, null=True, max_length=150)
    instagram_link = models.CharField(blank=True, null=True, max_length=150)
    facebook_link = models.CharField(blank=True, null=True, max_length=150)
    reddit_link = models.CharField(blank=True, null=True, max_length=150)
    telegram_link = models.CharField(blank=True, null=True, max_length=150)
    twitter_link = models.CharField(blank=True, null=True, max_length=150)
    website_link = models.CharField(blank=True, null=True, max_length=150)
 
    # telegram 
    telegram = models.CharField(blank=True, null=True, max_length=150)
    
    # yoomoney
    wallet = models.CharField(blank=True, null=True, max_length=16)
    donat_text = models.CharField(blank=True, null=True, max_length=60, default="Support the author ❤️")

    # date created
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'
    
    def __str__(self):
        return self.email

class Subscribe(models.Model):
    subscriber = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='subscriber')
    channel = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='subscribers')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

class Notification(models.Model):
    notification_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='notification_user')
    notification_channel = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='notification_channel')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

# Video
class Video(models.Model):
    # video id
    video_id = models.CharField(blank=True, null=True, max_length=32)

    # creator
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='video_creator')

    # files
    video = models.FileField(upload_to='videos/')
    video_banner = models.ImageField(upload_to='video_banners/')

    # stats
    views = models.BigIntegerField(default=0)
    likes = models.BigIntegerField(default=0)
    dislikes = models.BigIntegerField(default=0)
    comments = models.BigIntegerField(default=0)

    # coefficient for tranding tab
    coefficient = models.FloatField(default=0)

    # video info
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True, max_length=1000000)

    # date created
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

    # date for analytics
    date_created_without_time = models.DateField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.title

class VideoViewModel(models.Model):
    watched_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='watched_user')
    watched_video = models.ForeignKey(Video, on_delete=models.CASCADE, null=False, related_name='watched_video')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    date_created2 = models.DateField(auto_now_add=True, db_index=True)

class SavedVideo(models.Model):
    saved_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='saved_user')
    saved_video = models.ForeignKey(Video, on_delete=models.CASCADE, null=False, related_name='saved_video')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

class Like(models.Model):
    liked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='liked_video_user')
    liked_video = models.ForeignKey(Video, on_delete=models.CASCADE, null=False, related_name='liked_video')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

class Dislike(models.Model):
    disliked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='disliked_video_user')
    disliked_video = models.ForeignKey(Video, on_delete=models.CASCADE, null=False, related_name='disliked_video')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

# Comments for videos
class Comment(models.Model):
    # comment id
    comment_id = models.CharField(blank=True, null=True, max_length=32)

    # comment creator
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='comment_creator')

    # video
    commented_video = models.ForeignKey(Video, on_delete=models.CASCADE, null=False, related_name='commented_video')

    # stats
    likes = models.BigIntegerField(default=0)
    dislikes = models.BigIntegerField(default=0)
    replies = models.BigIntegerField(default=0)

    # text
    comment_text = models.TextField(max_length=5000)

    # date created
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.comment_text

class CommentLike(models.Model):
    liked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='liked_comment_user')
    liked_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=False, related_name='liked_comment')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

class CommentDislike(models.Model):
    disliked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='disliked_comment_user')
    disliked_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=False, related_name='disliked_comment')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

# Reply comments for videos
class ReplyComment(models.Model):
    # reply comment id
    reply_comment_id = models.CharField(blank=True, null=True, max_length=32)

    # reply comment creator
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='reply_comment_creator')
    reply_commented_video = models.ForeignKey(Video, on_delete=models.CASCADE, null=False, related_name='reply_commented_video')

    # comment parent
    comment_parent = models.ForeignKey(Comment, on_delete=models.CASCADE, null=False, related_name='comment_parent')

    # stats
    likes = models.BigIntegerField(default=0)
    dislikes = models.BigIntegerField(default=0)
    
    # text
    comment_text = models.TextField(max_length=5000)

    # date created
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    
    def __str__(self):
        return self.comment_text

class ReplyCommentLike(models.Model):
    liked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='liked_reply_comment_user')
    liked_reply_comment = models.ForeignKey(ReplyComment, on_delete=models.CASCADE, null=False, related_name='liked_reply_comment')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

class ReplyCommentDislike(models.Model):
    disliked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='disliked_reply_comment_user')
    disliked_reply_comment = models.ForeignKey(ReplyComment, on_delete=models.CASCADE, null=False, related_name='disliked_reply_comment')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)


# Article
class Article(models.Model):
    # article id
    article_id = models.CharField(blank=True, null=True, max_length=32)

    # article creator
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='article_creator')

    # stats
    likes = models.BigIntegerField(default=0)
    dislikes = models.BigIntegerField(default=0)

    # text
    text = models.TextField(blank=True, null=True, max_length=1000000)

    # date created
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.article_id

class ArticleLike(models.Model):
    liked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='liked_article_user')
    liked_article = models.ForeignKey(Article, on_delete=models.CASCADE, null=False, related_name='liked_article')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

class ArticleDislike(models.Model):
    disliked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='disliked_article_user')
    disliked_article = models.ForeignKey(Article, on_delete=models.CASCADE, null=False, related_name='disliked_article')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)


# Actor
class Actor(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    # actor id
    actor_id = models.CharField(blank=True, null=True, max_length=32, default=generate_id(32))

    # actor info
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=50, null=True, choices=GENDER)
    photo = models.ImageField(upload_to='avatars/', default="avatars/default/man.png")

    def __str__(self):
        return self.name

# Producer
class Producer(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    # producer id
    producer_id = models.CharField(blank=True, null=True, max_length=32, default=generate_id(32))

    # producer info
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=50, null=True, choices=GENDER)
    photo = models.ImageField(upload_to='avatars/', default="avatars/default/man.png")

    def __str__(self):
        return self.name

# Writer
class Writer(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    # writer id
    writer_id = models.CharField(blank=True, null=True, max_length=32, default=generate_id(32))

    # writer info
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=50, null=True, choices=GENDER)
    photo = models.ImageField(upload_to='avatars/', default="avatars/default/man.png")

    def __str__(self):
        return self.name

# Genre
class Genre(models.Model):
    # genre name
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


# Film
class Film(models.Model):
    RATING = (
        ('0+', '0+'),
        ('6+', '6+'),
        ('12+', '12+'),
        ('16+', '16+'),
        ('18+', '18+')
    )

    # film id
    film_id = models.CharField(blank=True, null=True, max_length=32)

    # files
    film = models.FileField(upload_to='films/')
    trailer = models.FileField(upload_to='trailers/')
    film_poster = models.ImageField(upload_to='film_posters/')
    film_banner = models.ImageField(upload_to='film_banners/')

    # stats
    likes = models.BigIntegerField(default=0)
    dislikes = models.BigIntegerField(default=0)
    #comments = models.BigIntegerField(default=0)

    # film info
    title = models.CharField(max_length=150)
    price = models.FloatField(default=0)
    running_time = models.CharField(max_length=150, default="0:00")
    rating = models.CharField(max_length=50, null=True, choices=RATING)
    release_date = models.DateField()
    release_year = models.CharField(max_length=4, default="2021")
    main_genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=False)
    description = models.TextField(blank=True, null=True, max_length=1000000)

    # date created
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.title

class FilmLike(models.Model):
    liked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='liked_film_user')
    liked_film = models.ForeignKey(Film, on_delete=models.CASCADE, null=False, related_name='liked_film')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

class FilmDislike(models.Model):
    disliked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='disliked_film_user')
    disliked_film = models.ForeignKey(Film, on_delete=models.CASCADE, null=False, related_name='disliked_film')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

class FilmProducer(models.Model):
    producer_film = models.ForeignKey(Film, on_delete=models.CASCADE, null=False, related_name='producer_film')
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, null=False, related_name='producer')

class FilmActor(models.Model):
    actor_film = models.ForeignKey(Film, on_delete=models.CASCADE, null=False, related_name='actor_film')
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, null=False, related_name='actor')

class FilmWriter(models.Model):
    writer_film = models.ForeignKey(Film, on_delete=models.CASCADE, null=False, related_name='writer_film')
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE, null=False, related_name='writer')

class FilmGenre(models.Model):
    genre_film = models.ForeignKey(Film, on_delete=models.CASCADE, null=False, related_name='genre_film')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=False, related_name='genre')

class BuyFilm(models.Model):
    buy_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='buy_user')
    buy_film = models.ForeignKey(Film, on_delete=models.CASCADE, null=False, related_name='buy_film')