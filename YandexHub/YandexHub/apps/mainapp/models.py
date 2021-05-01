from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # user id
    user_id = models.CharField(blank=True, null=True, max_length=24)
    
    # email
    email = models.EmailField(null=True, unique=True)

    # username
    username = models.CharField(blank=True, null=True, max_length=25)

    # user media
    avatar = models.ImageField(blank=True, null=True, upload_to = 'avatars/', default='avatars/default/default_avatar.png')
    banner = models.ImageField(blank=True, null=True, upload_to='users_banners/')
    
    # user stats
    all_views = models.BigIntegerField(default=0)
    all_subscribers = models.BigIntegerField(default=0)
    
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

class Video(models.Model):
    # video id
    video_id = models.CharField(blank=True, null=True, max_length=32)

    # creator
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='video_creator')

    # files
    video = models.FileField(upload_to='videos/')
    video_banner = models.ImageField(upload_to='video_banners/')

    # video stats
    views = models.BigIntegerField(default=0)
    likes = models.BigIntegerField(default=0)
    dislikes = models.BigIntegerField(default=0)
    comments = models.BigIntegerField(default=0)


    coefficient = models.FloatField(default=0)

    # video info
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True, max_length=1000000)

    # date created
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    def __str__(self):
        return self.title

class VideoViewModel(models.Model):
    watched_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='watched_user')
    watched_video = models.ForeignKey(Video, on_delete=models.CASCADE, null=False, related_name='watched_video')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

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


class Comment(models.Model):
    comment_id = models.CharField(blank=True, null=True, max_length=32)

    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='comment_creator')
    commented_video = models.ForeignKey(Video, on_delete=models.CASCADE, null=False, related_name='commented_video')

    likes = models.BigIntegerField(default=0)
    dislikes = models.BigIntegerField(default=0)
    replies = models.BigIntegerField(default=0)

    comment_text = models.TextField(max_length=5000)

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


class ReplyComment(models.Model):
    reply_comment_id = models.CharField(blank=True, null=True, max_length=32)

    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='reply_comment_creator')
    reply_commented_video = models.ForeignKey(Video, on_delete=models.CASCADE, null=False, related_name='reply_commented_video')
    comment_parent = models.ForeignKey(Comment, on_delete=models.CASCADE, null=False, related_name='comment_parent')

    likes = models.BigIntegerField(default=0)
    dislikes = models.BigIntegerField(default=0)
    
    comment_text = models.TextField(max_length=5000)

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


class Article(models.Model):
    # article id
    article_id = models.CharField(blank=True, null=True, max_length=32)

    # creator
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='article_creator')

    # article stats
    likes = models.BigIntegerField(default=0)
    dislikes = models.BigIntegerField(default=0)

    # article info
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
