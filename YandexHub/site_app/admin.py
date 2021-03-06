from django_summernote.admin import SummernoteModelAdmin
from django.contrib import admin
from .models import *


class VideoAdmin(SummernoteModelAdmin):
    description = '__all__'


class FilmAdmin(SummernoteModelAdmin):
    description = '__all__'


class CustomUserAdmin(SummernoteModelAdmin):
    description = '__all__'


class ArticleAdmin(SummernoteModelAdmin):
    text = '__all__'


admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(Subscribe)
# admin.site.register(Notification)
admin.site.register(Article, ArticleAdmin)
# admin.site.register(ArticleLike)
# admin.site.register(ArticleDislike)
admin.site.register(Video, VideoAdmin)
# admin.site.register(VideoViewModel)
# admin.site.register(SavedVideo)
# admin.site.register(Like)
# admin.site.register(Dislike)
admin.site.register(Track)
# admin.site.register(TrackListenModel)
admin.site.register(Comment)
# admin.site.register(CommentLike)
# admin.site.register(CommentDislike)
admin.site.register(ReplyComment)
# admin.site.register(ReplyCommentLike)
# admin.site.register(ReplyCommentDislike)
admin.site.register(Film, FilmAdmin)
admin.site.register(Actor)
admin.site.register(Producer)
admin.site.register(Writer)
admin.site.register(Genre)
admin.site.register(FilmProducer)
admin.site.register(FilmActor)
admin.site.register(FilmWriter)
admin.site.register(FilmGenre)
admin.site.register(BuyFilm)
