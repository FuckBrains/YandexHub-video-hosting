# MODELS
from django.db import models
from django.contrib.auth.models import AbstractUser

# HELPERS
from .helpers import generate_id


# User -> Channel Model
class CustomUser(AbstractUser):
    # user id
    user_id = models.CharField(blank=True, null=True, max_length=24)
    
    # user email
    email = models.EmailField(null=True, unique=True)

    # username (channel name)
    username = models.CharField(blank=True, null=True, max_length=50)

    # user avatar file
    avatar = models.ImageField(blank=True, null=True, upload_to = 'avatars/', default='avatars/default/default_avatar.png')
    
    # channel banner file
    banner = models.ImageField(blank=True, null=True, upload_to='users_banners/')
    
    # channel stats
    all_auditions = models.BigIntegerField(default=0) # all user tracks auditions
    all_views = models.BigIntegerField(default=0) # all video views
    all_comments = models.BigIntegerField(default=0) # comments under all videos
    all_likes = models.BigIntegerField(default=0) # likes under all videos
    all_dislikes = models.BigIntegerField(default=0) # dislikes under all videos
    all_subscribers = models.BigIntegerField(default=0) # subscribers
    all_notifications = models.BigIntegerField(default=0) # notifications
    all_posts_likes = models.BigIntegerField(default=0) # all likes under all posts
    all_posts_dislikes = models.BigIntegerField(default=0) # all dislikes under all posts
    
    # User info on "About" page
    description = models.TextField(blank=True, null=True, max_length=5000) # channel description
    contact_email  = models.CharField(blank=True, null=True, max_length=75) # email for contact
    location = models.CharField(blank=True, null=True, max_length=50) # user location
    vk_link = models.CharField(blank=True, null=True, max_length=150) # vk link
    instagram_link = models.CharField(blank=True, null=True, max_length=150) # instagram link
    facebook_link = models.CharField(blank=True, null=True, max_length=150) # facebook link
    reddit_link = models.CharField(blank=True, null=True, max_length=150) # reddit link
    telegram_link = models.CharField(blank=True, null=True, max_length=150) # telegram link
    twitter_link = models.CharField(blank=True, null=True, max_length=150) # twitter link
    website_link = models.CharField(blank=True, null=True, max_length=150) # website link
 
    # telegram id for notifications
    telegram = models.CharField(blank=True, null=True, max_length=150)
    
    # yoomoney
    wallet = models.CharField(blank=True, null=True, max_length=16) # yoomoney wallet for donations 
    donat_text = models.CharField(blank=True, null=True, max_length=60, default="Support the author ❤️") # text above the danat form 

    date_created = models.DateTimeField(auto_now_add=True, db_index=True) # date created
    
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'
    
    def __str__(self):
        return self.email


# Subscribe model
class Subscribe(models.Model):
    subscriber = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='subscriber')
    channel = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='subscribers')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)


# Notification model
class Notification(models.Model):
    notification_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='notification_user')
    notification_channel = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='notification_channel')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)


# Video model
class Video(models.Model):
    # video id
    video_id = models.CharField(blank=True, null=True, max_length=32)

    # creator
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='video_creator')

    # video file
    video = models.FileField(upload_to='videos/')
    
    # video banner file
    video_banner = models.ImageField(upload_to='video_banners/')

    # stats
    views = models.BigIntegerField(default=0) # all views under video 
    likes = models.BigIntegerField(default=0) # all likes under video
    dislikes = models.BigIntegerField(default=0) # all dislikes under video
    comments = models.BigIntegerField(default=0) # all comments under video
    coefficient = models.FloatField(default=0) # coefficient for tranding tab

    title = models.CharField(max_length=150) # video title
    description = models.TextField(blank=True, null=True, max_length=1000000) # video description

    date_created = models.DateTimeField(auto_now_add=True, db_index=True) # date created

    date_created_without_time = models.DateField(auto_now_add=True, db_index=True) # date created for analytics

    def __str__(self):
        return self.title


# Video view model
class VideoViewModel(models.Model):
    watched_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='watched_user')
    watched_video = models.ForeignKey(Video, on_delete=models.CASCADE, null=False, related_name='watched_video')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True) # date created
    date_created_without_time = models.DateField(auto_now_add=True, db_index=True) # date created for analytics


# Saved video model
class SavedVideo(models.Model):
    saved_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='saved_user')
    saved_video = models.ForeignKey(Video, on_delete=models.CASCADE, null=False, related_name='saved_video')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True) # date created


# Liked video model
class Like(models.Model):
    liked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='liked_video_user')
    liked_video = models.ForeignKey(Video, on_delete=models.CASCADE, null=False, related_name='liked_video')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True) # date created
    date_created_without_time = models.DateField(auto_now_add=True, db_index=True) # date created for analytics


