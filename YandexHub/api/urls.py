# DJANGO URLS
from django.urls import path

# API -> DRF
from .api import *

urlpatterns = [
    # site
    path('token/create/', CreateTokenApi.as_view()),
    path('site/', SiteStatsApi.as_view()),
    path('user/', UserInfoApi.as_view()),
    path('trending/', TrendingApi.as_view()),

    # video
    path('videos/', VideosApi.as_view()),
    path('videos/liked/', LikedVideosApi.as_view()),
    path('videos/disliked/', DislikedVideosApi.as_view()),
    path('videos/saved/', SavedVideosApi.as_view()),
    path('video/<str:pk>/info/', VideoApi.as_view()),
    path('video/<str:pk>/download/', DownloadVideoFile.as_view()),
    path('video/<str:pk>/banner/download/', DownloadBannerFile.as_view()),
    path('video/upload/', UploadVideoApi.as_view()),
    path('video/like/', LikeVideoApi.as_view()),
    path('video/dislike/', DislikeVideoApi.as_view()),
    path('video/save/', SaveVideoApi.as_view()),
    path('video/delete/', DeleteVideoApi.as_view()),
    path('video/stats/', VideoStatsApi.as_view()),

    # track
    path('track/delete/', DeleteTrackApi.as_view()),
    path('track/stats/', TrackStatsApi.as_view()),
    path('tracks/', TracksApi.as_view()),

    # comment
    path('comment/add/', AddCommentApi.as_view()),
    path('comment/like/', LikeCommentApi.as_view()),
    path('comment/dislike/', DislikeCommentApi.as_view()),
    path('comment/delete/', DeleteCommentApi.as_view()),

    # reply comment
    path('comment/reply/add/', AddReplyCommentApi.as_view()),
    path('comment/reply/like/', LikeReplyCommentApi.as_view()),
    path('comment/reply/dislike/', DislikeReplyCommentApi.as_view()),
    path('comment/reply/delete/', DeleteReplyCommentApi.as_view()),

    # film
    path('films/', FilmsApi.as_view()),
    path('film/<str:pk>/info/', FilmApi.as_view()),
    path('films/liked/', LikedFilmsApi.as_view()),
    path('films/disliked/', DislikedFilmsApi.as_view()),
    path('films/purchased/', PurchasedFilmsApi.as_view()),
    path('film/<str:pk>/banner/download/', DownloadFilmBannerFile.as_view()),
    path('film/<str:pk>/poster/download/', DownloadFilmPosterFile.as_view()),
    path('film/<str:pk>/trailer/download/', DownloadFilmTrailerFile.as_view()),
    path('film/<str:pk>/download/', DownloadFilmFile.as_view()),
    path('film/like/', LikeFilmApi.as_view()),
    path('film/dislike/', DislikeFilmApi.as_view()),
    path('buy/film/', BuyFilmApi.as_view()),

    # article
    path('article/<str:pk>/info/', ArticleApi.as_view()),
    path('article/delete/', DeleteArticleApi.as_view()),
    path('article/like/', LikeArticleApi.as_view()),
    path('article/dislike/', DislikeArticleApi.as_view()),
    path('article/stats/', ArticleStatsApi.as_view()),
    path('article/create/', CreateArticleApi.as_view()),

    # subscribe
    path('channel/subscribe/', SubscribeApi.as_view()),

    # notifications
    path('channel/notifications/', NotificationsApi.as_view()),
]
