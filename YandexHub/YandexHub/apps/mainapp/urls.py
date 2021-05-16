# DJANGO URLS
from django.urls import path
from django.contrib.auth import views as auth_views

# VIEWS
from .views import *

# API -> DRF
from .api import *

urlpatterns = [
    # home
    path('', HomeView.as_view(), name='main__page'),
    
    # auth
    path('sign/up/', SignUpView.as_view(), name='sign__up__page'),
    path('sign/in/', SignInView.as_view(), name='signin'),
    path('sign/out/', SignOutView.as_view(), name='sign__out__page'),

    # channel & user
    path('channel/<str:pk>/', ChannelView.as_view(), name='channel__page'),
    path('channel/<str:pk>/about/', AboutView.as_view(), name='about__channel'),
    path('channel/<str:pk>/community/', CommunityView.as_view(), name='community__page'),
    path('subscriptions/', SubscriptionsView.as_view(), name='subscriptions__page'),
    path('subscribers/', SubscribersView.as_view(), name='subscribers__page'),

    # donations
    path('connect/donations/', ConnectDonationsView.as_view(), name='connect__donations__page'),
    path('channel/<str:pk>/donation/', DonationView.as_view(), name='donation__page'),
    path('donations/manual/', DonationsManualView.as_view(), name='donations__manual__page'),

    # user settings
    path('settings/', SettingsView.as_view(), name='settings__page'),
    path('settings/channel/', ChannelSettingsView.as_view(), name='channel__settings__page'),
    path('settings/account/', AccountSettingsView.as_view(), name='account__settings__page'),
    path('settings/password/change/', ChangePasswordView.as_view(), name='change__password__page'),
    path('settings/email/change/', ChangeEmailView.as_view(), name='change__email__page'),

    # more
    path('more/', MoreView.as_view(), name="more__page"),
    path('about/', AboutProjectView.as_view(), name='about__page'),
    path('faq/', FAQView.as_view(), name='faq__page'),
    
    # api
    path('token/', ApiTokenView.as_view(), name="token__page"),
    path('api/', ApiView.as_view(), name="api_page"),
    path('api/token/create/', CreateTokenApi.as_view()),
    path('api/site/', SiteStatsApi.as_view()),
    path('api/user/', UserInfoApi.as_view()),
    path('api/trending/', TrendingApi.as_view()),
    
    path('api/videos/', VideosApi.as_view()),
    path('api/videos/liked/', LikedVideosApi.as_view()),
    path('api/videos/disliked/', DislikedVideosApi.as_view()),
    path('api/videos/saved/', SavedVideosApi.as_view()),
    path('api/video/<str:pk>/info/', VideoApi.as_view()),
    path('api/video/<str:pk>/download/', DownloadVideoFile.as_view()),
    path('api/video/<str:pk>/banner/download/', DownloadBannerFile.as_view()),
    path('api/video/upload/', UploadVideoApi.as_view()),
    
    path('api/films/', FilmsApi.as_view()),
    path('api/film/<str:pk>/info/', FilmApi.as_view()),
    path('api/films/liked/', LikedFilmsApi.as_view()),
    path('api/films/disliked/', DislikedFilmsApi.as_view()),
    path('api/films/purchased/', PurchasedFilmsApi.as_view()),
    path('api/film/<str:pk>/banner/download/', DownloadFilmBannerFile.as_view()),
    path('api/film/<str:pk>/poster/download/', DownloadFilmPosterFile.as_view()),
    path('api/film/<str:pk>/trailer/download/', DownloadFilmTrailerFile.as_view()),
    path('api/film/<str:pk>/download/', DownloadFilmFile.as_view()),
    
    # subscribe
    path('api/channel/subscribe/', SubscribeApi.as_view()),
    
    # notifications
    path('api/channel/notifications/', NotificationsApi.as_view()),
    
    # bot
    path('bot/', AlertBotView.as_view(), name='bot__page'),
    path('bot/manual/', AlertBotManualView.as_view(), name='bot__manual__page'),
    
    # article
    path('create/article/', CreateArticleView.as_view(), name='create__article__page'),
    path('article/<str:pk>/edit/', ChangeArticleView.as_view(), name='edit__article__page'),
    path('api/article/delete/', DeleteArticleApi.as_view()),
    path('api/article/like/', LikeArticleApi.as_view()),
    path('api/article/dislike/', DislikeArticleApi.as_view()),

    # analytics
    path('analytics/', AnalyticsView.as_view(), name="analytics__page"),
    path('analytics/dashboard/', DashboardView.as_view(), name="dashboard__page"),
    path('api/video/stats/', VideoStatsApi.as_view()),
    path('analytics/videos/', UserVideosView.as_view(), name='my__videos__page'),
    path('analytics/video/<str:pk>/info/', VideoStatsView.as_view(), name='video__stats__page'),
    path('analytics/video/<str:pk>/comments/', VideoCommentsView.as_view(), name='video__comments__page'),
    path('analytics/comment/<str:pk>/info/', CommentView.as_view(), name='comment__page'),
    path('analytics/articles/', UserArticlesView.as_view(), name='my__articles__page'),
    path('analytics/article/<str:pk>/info/', ArticleStatsView.as_view(), name='article__stats__page'),
    path('api/article/stats/', ArticleStatsApi.as_view()),

    # video
    path('create/video/', CreateVideoView.as_view(), name='create__video__page'),
    path('video/<str:pk>/', VideoView.as_view(), name='video__page'),
    path('video/<str:pk>/edit/', ChangeVideoView.as_view(), name='edit__video__page'),
    path('api/video/like/', LikeVideoApi.as_view()),
    path('api/video/dislike/',DislikeVideoApi.as_view()),
    path('api/video/save/', SaveVideoApi.as_view()),
    path('api/video/delete/', DeleteVideoApi.as_view()),

    # films
    path('films/', FilmsView.as_view(), name='films__page'),
    path('liked/films/', LikedFilmsView.as_view(), name='liked__films__page'),
    path('film/<str:pk>/', FilmView.as_view(), name='film__page'),
    path('api/film/like/', LikeFilmApi.as_view()),
    path('api/film/dislike/',DislikeFilmApi.as_view()),
    path('my/films/', UserFilmsView.as_view(), name='user__films__page'),
    path('api/buy/film/', BuyFilmApi.as_view()),
    path('actor/<str:pk>/', ActorView.as_view(), name='actor__page'),
    path('producer/<str:pk>/', ProducerView.as_view(), name='producer__page'),
    path('writer/<str:pk>/', WriterView.as_view(), name='writer__page'),
    path('genre/<str:pk>/', GenreView.as_view(), name='genre__page'),

    # comments
    path('api/comment/add/', AddCommentApi.as_view()),
    path('api/comment/like/', LikeCommentApi.as_view()),
    path('api/comment/dislike/', DislikeCommentApi.as_view()),
    path('api/comment/delete/', DeleteCommentApi.as_view()),
    
    # reply comments
    path('api/comment/reply/add/', AddReplyCommentApi.as_view()),
    path('api/comment/reply/like/', LikeReplyCommentApi.as_view()),
    path('api/comment/reply/dislike/', DislikeReplyCommentApi.as_view()),
    path('api/comment/reply/delete/', DeleteReplyCommentApi.as_view()),

    # other site pages
    path('saved/', SavedVideosView.as_view(), name='saved__videos__page'),
    path('liked/', LikedVideosView.as_view(), name='liked__videos__page'),
    path('history/', HistoryView.as_view(), name='history__page'),
    path('trending/', TrendingView.as_view(), name='trending__page'),

    # search
    path('results/search_query=<str:pk>/', SearchView.as_view(), name='search_page'),

    # reset password
    path('reset/password/', auth_views.PasswordResetView.as_view(template_name='password/reset_password.html'), name='reset_password'),
    path('reset/password/sent/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete')
]