# Dislike video model
class Dislike(models.Model):
    disliked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='disliked_video_user')
    disliked_video = models.ForeignKey(Video, on_delete=models.CASCADE, null=False, related_name='disliked_video')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True) # date created
    date_created_without_time = models.DateField(auto_now_add=True, db_index=True) # date created for analytics


# Comment model
class Comment(models.Model):
    # comment id
    comment_id = models.CharField(blank=True, null=True, max_length=32)

    # comment creator
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='comment_creator')

    # commented video
    commented_video = models.ForeignKey(Video, on_delete=models.CASCADE, null=False, related_name='commented_video')

    # stats
    likes = models.BigIntegerField(default=0) # all likes under comment
    dislikes = models.BigIntegerField(default=0) # all dislikes under comment
    replies = models.BigIntegerField(default=0) # all replies under comment

    comment_text = models.TextField(max_length=5000) # comment text

    date_created = models.DateTimeField(auto_now_add=True, db_index=True) # date created
    date_created_without_time = models.DateField(auto_now_add=True, db_index=True) # date created for analytics

    def __str__(self):
        return self.comment_text


# Liked comment model
class CommentLike(models.Model):
    liked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='liked_comment_user')
    liked_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=False, related_name='liked_comment')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True) # date created


# Disliked comment model
class CommentDislike(models.Model):
    disliked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='disliked_comment_user')
    disliked_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=False, related_name='disliked_comment')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True) # date created


# Reply comments for videos
class ReplyComment(models.Model):
    # reply comment id
    reply_comment_id = models.CharField(blank=True, null=True, max_length=32)

    # reply comment creator
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='reply_comment_creator')
    
    # reply comment video
    reply_commented_video = models.ForeignKey(Video, on_delete=models.CASCADE, null=False, related_name='reply_commented_video')

    # comment parent
    comment_parent = models.ForeignKey(Comment, on_delete=models.CASCADE, null=False, related_name='comment_parent')

    # stats
    likes = models.BigIntegerField(default=0) # all likes under reply comment
    dislikes = models.BigIntegerField(default=0) # all dislikes under reply comment

    comment_text = models.TextField(max_length=5000) # comment text

    date_created = models.DateTimeField(auto_now_add=True, db_index=True) # date created
    date_created_without_time = models.DateField(auto_now_add=True, db_index=True) # date created for analytics

    def __str__(self):
        return self.comment_text


# Liked reply comment model 
class ReplyCommentLike(models.Model):
    liked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='liked_reply_comment_user')
    liked_reply_comment = models.ForeignKey(ReplyComment, on_delete=models.CASCADE, null=False, related_name='liked_reply_comment')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True) # date created


# Disliked reply comment model
class ReplyCommentDislike(models.Model):
    disliked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='disliked_reply_comment_user')
    disliked_reply_comment = models.ForeignKey(ReplyComment, on_delete=models.CASCADE, null=False, related_name='disliked_reply_comment')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True) # date created


# Article
class Article(models.Model):
    # article id
    article_id = models.CharField(blank=True, null=True, max_length=32)

    # article creator
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='article_creator')
    
    likes = models.BigIntegerField(default=0) # all likes under post (article)
    dislikes = models.BigIntegerField(default=0) # all dislikes upder post

    text = models.TextField(blank=True, null=True, max_length=1000000) # article text

    date_created = models.DateTimeField(auto_now_add=True, db_index=True) # date created
    date_created_without_time = models.DateField(auto_now_add=True, db_index=True) # date created for analytics

    def __str__(self):
        return self.article_id


# Liked article model
class ArticleLike(models.Model):
    liked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='liked_article_user')
    liked_article = models.ForeignKey(Article, on_delete=models.CASCADE, null=False, related_name='liked_article')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True) # date created
    date_created_without_time = models.DateField(auto_now_add=True, db_index=True) # date created for analytics


# Disliked article model
class ArticleDislike(models.Model):
    disliked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='disliked_article_user')
    disliked_article = models.ForeignKey(Article, on_delete=models.CASCADE, null=False, related_name='disliked_article')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True) # date created
    date_created_without_time = models.DateField(auto_now_add=True, db_index=True) # date created for analytics


# Actor model
class Actor(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    actor_id = models.CharField(blank=True, null=True, max_length=32, default=generate_id(32)) # actor id
    name = models.CharField(max_length=100) # actor name
    gender = models.CharField(max_length=50, null=True, choices=GENDER) # gender
    photo = models.ImageField(upload_to='avatars/', default="avatars/default/man.png") # actor photo file

    def __str__(self):
        return self.name


# Producer model
class Producer(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    producer_id = models.CharField(blank=True, null=True, max_length=32, default=generate_id(32)) # producer id
    name = models.CharField(max_length=100) # producer name
    gender = models.CharField(max_length=50, null=True, choices=GENDER) # gender
    photo = models.ImageField(upload_to='avatars/', default="avatars/default/man.png") # producer photo file

    def __str__(self):
        return self.name


# Writer model
class Writer(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    writer_id = models.CharField(blank=True, null=True, max_length=32, default=generate_id(32)) # writer id
    name = models.CharField(max_length=100) # writer name
    gender = models.CharField(max_length=50, null=True, choices=GENDER) # gender
    photo = models.ImageField(upload_to='avatars/', default="avatars/default/man.png") # writer photo file

    def __str__(self):
        return self.name


# Genre model
class Genre(models.Model):
    name = models.CharField(max_length=150) # genre name

    def __str__(self):
        return self.name


# Film model
class Film(models.Model):
    RATING = (
        ('0+', '0+'),
        ('6+', '6+'),
        ('12+', '12+'),
        ('16+', '16+'),
        ('18+', '18+')
    )

    film_id = models.CharField(blank=True, null=True, max_length=32) # film id
    
    film = models.FileField(upload_to='films/') # film file
    trailer = models.FileField(upload_to='trailers/') # film trailer file
    film_poster = models.ImageField(upload_to='film_posters/') # film poster file
    film_banner = models.ImageField(upload_to='film_banners/') # film banner file

    likes = models.BigIntegerField(default=0) # all likes under film
    dislikes = models.BigIntegerField(default=0) # all dislikes under film
    
    title = models.CharField(max_length=150) # film title
    price = models.FloatField(default=0) # film price
    running_time = models.CharField(max_length=150, default="0:00") # running time
    rating = models.CharField(max_length=50, null=True, choices=RATING) # film rating
    release_date = models.DateField() # film release date
    release_year = models.CharField(max_length=4, default="2021") # film release year
    main_genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=False) # film main genre
    description = models.TextField(blank=True, null=True, max_length=1000000) # film description

    date_created = models.DateTimeField(auto_now_add=True, db_index=True) # date created

    def __str__(self):
        return self.title


# Liked film model
class FilmLike(models.Model):
    liked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='liked_film_user')
    liked_film = models.ForeignKey(Film, on_delete=models.CASCADE, null=False, related_name='liked_film')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True) # date created


# Disliked film model
class FilmDislike(models.Model):
    disliked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='disliked_film_user')
    disliked_film = models.ForeignKey(Film, on_delete=models.CASCADE, null=False, related_name='disliked_film')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)


# Film & Producer
class FilmProducer(models.Model):
    producer_film = models.ForeignKey(Film, on_delete=models.CASCADE, null=False, related_name='producer_film')
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, null=False, related_name='producer')


# Film & Actor
class FilmActor(models.Model):
    actor_film = models.ForeignKey(Film, on_delete=models.CASCADE, null=False, related_name='actor_film')
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, null=False, related_name='actor')


# Film & Writer
class FilmWriter(models.Model):
    writer_film = models.ForeignKey(Film, on_delete=models.CASCADE, null=False, related_name='writer_film')
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE, null=False, related_name='writer')


# Film & Genre
class FilmGenre(models.Model):
    genre_film = models.ForeignKey(Film, on_delete=models.CASCADE, null=False, related_name='genre_film')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=False, related_name='genre')


# Buy film
class BuyFilm(models.Model):
    buy_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='buy_user')
    buy_film = models.ForeignKey(Film, on_delete=models.CASCADE, null=False, related_name='buy_film')
    
    
# Track model
class Track(models.Model):
    track_id = models.CharField(blank=True, null=True, max_length=32) # track id
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='track_creator') # creator
    
    track = models.FileField(upload_to='tracks/') # track file
    track_poster = models.ImageField(upload_to='track_posters/') # track poster file
    
    title = models.CharField(max_length=150) # track title
    
    auditions = models.BigIntegerField(default=0) # all track auditions
    
    date_created = models.DateTimeField(auto_now_add=True, db_index=True) # date created
    date_created_without_time = models.DateField(auto_now_add=True, db_index=True) # date created for analytics

    def __str__(self):
        return self.title


# Track listen model
class TrackListenModel(models.Model):
    listening_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='listening_user')
    listened_track = models.ForeignKey(Track, on_delete=models.CASCADE, null=False, related_name='listened_track')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True) # date created
    date_created_without_time = models.DateField(auto_now_add=True, db_index=True) # date created for analytics