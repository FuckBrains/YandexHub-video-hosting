# USER
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# DRF AUTH
import re
from rest_framework.authtoken.models import Token

# VIEWS
from django.views.generic import View, TemplateView, ListView

# HTTP 
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# DRF - status
from rest_framework import status

# MESSAGES
from django.contrib import messages

# MODELS
from .models import *
from django.db.models import Q

# DECORATORS
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# FORMS
from .forms import *

# DATE/TIME
from datetime import datetime, timedelta, date

# OS
from pathlib import Path

# HELPERS
from .helpers import random_list, generate_id, get_city_and_country_ip

# BOT
from .bot import YandexHubAlert

# site domain, used for telegram bot
DOMEN = 'http://127.0.0.1:8000/'

# Limitations
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.wmv', '.mov', '.3gp', '.flv', '.webm']
IMAGE_EXTENSIONS = ['.jpeg', '.jpg', '.gif', '.png', '.pict', '.ico', '.tiff', '.ai', '.webp', '.eps', '.cdr']
TRACK_EXTENSIONS = ['.wav', '.aif', '.mp3', '.mid']
MAX_IMAGE_SIZE = 7864320  # 7.5 MB
MAX_VIDEO_SIZE = 209715200  # 200 MB


# get recommendations on video page
def get_video_recommendations(channel, video):
    video_channel_recommendations = []
    for i in range(5):
        try:
            channel_video = Video.objects.filter(
                creator=channel).order_by('-date_created')[i]
            if channel_video == video:
                pass
            else:
                video_channel_recommendations.append(channel_video)
        except:
            pass

    video_recommendations = []
    for i in range(30):
        try:
            other_video = Video.objects.order_by(
                'likes', 'comments', 'views', 'date_created')[i]
            if other_video == video:
                pass
            else:
                video_recommendations.append(other_video)
        except:
            pass

    return list(set(video_channel_recommendations + random_list(video_recommendations)))


# get recommendations on film page
def get_film_recommendations(film):
    film_recommendations = []
    for i in range(30):
        try:
            other_film = Film.objects.order_by('-date_created')[i]
            if other_film == film:
                pass
            else:
                film_recommendations.append(other_film)
        except:
            pass

    return film_recommendations


# add coefficient for video
def coefficient_func(video):
    video.coefficient = (video.comments + video.likes) / (video.dislikes + 1)
    video.save()


# view function
def view_func(video, request):
    if request.user.is_authenticated:
        # maximum 10 views per day (one user)
        today = date.today()
        if VideoViewModel.objects.filter(watched_user=request.user, watched_video=video,
                                         date_created_without_time=today).count() < 10:
            VideoViewModel.objects.create(watched_user=request.user, watched_video=video)
            video.views += 1
            video.save()
            video.creator.all_views += 1
            video.creator.save()

        coefficient_func(video)  # coefficient function


# listen function
def listen_func(track, request):
    if request.user.is_authenticated:
        # maximum 10 views per day (one user)
        today = date.today()
        if TrackListenModel.objects.filter(listening_user=request.user, listened_track=track,
                                           date_created_without_time=today).count() < 10:
            TrackListenModel.objects.create(listening_user=request.user, listened_track=track)
            track.auditions += 1
            track.save()
            track.creator.all_auditions += 1
            track.creator.save()


#  home page
class HomeView(ListView):
    template_name = 'home.html'
    paginate_by = 20
    model = Video
    context_object_name = 'videos'

    def get_queryset(self):
        return Video.objects.all().order_by('-coefficient')  # filter by coefficient for tranding page

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['title'] = 'YandexHub'
        return context


# search video system
class SearchView(ListView):
    template_name = 'video/search/search.html'
    paginate_by = 10
    queryset = Video
    context_object_name = 'videos'

    def get_queryset(self):
        return Video.objects.filter(title__icontains=self.kwargs['pk']).order_by('-coefficient')

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['title'] = self.kwargs['pk']
        return context


# subscribers page
class SubscribersView(ListView):
    template_name = 'user/subscribers.html'
    paginate_by = 10
    queryset = Subscribe
    context_object_name = 'subscribers'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Subscribe.objects.filter(channel=self.request.user).order_by('-date_created')
        else:
            return Subscribe.objects.none()

    def get_context_data(self, **kwargs):
        context = super(SubscribersView, self).get_context_data(**kwargs)
        context['title'] = 'Subscribers 👱‍♂️'
        return context


# channel page
class ChannelView(ListView):
    template_name = 'user/channel.html'
    paginate_by = 10
    queryset = Video
    context_object_name = 'videos'

    def get_queryset(self):
        channel = CustomUser.objects.filter(user_id=self.kwargs['pk'])
        if channel:
            return Video.objects.filter(creator=channel[0]).order_by('-date_created')
        else:
            return Video.objects.none()

    def get_context_data(self, **kwargs):
        context = super(ChannelView, self).get_context_data(**kwargs)
        channel = CustomUser.objects.filter(user_id=self.kwargs['pk'])
        if channel:
            channel = channel[0]
            # find subscribe model
            if self.request.user.is_authenticated:
                subscribe = Subscribe.objects.filter(
                    subscriber=self.request.user, channel=channel)
            else:
                subscribe = None

            # find notification model
            if self.request.user.is_authenticated:
                notifications = Notification.objects.filter(
                    notification_channel=channel, notification_user=self.request.user)
            else:
                notifications = None

            context['notifications'] = notifications
            context['subscribe'] = subscribe
            context['title'] = channel.username
            context['channel'] = channel
            context['page'] = 'channel'
            return context
        else:
            # if channel not found
            context['error'] = True
            return context


# donation page
class DonationView(TemplateView):
    template_name = 'user/donations/donation.html'

    def get_context_data(self, **kwargs):
        context = super(DonationView, self).get_context_data(**kwargs)
        channel = CustomUser.objects.filter(user_id=self.kwargs['pk'])
        if channel:
            channel = channel[0]
            context['title'] = f'Support - {channel.username}'
            context['text'] = channel.donat_text
            context['wallet'] = channel.wallet
            context['url'] = f'{DOMEN}channel/{channel.user_id}/'
            context['channel'] = channel
            return context
        else:
            # if channel not found
            context['error'] = True
            return context


# connect donations
class ConnectDonationsView(TemplateView):
    template_name = 'user/donations/connect.html'

    def get_context_data(self, **kwargs):
        context = super(ConnectDonationsView, self).get_context_data(**kwargs)
        context['title'] = 'Connect donations 💰'
        return context

    @method_decorator(login_required)
    def post(self, request):
        try:
            wallet = request.POST['wallet']
            title = request.POST['title']
            if len(str(wallet)) != 0:
                if len(str(wallet)) == 16:
                    if len(str(title)) <= 60:
                        request.user.wallet = wallet
                        request.user.donat_text = title
                        request.user.save()

                        # YandexHub Alert
                        if request.user.telegram:
                            # send alert
                            message = YandexHubAlert(
                                f'Donations via YooMoney are successfully connected 🔮\n\n{get_city_and_country_ip(request)}',
                                request.user.telegram)
                            if message == 200:
                                pass
                            elif message == 400:
                                messages.error(self.request,
                                               '''An error occurred while sending the notification. Check the correctness of your Telegram ID by the <a style='cursor: pointer; color: #0D6EFD;' onclick='transition_link("/bot/")'>link</a> 🤖''')
                            else:
                                messages.error(self.request,
                                               '''An error occurred while sending a notification. You have blocked the bot from sending messages to fix this read the <a style='cursor: pointer; color: #0D6EFD;' onclick='transition_link("/bot/manual/")'>manual</a> 🤖''')
                        else:
                            pass

                        messages.success(request, 'Donations via YooMoney are successfully connected 🔮')
                        return redirect('connect__donations__page')
                    else:
                        messages.error(request, 'Maximum title length 60 characters 😳')
                        return redirect('connect__donations__page')
                else:
                    messages.error(request, 'Incorrect Wallet ID 😒')
                    return redirect('connect__donations__page')
            else:
                title = request.POST['title']
                request.user.wallet = None
                request.user.donat_text = title
                request.user.save()
                messages.success(request, 'Donations are successfully disabled 🤗')
                return redirect('connect__donations__page')
        except:
            return redirect('connect__donations__page')


# donations manual page
class DonationsManualView(TemplateView):
    template_name = 'user/donations/manual.html'

    def get_context_data(self, **kwargs):
        context = super(DonationsManualView, self).get_context_data(**kwargs)
        context['title'] = 'YooMoney donations - Manual 📋'
        return context


# about channel page
class AboutView(TemplateView):
    template_name = 'user/about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        channel = CustomUser.objects.filter(user_id=self.kwargs['pk'])
        if channel:
            channel = channel[0]
            # find subscribe model
            if self.request.user.is_authenticated:
                subscribe = Subscribe.objects.filter(subscriber=self.request.user.id, channel=channel)
            else:
                subscribe = None

            # find notification model
            if self.request.user.is_authenticated:
                notifications = Notification.objects.filter(notification_channel=channel,
                                                            notification_user=self.request.user)
            else:
                notifications = None

            context['title'] = f'About - {channel.username}'
            context['notifications'] = notifications
            context['subscribe'] = subscribe
            context['channel'] = channel
            context['page'] = 'about'
            return context
        else:
            # if channel not found
            context['error'] = True
            return context


# settings page
class SettingsView(TemplateView):
    template_name = 'user/settings/main.html'

    def get_context_data(self, **kwargs):
        context = super(SettingsView, self).get_context_data(**kwargs)
        context['title'] = 'Settings ⚙️'
        return context


# channel settings page
class ChannelSettingsView(TemplateView):
    template_name = 'user/settings/channel.html'

    def get_context_data(self, **kwargs):
        context = super(ChannelSettingsView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['title'] = 'Channel settings 👻'
            context['CustomUserTextArea'] = CustomUserTextArea(instance=self.request.user)
            return context
        else:
            context['title'] = 'Channel settings 👻'
            return context

    @method_decorator(login_required)
    def post(self, request):
        user = request.user
        try:
            _file = request.FILES['avatar']
            file_extension = Path(str(_file)).suffix
            if not file_extension in IMAGE_EXTENSIONS:
                messages.error(request,
                               'This file extension is not supported (<b>avatar</b>) 😑<br/>You can read more about supported extensions <a href="/faq/">here</a>.')
                return redirect('channel__settings__page')
            else:
                if _file.size > MAX_IMAGE_SIZE:
                    messages.error(request, 'The size of the photo should not exceed 7.5 MB. 💡')
                    return redirect('channel__settings__page')
                else:
                    user.avatar = _file
        except:
            pass

        try:
            _file = request.FILES['banner']
            file_extension = Path(str(_file)).suffix
            if not file_extension in IMAGE_EXTENSIONS:
                messages.error(request,
                               'This file extension is not supported (<b>banner</b>) 😑<br/>You can read more about supported extensions <a href="/faq/">here</a>.')
                return redirect('channel__settings__page')
            else:
                if _file.size > MAX_IMAGE_SIZE:
                    messages.error(request, 'The size of the photo should not exceed 7.5 MB. 💡')
                    return redirect('channel__settings__page')
                else:
                    user.banner = _file
        except:
            pass

        username = request.POST['username']
        if len(str(username).replace(' ', '')) != 0:
            user.username = username
        else:
            messages.error(request, 'Username cannot be empty 😦')
            return redirect('channel__settings__page')

        description = request.POST['description']
        if len(str(description)) > 5000:
            messages.error(request, 'Maximum description length 5000 characters 😯')
            return redirect('channel__settings__page')
        else:
            user.description = description

        location = request.POST['location']
        if len(str(location)) <= 150:
            user.location = location
        else:
            messages.error(request, 'Maximum location length 150 characters 😓')
            return redirect('channel__settings__page')

        contact_email = request.POST['contact_email']
        if len(str(contact_email)) <= 150:
            user.contact_email = contact_email
        else:
            messages.error(request, 'Maximum contact email length 150 characters 🤕')
            return redirect('channel__settings__page')

        vk_link = request.POST['vk_link']
        if len(str(vk_link)) <= 150:
            user.vk_link = vk_link
        else:
            messages.error(request, 'Maximum link length 150 characters 😕')
            return redirect('channel__settings__page')

        telegram_link = request.POST['telegram_link']
        if len(str(telegram_link)) <= 150:
            user.telegram_link = telegram_link
        else:
            messages.error(request, 'Maximum link length 150 characters 🥺')
            return redirect('channel__settings__page')

        instagram_link = request.POST['instagram_link']
        if len(str(instagram_link)) <= 150:
            user.instagram_link = instagram_link
        else:
            messages.error(request, 'Maximum link length 150 characters 😣')
            return redirect('channel__settings__page')

        facebook_link = request.POST['facebook_link']
        if len(str(facebook_link)) <= 150:
            user.facebook_link = facebook_link
        else:
            messages.error(request, 'Maximum link length 150 characters 😖')
            return redirect('channel__settings__page')

        twitter_link = request.POST['twitter_link']
        if len(str(twitter_link)) <= 150:
            user.twitter_link = twitter_link
        else:
            messages.error(request, 'Maximum link length 150 characters 🤨')
            return redirect('channel__settings__page')

        reddit_link = request.POST['reddit_link']
        if len(str(reddit_link)) <= 150:
            user.reddit_link = reddit_link
        else:
            messages.error(request, 'Maximum link length 150 characters 🥴')
            return redirect('channel__settings__page')

        website_link = request.POST['website_link']
        if len(str(website_link)) <= 150:
            user.website_link = website_link
        else:
            messages.error(request, 'Maximum link length 150 characters 🤒')
            return redirect('channel__settings__page')

        user.save()

        messages.success(request, 'Settings have been saved 👽')
        return redirect('channel__settings__page')


# account settings page
class AccountSettingsView(TemplateView):
    template_name = 'user/settings/account.html'

    def get_context_data(self, **kwargs):
        context = super(AccountSettingsView, self).get_context_data(**kwargs)
        context['title'] = 'Account settings 🤡'
        return context

    @method_decorator(login_required)
    def post(self, request):
        try:
            password = request.POST['password']
            email = request.user.email
            user_id = request.user.user_id
            telegram = request.user.telegram
            user = authenticate(email=email, password=password)

            if user is not None:
                # logout
                logout(request)
                user = CustomUser.objects.filter(email=email, user_id=user_id)
                if user.count() > 0:
                    # delete user model
                    user[0].delete()

                    # YandexHub Alert
                    if telegram:
                        # send alert
                        message = YandexHubAlert(
                            f'Your YandexHub account has been successfully deleted 💀\n\n{get_city_and_country_ip(request)}',
                            telegram)
                        if message == 'ok':
                            pass
                        else:
                            pass
                    else:
                        pass

                    messages.success(request, 'Account successfully deleted 😭')
                    return redirect('main__page')
                else:
                    messages.error(request, 'Fatal error 🤬')
                    return redirect('main__page')
            else:
                messages.error(request, 'Wrong password entered 😖')
                return redirect('account__settings__page')
        except:
            return redirect('account__settings__page')


# change password page
class ChangePasswordView(TemplateView):
    template_name = 'user/settings/password.html'

    def get_context_data(self, **kwargs):
        context = super(ChangePasswordView, self).get_context_data(**kwargs)
        context['title'] = 'Change password 🔒'
        return context

    @method_decorator(login_required)
    def post(self, request):
        try:
            password = request.POST['password']
            new_password = request.POST['new_password']
            confirm_new_password = request.POST['confirm_new_password']

            if new_password == confirm_new_password:
                if 7 < len(new_password) < 150 and 7 < len(str(new_password).replace(' ', '')) < 150:
                    email = request.user.email
                    user_id = request.user.user_id
                    telegram = request.user.telegram
                    user = authenticate(email=email, password=password)

                    if user is not None:
                        user.set_password(new_password)
                        user.save()

                        # logout
                        logout(request)

                        # YandexHub Alert
                        if telegram:
                            # send alert
                            message = YandexHubAlert(
                                f'Your password has been successfully changed 👻\n\n{get_city_and_country_ip(request)}',
                                telegram)
                            if message == 200:
                                pass
                            elif message == 400:
                                messages.error(self.request,
                                               '''An error occurred while sending the notification. Check the correctness of your Telegram ID by the <a style='cursor: pointer; color: #0D6EFD;' onclick='transition_link("/bot/")'>link</a> 🤖''')
                            else:
                                messages.error(self.request,
                                               '''An error occurred while sending a notification. You have blocked the bot from sending messages to fix this read the <a style='cursor: pointer; color: #0D6EFD;' onclick='transition_link("/bot/manual/")'>manual</a> 🤖''')
                        else:
                            pass

                        messages.success(request, 'Your password has been successfully changed 👻')
                        messages.success(request,
                                         '''After changing your password, you must re-enter your account using the <a style='cursor: pointer; color: #0D6EFD;' onclick='transition_link("/sign/in/")'>link</a> 📱''')
                        return redirect('main__page')
                    else:
                        messages.error(request, 'Wrong password entered 😖')
                        return redirect('change__password__page')
                else:
                    messages.error(request, 'Password cannot contain only spaces or be less than 8 characters 🧸')
                    return redirect('change__password__page')
            else:
                messages.error(request, 'Password mismatch 😿')
                return redirect('change__password__page')
        except:
            return redirect('change__password__page')


# change email page
class ChangeEmailView(TemplateView):
    template_name = 'user/settings/email.html'

    def get_context_data(self, **kwargs):
        context = super(ChangeEmailView, self).get_context_data(**kwargs)
        context['title'] = 'Change email ✉️'
        return context

    @method_decorator(login_required)
    def post(self, request):
        try:
            password = request.POST['password']
            new_email = request.POST['new_email']
            if len(str(new_email).replace(' ', '')) < 5:
                messages.error(request, 'Invalid email ☠️')
                return redirect('change__email__page')
            else:
                email = request.user.email
                telegram = request.user.telegram
                user = authenticate(email=email, password=password)

                if user is not None:
                    user.email = new_email
                    user.save()

                    # logout
                    logout(request)

                    # YandexHub Alert
                    if telegram:
                        # send alert
                        message = YandexHubAlert(
                            f'Your email has been successfully changed 🙃\n\n{get_city_and_country_ip(request)}',
                            telegram)
                        if message == 200:
                            pass
                        elif message == 400:
                            messages.error(self.request,
                                           '''An error occurred while sending the notification. Check the correctness of your Telegram ID by the <a style='cursor: pointer; color: #0D6EFD;' onclick='transition_link("/bot/")'>link</a> 🤖''')
                        else:
                            messages.error(self.request,
                                           '''An error occurred while sending a notification. You have blocked the bot from sending messages to fix this read the <a style='cursor: pointer; color: #0D6EFD;' onclick='transition_link("/bot/manual/")'>manual</a> 🤖''')
                    else:
                        pass

                    messages.success(request, 'Your email has been successfully changed 🙃')
                    messages.success(request,
                                     '''After changing your email, you must re-enter your account using the <a style='cursor: pointer; color: #0D6EFD;' onclick='transition_link("/sign/in/")'>link</a> 📱''')
                    return redirect('main__page')

                else:
                    messages.error(request, 'Wrong password entered 😖')
                    return redirect('change__email__page')
        except:
            return redirect('change__email__page')


# video page
class VideoView(ListView):
    template_name = 'video/video.html'
    paginate_by = 10
    queryset = Comment
    context_object_name = 'comments'

    def get_queryset(self, **kwargs):
        video = Video.objects.filter(video_id=self.kwargs['pk'])
        if video:
            return Comment.objects.filter(commented_video=video[0]).order_by('-likes')
        else:
            return Comment.objects.none()

    def get_context_data(self, **kwargs):
        context = super(VideoView, self).get_context_data(**kwargs)
        video = Video.objects.filter(video_id=self.kwargs['pk'])
        if video:
            video = video[0]
            view_func(video, self.request)  # view video

            context['title'] = video.title
            context['video'] = video
            context['video_recommendations'] = get_video_recommendations(video.creator, video)
            if self.request.user.is_authenticated:
                context['subscribe'] = Subscribe.objects.filter(subscriber=self.request.user, channel=video.creator)
                context['saved_video'] = SavedVideo.objects.filter(saved_user=self.request.user, saved_video=video)
                context['liked'] = Like.objects.filter(liked_user=self.request.user, liked_video=video)
                context['disliked'] = Dislike.objects.filter(disliked_user=self.request.user, disliked_video=video)

            return context
        else:
            # if video not found
            context['error'] = True
            return context


# create video page
class CreateVideoView(TemplateView):
    template_name = 'video/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateVideoView, self).get_context_data(**kwargs)
        context['title'] = 'Upload video 📲'
        context['VideoTextArea'] = VideoTextArea()
        return context

    @method_decorator(login_required)
    def post(self, request):
        try:
            if request.POST['title'] is None or len(request.POST['title'].replace(' ', '')) == 0:
                messages.error(request, 'Video title cannot contain spaces 😈')
                return redirect('create__video__page')
            else:
                if 'video' not in request.FILES or 'video_banner' not in request.FILES:
                    messages.error(request, 'You must upload <b>video</b> and <b>banner</b> 😖')
                    return redirect('create__video__page')
                else:
                    video = request.FILES['video']
                    file_extension = Path(str(video)).suffix
                    if not file_extension in VIDEO_EXTENSIONS:
                        messages.error(request,
                                       'This file extension is not supported (<b>video</b>) 😑<br/>You can read more about supported extensions <a href="/faq/">here</a>.')
                        return redirect('create__video__page')
                    else:
                        if video.size > MAX_VIDEO_SIZE:
                            messages.error(request, 'The size of the video should not exceed 200 MB. 💡')
                            return redirect('create__video__page')

                    banner = request.FILES['video_banner']
                    file_extension = Path(str(banner)).suffix
                    if not file_extension in IMAGE_EXTENSIONS:
                        messages.error(request,
                                       'This file extension is not supported (<b>banner</b>) 😑<br/>You can read more about supported extensions <a href="/faq/">here</a>.')
                        return redirect('create__video__page')
                    else:
                        if banner.size > MAX_IMAGE_SIZE:
                            messages.error(request, 'The size of the photo should not exceed 7.5 MB. 💡')
                            return redirect('create__video__page')

                    title = request.POST['title']
                    if len(str(title)) > 150:
                        messages.error(request, 'Maximum title length 150 characters 🥴')
                        return redirect('create__video__page')

                    description = request.POST['description']
                    if len(str(description)) > 50000:
                        messages.error(request, 'Maximum description length 50000 characters 🥴')
                        return redirect('create__video__page')

                    # maximum 5 videos per day (one user)
                    today = date.today()
                    if Video.objects.filter(creator=request.user, date_created_without_time=today).count() < 5:
                        # create video model
                        video = Video.objects.create(creator=request.user, video=video, video_id=generate_id(32),
                                                     video_banner=banner, title=title, description=description)
                        video.save()

                        # send notifications
                        subscribers = Notification.objects.filter(notification_channel=video.creator)
                        for i in subscribers:
                            if i.notification_user.telegram:
                                YandexHubAlert(
                                    f'A new video has been released on the {video.creator.username} channel 🥳\n{DOMEN}video/{video.video_id}/',
                                    i.notification_user.telegram)

                        messages.success(request, f'You have successfully posted a video: <b>{video.title}</b> 🤩')
                        return redirect('video__page', video.video_id)
                    else:
                        messages.success(request, 'You have exceeded the videos limit for one day today 😥')
                        return redirect('main__page')
        except:
            return redirect('create__video__page')


# change video page
class ChangeVideoView(TemplateView):
    template_name = 'video/change.html'

    def get_context_data(self, **kwargs):
        context = super(ChangeVideoView, self).get_context_data(**kwargs)
        video = Video.objects.filter(video_id=self.kwargs['pk'])
        if video:
            video = video[0]
            context['video'] = video
            context['title'] = f'Change - {video.title}'
            context['VideoTextArea'] = VideoTextArea(instance=video)
            return context
        else:
            # if video not found
            context['error'] = True
            return context

    @method_decorator(login_required)
    def post(self, request, **kwargs):
        try:
            video = Video.objects.get(video_id=self.kwargs['pk'])
            if video.creator == self.request.user:
                try:
                    banner = request.FILES['video_banner']
                    file_extension = Path(str(banner)).suffix
                    if not file_extension in IMAGE_EXTENSIONS:
                        messages.error(request,
                                       'This file extension is not supported (<b>banner</b>) 😑<br/>You can read more about supported extensions <a href="/faq/">here</a>.')
                        return redirect('edit__video__page', video.video_id)
                    else:
                        if banner.size > MAX_IMAGE_SIZE:
                            messages.error(request,
                                           'The size of the photo should not exceed 7.5 MB. 💡<br/>You can read more about images size <a href="/faq/">here</a>.')
                            return redirect('edit__video__page', video.video_id)
                        else:
                            video.video_banner = banner
                except:
                    pass

                title = request.POST['title']
                if len(str(title)) > 150:
                    messages.error(request, 'Maximum title length 150 characters 🥴')
                    return redirect('edit__video__page', video.video_id)
                else:
                    video.title = title

                description = request.POST['description']
                if len(str(title)) > 150:
                    messages.error(request, 'Maximum description length 5000 characters 🥴')
                    return redirect('edit__video__page', video.video_id)
                else:
                    video.description = description

                video.save()

                # alert
                messages.success(request, f'You have successfully changed the video: <b>{video.title}</b> 😍')
                return redirect('video__page', video.video_id)

            else:
                # alert
                messages.error(request, f'You are not the author of the video: <b>{video.title}</b> 😡')
                return redirect('main__page')
        except:
            return redirect('main__page')


# alert bot page
class AlertBotView(TemplateView):
    template_name = 'user/bot/main.html'

    def get_context_data(self, **kwargs):
        context = super(AlertBotView, self).get_context_data(**kwargs)
        context['title'] = 'YandexHub Alert Bot 🤖'
        return context

    @method_decorator(login_required)
    def post(self, request):
        try:
            telegram = request.POST['telegram']
            if len(str(telegram)) != 0:
                if len(str(telegram)) < 25:
                    message = YandexHubAlert('YandexHub Alert successfully connected 👻', telegram)
                    if message == 200:
                        request.user.telegram = telegram
                        request.user.save()
                        messages.success(request, 'Your Telegram ID has been successfully saved 🤖')
                        return redirect('bot__page')
                    elif message == 400:
                        messages.error(request,
                                       '''An error occurred while sending the notification. Check the correctness of your Telegram ID by the <a style='cursor: pointer; color: #0D6EFD;' onclick='transition_link("/bot/manual/")'>link</a> 🤖''')
                        return redirect('bot__page')
                    else:
                        messages.error(request,
                                       '''An error occurred while sending a notification. You have blocked the bot from sending messages to fix this read the <a style='cursor: pointer; color: #0D6EFD;' onclick='transition_link("/bot/manual/")'>manual</a> 🤖''')
                        return redirect('bot__page')
                else:
                    messages.error(request,
                                   '''An error occurred while sending the notification. Check the correctness of your Telegram ID by the <a style='cursor: pointer; color: #0D6EFD;' onclick='transition_link("/bot/manual/")'>link</a> 🤖''')
                    return redirect('bot__page')
            else:
                YandexHubAlert(f'YandexHub Alert successfully disabled 🤗\n\n{get_city_and_country_ip(request)}',
                               request.user.telegram)
                request.user.telegram = None
                request.user.save()
                messages.success(request, 'YandexHub Alert successfully disabled 🤗')
                return redirect('bot__page')
        except:
            return redirect('bot__page')


# alert bot manual page
class AlertBotManualView(TemplateView):
    template_name = 'user/bot/manual.html'

    def get_context_data(self, **kwargs):
        context = super(AlertBotManualView, self).get_context_data(**kwargs)
        context['title'] = 'YandexHub Alert Bot - Manual 📋'
        return context


# community page
class CommunityView(ListView):
    template_name = 'user/community/community.html'
    paginate_by = 10
    model = Article
    context_object_name = 'articles'

    def get_queryset(self, **kwargs):
        channel = CustomUser.objects.filter(user_id=self.kwargs['pk'])
        if channel:
            return Article.objects.filter(creator=channel[0]).order_by('-date_created')
        else:
            return Article.objects.none()

    def get_context_data(self, **kwargs):
        context = super(CommunityView, self).get_context_data(**kwargs)
        channel = CustomUser.objects.filter(user_id=self.kwargs['pk'])
        if channel:
            channel = channel[0]
            # find subscribe model 
            if self.request.user.is_authenticated:
                subscribe = Subscribe.objects.filter(subscriber=self.request.user, channel=channel)
            else:
                subscribe = None

            # find notification model 
            if self.request.user.is_authenticated:
                notifications = Notification.objects.filter(notification_channel=channel,
                                                            notification_user=self.request.user)
            else:
                notifications = None

            context['title'] = f'Community - {channel.username}'
            context['notifications'] = notifications
            context['subscribe'] = subscribe
            context['channel'] = channel
            context['page'] = 'community'
            return context
        else:
            # if channel not found
            context['error'] = True
            return context


# create article page
class CreateArticleView(TemplateView):
    template_name = 'user/community/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateArticleView, self).get_context_data(**kwargs)
        context['title'] = 'Create article 📄'
        context['ArticleTextArea'] = ArticleTextArea()
        return context

    def post(self, request):
        try:
            if len(str(request.POST['text']).replace(' ', '')) == 0:
                messages.error(request, 'Article text cannot contain spaces 😈')
                return redirect('create__article__page')
            else:
                text = request.POST['text']
                if len(str(text)) > 1000000:
                    messages.error(request, 'Maximum text length 1000000 characters 🥴')
                    return redirect('create__article__page')

                # maximum 10 articles per day (one user)
                today = date.today()
                if Article.objects.filter(creator=request.user, date_created_without_time=today).count() < 10:
                    # create article model
                    article = Article.objects.create(creator=request.user, article_id=generate_id(32), text=text)
                    article.save()

                    messages.success(request, 'You have successfully posted a article 🤪')
                    return redirect('community__page', request.user.user_id)
                else:
                    messages.error(request, 'You have exceeded the articles limit for one day today 😥')
                    return redirect('community__page', request.user.user_id)
        except:
            return redirect('main__page')


# change article page 
class ChangeArticleView(TemplateView):
    template_name = 'user/community/change.html'

    def get_context_data(self, **kwargs):
        context = super(ChangeArticleView, self).get_context_data(**kwargs)
        article = Article.objects.filter(article_id=self.kwargs['pk'])
        if article:
            article = article[0]
            context['article'] = article
            context['title'] = 'Change article 🛠'
            context['ArticleTextArea'] = ArticleTextArea(instance=article)
            return context
        else:
            # if article not found
            context['error'] = True
            return context

    def post(self, request, **kwargs):
        try:
            article = Article.objects.get(article_id=self.kwargs['pk'])
            if article.creator == self.request.user:
                text = request.POST['text']
                if len(str(text)) > 5000:
                    messages.error(request, 'Maximum text length 5000 characters 🥴')
                    return redirect('edit__article__page', article.article_id)

                article.text = text
                article.save()

                # alert
                messages.success(request, f'You have successfully changed the article 😍')
                return redirect('community__page', article.creator.user_id)

            else:
                # alert
                messages.error(request, f'You are not the author of the article 😡')
                return redirect('main__page')
        except:
            return redirect('main__page')


# saved videos page
class SavedVideosView(ListView):
    template_name = 'user/video/saved.html'
    paginate_by = 10
    queryset = SavedVideo
    context_object_name = 'videos'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return SavedVideo.objects.filter(saved_user=self.request.user).order_by('-date_created')
        else:
            return SavedVideo.objects.none()

    def get_context_data(self, **kwargs):
        context = super(SavedVideosView, self).get_context_data(**kwargs)
        context['title'] = 'Saved videos 💾'
        return context


# liked videos page
class LikedVideosView(ListView):
    template_name = 'user/video/liked.html'
    paginate_by = 10
    queryset = Like
    context_object_name = 'videos'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Like.objects.filter(liked_user=self.request.user).order_by('-date_created')
        else:
            return Like.objects.none()

    def get_context_data(self, **kwargs):
        context = super(LikedVideosView, self).get_context_data(**kwargs)
        context['title'] = 'Liked videos ❤️'
        return context


# history page
class HistoryView(ListView):
    template_name = 'user/video/history.html'
    paginate_by = 10
    queryset = VideoViewModel
    context_object_name = 'videos'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return VideoViewModel.objects.filter(watched_user=self.request.user).order_by('-date_created')
        else:
            return VideoViewModel.objects.none()

    def get_context_data(self, **kwargs):
        context = super(HistoryView, self).get_context_data(**kwargs)
        context['title'] = 'Watch history 🕓'
        return context


# trending page
class TrendingView(ListView):
    template_name = 'video/other/trending.html'
    paginate_by = 100
    queryset = Video
    context_object_name = 'videos'

    def get_queryset(self):
        tranding_time = datetime.utcnow() - timedelta(days=2)
        videos = []
        for i in range(100):
            try:
                video = \
                Video.objects.filter(~Q(coefficient=0.0), date_created__gt=tranding_time).order_by('-coefficient')[i]
                videos.append(video)
            except:
                break

        return videos

    def get_context_data(self, **kwargs):
        context = super(TrendingView, self).get_context_data(**kwargs)
        context['title'] = 'Trending videos 📈'
        return context


# subscriptions page
class SubscriptionsView(TemplateView):
    template_name = 'user/other/subscriptions.html'

    def get_context_data(self, **kwargs):
        context = super(SubscriptionsView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            n = 0
            videos = []
            for i in Subscribe.objects.filter(subscriber=self.request.user):
                for j in Video.objects.filter(creator=i.channel).order_by('-date_created'):
                    videos.append(j)

                n += 1
                if n > 100:
                    break
        else:
            videos = []

        context['title'] = 'Subscriptions 🎞'
        context['videos'] = videos
        return context


# analytics
class AnalyticsView(TemplateView):
    template_name = 'user/analytics/analytics.html'

    def get_context_data(self, **kwargs):
        context = super(AnalyticsView, self).get_context_data(**kwargs)
        context['title'] = 'Analytics 🧐'
        return context


# dashboard
class DashboardView(TemplateView):
    template_name = 'user/analytics/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['title'] = 'Dashboard 📈'
        return context


# user videos page 
class UserVideosView(ListView):
    template_name = 'user/analytics/videos/videos.html'
    paginate_by = 10
    queryset = Video
    context_object_name = 'videos'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Video.objects.filter(creator=self.request.user).order_by('-date_created')
        else:
            return Video.objects.none()

    def get_context_data(self, **kwargs):
        context = super(UserVideosView, self).get_context_data(**kwargs)
        context['title'] = 'Your videos 🎥'
        return context


# video comments page 
class VideoCommentsView(ListView):
    template_name = 'user/analytics/videos/comments.html'
    paginate_by = 25
    queryset = Comment
    context_object_name = 'comments'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            video = Video.objects.filter(video_id=self.kwargs['pk'])
            if video:
                return Comment.objects.filter(commented_video=video[0]).order_by('-date_created')
            else:
                return Comment.objects.none()
        else:
            return Comment.objects.none()

    def get_context_data(self, **kwargs):
        context = super(VideoCommentsView, self).get_context_data(**kwargs)
        video = Video.objects.filter(video_id=self.kwargs['pk'])
        if video:
            video = video[0]
            context['title'] = 'Video comments 📝'
            context['video'] = video
            return context
        else:
            # if video not found
            context['error'] = True
            return context


# comment page 
class CommentView(ListView):
    template_name = 'user/analytics/videos/comment.html'
    paginate_by = 25
    queryset = ReplyComment
    context_object_name = 'comments'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            comment = Comment.objects.filter(comment_id=self.kwargs['pk'])
            if comment:
                return ReplyComment.objects.filter(comment_parent=comment[0]).order_by('-date_created')
            else:
                return ReplyComment.objects.none()
        else:
            return ReplyComment.objects.none()

    def get_context_data(self, **kwargs):
        context = super(CommentView, self).get_context_data(**kwargs)
        comment = Comment.objects.filter(comment_id=self.kwargs['pk'])
        if comment:
            context['title'] = 'Video comments 📝'
            context['comment'] = comment[0]
            return context
        else:
            # if comment not found
            context['error'] = True
            return context


# video stats page
class VideoStatsView(TemplateView):
    template_name = 'user/analytics/videos/video.html'

    def get_context_data(self, **kwargs):
        context = super(VideoStatsView, self).get_context_data(**kwargs)
        video = Video.objects.filter(video_id=self.kwargs['pk'])
        if video:
            video = video[0]
            context['title'] = video.title
            context['video'] = video
            return context
        else:
            # if video not found
            context['error'] = True
            return context


# user articles page 
class UserArticlesView(ListView):
    template_name = 'user/analytics/articles/articles.html'
    paginate_by = 10
    queryset = Article
    context_object_name = 'articles'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Article.objects.filter(creator=self.request.user).order_by('-date_created')
        else:
            return Article.objects.none()

    def get_context_data(self, **kwargs):
        context = super(UserArticlesView, self).get_context_data(**kwargs)
        context['title'] = 'Your articles 📜'
        return context


# article stats page
class ArticleStatsView(TemplateView):
    template_name = 'user/analytics/articles/article.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleStatsView, self).get_context_data(**kwargs)
        article = Article.objects.filter(article_id=self.kwargs['pk'])
        if article:
            context['title'] = article[0].text
            context['article'] = article[0]
            return context
        else:
            # if article not found
            context['error'] = True
            return context


# actor page
class ActorView(TemplateView):
    template_name = 'film/actor.html'

    def get_context_data(self, **kwargs):
        context = super(ActorView, self).get_context_data(**kwargs)
        actor = Actor.objects.filter(actor_id=self.kwargs['pk'])
        if actor:
            actor = actor[0]
            context['title'] = actor.name
            context['actor'] = actor
            return context
        else:
            # if actor not found
            context['error'] = True
            return context


# producer page
class ProducerView(TemplateView):
    template_name = 'film/producer.html'

    def get_context_data(self, **kwargs):
        context = super(ProducerView, self).get_context_data(**kwargs)
        producer = Producer.objects.filter(producer_id=self.kwargs['pk'])
        if producer:
            producer = producer[0]
            context['title'] = producer.name
            context['producer'] = producer
            return context
        else:
            # if producer not found
            context['error'] = True
            return context


# writer page
class WriterView(TemplateView):
    template_name = 'film/writer.html'

    def get_context_data(self, **kwargs):
        context = super(WriterView, self).get_context_data(**kwargs)
        writer = Writer.objects.filter(writer_id=self.kwargs['pk'])
        if writer:
            writer = writer[0]
            context['title'] = writer.name
            context['writer'] = writer
            return context
        else:
            # if writer not found
            context['error'] = True
            return context


# genre page
class GenreView(ListView):
    template_name = 'film/genre.html'
    paginate_by = 20
    model = Film
    context_object_name = 'films'

    def get_queryset(self):
        genre = Genre.objects.filter(name=self.kwargs['pk'])
        if genre:
            return Film.objects.filter(main_genre=genre[0])
        else:
            return Film.objects.none()

    def get_context_data(self, **kwargs):
        context = super(GenreView, self).get_context_data(**kwargs)
        genre = Genre.objects.filter(name=self.kwargs['pk'])
        if genre:
            genre = genre[0]
            context['title'] = genre.name
            context['genre'] = genre
            return context
        else:
            # if genre not found
            context['error'] = True
            return context


# films page
class FilmsView(ListView):
    template_name = 'film/films.html'
    paginate_by = 20
    model = Film
    context_object_name = 'films'

    def get_context_data(self, **kwargs):
        context = super(FilmsView, self).get_context_data(**kwargs)
        context['title'] = 'Films 🎥'
        return context


# user films page
class UserFilmsView(TemplateView):
    template_name = 'film/user/films.html'

    def get_context_data(self, **kwargs):
        context = super(UserFilmsView, self).get_context_data(**kwargs)
        context['title'] = 'Your films 🎥'
        return context


# film page
class FilmView(TemplateView):
    template_name = 'film/film.html'

    def get_context_data(self, **kwargs):
        context = super(FilmView, self).get_context_data(**kwargs)
        film = Film.objects.filter(film_id=self.kwargs['pk'])
        if film:
            film = film[0]
            # find buy model 
            if self.request.user.is_authenticated:
                buy = BuyFilm.objects.filter(buy_film=film, buy_user=self.request.user)
            else:
                buy = None

            context['title'] = f'{film.title}'
            context['buy'] = buy
            context['film'] = film
            context['film_recommendations'] = get_film_recommendations(film)

            if self.request.user.is_authenticated:
                context['liked'] = FilmLike.objects.filter(liked_user=self.request.user, liked_film=film)
                context['disliked'] = FilmDislike.objects.filter(disliked_user=self.request.user, disliked_film=film)

            return context
        else:
            # if film not found
            context['error'] = True
            return context


# liked films page
class LikedFilmsView(ListView):
    template_name = 'film/user/liked.html'
    paginate_by = 10
    queryset = FilmLike
    context_object_name = 'films'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return FilmLike.objects.filter(liked_user=self.request.user).order_by('-date_created')
        else:
            return FilmLike.objects.none()

    def get_context_data(self, **kwargs):
        context = super(LikedFilmsView, self).get_context_data(**kwargs)
        context['title'] = 'Liked films ❤️'
        return context


# more page
class MoreView(TemplateView):
    template_name = 'more/main.html'

    def get_context_data(self, **kwargs):
        context = super(MoreView, self).get_context_data(**kwargs)
        context['title'] = 'More 🧻'
        return context


# about project page
class AboutProjectView(TemplateView):
    template_name = 'more/about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutProjectView, self).get_context_data(**kwargs)
        context['title'] = 'About 🥴'
        return context


# FAQ page
class FAQView(TemplateView):
    template_name = 'more/faq.html'

    def get_context_data(self, **kwargs):
        context = super(FAQView, self).get_context_data(**kwargs)
        context['title'] = 'FAQ 📃'
        context['domen'] = DOMEN
        return context


# Api token page
class ApiTokenView(TemplateView):
    template_name = 'more/api/token.html'

    def get_context_data(self, **kwargs):
        context = super(ApiTokenView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            token = Token.objects.filter(user=self.request.user)
            if not token:
                token = None
            else:
                token = token[0]
        else:
            token = None

        context['title'] = 'Api token 🔑'
        context['token'] = token
        return context


# api page
class ApiView(TemplateView):
    template_name = 'more/api/main.html'

    def get_context_data(self, **kwargs):
        context = super(ApiView, self).get_context_data(**kwargs)
        context['title'] = 'Api ⚡️'
        context['domen'] = DOMEN
        return context


#  music page
class MusicView(ListView):
    template_name = 'music/main.html'
    paginate_by = 20
    model = Track
    context_object_name = 'tracks'

    def get_queryset(self):
        return Track.objects.all().order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super(MusicView, self).get_context_data(**kwargs)
        context['title'] = 'Music 🎧'
        return context


# tracks page
class TracksView(ListView):
    template_name = 'music/tracks.html'
    paginate_by = 20
    model = Track
    context_object_name = 'tracks'

    def get_queryset(self, **kwargs):
        user = CustomUser.objects.filter(user_id=self.kwargs['pk'])
        if user:
            return Track.objects.filter(creator=user[0]).order_by('-date_created')
        else:
            return Track.objects.none()

    def get_context_data(self, **kwargs):
        context = super(TracksView, self).get_context_data(**kwargs)
        user = CustomUser.objects.filter(user_id=self.kwargs['pk'])
        if user:
            user = user[0]
            context['title'] = f'Tracks - {user.username}'
            context['user'] = user
            return context
        else:
            # if channel not found
            context['error'] = True
            return context


# track page
class TrackView(TemplateView):
    template_name = 'music/track.html'

    def get_context_data(self, **kwargs):
        context = super(TrackView, self).get_context_data(**kwargs)
        track = Track.objects.filter(track_id=self.kwargs['pk'])
        if track:
            track = track[0]
            listen_func(track, self.request)  # listen function
            context['title'] = f'{track.title}'
            context['track'] = track
            return context
        else:
            # if track not found
            context['error'] = True
            return context


# change track page
class ChangeTrackView(TemplateView):
    template_name = 'music/edit.html'

    def get_context_data(self, **kwargs):
        context = super(ChangeTrackView, self).get_context_data(**kwargs)
        track = Track.objects.filter(track_id=self.kwargs['pk'])
        if track:
            track = track[0]
            context['track'] = track
            context['title'] = f'Change - {track.title}'
            return context
        else:
            # if track not found
            context['error'] = True
            return context

    @method_decorator(login_required)
    def post(self, request, **kwargs):
        try:
            track = Track.objects.get(track_id=self.kwargs['pk'])

            if track.creator == self.request.user:
                try:
                    poster = request.FILES['track_poster']
                    file_extension = Path(str(poster)).suffix
                    if not file_extension in IMAGE_EXTENSIONS:
                        messages.error(request,
                                       'This file extension is not supported (<b>poster</b>) 😑<br/>You can read more about supported extensions <a href="/faq/">here</a>.')
                        return redirect('edit__track__page', track.track_id)
                    else:
                        if poster.size > MAX_IMAGE_SIZE:
                            messages.error(request,
                                           'The size of the photo should not exceed 7.5 MB. 💡<br/>You can read more about images size <a href="/faq/">here</a>.')
                            return redirect('edit__track__page', track.track_id)
                        else:
                            track.track_poster = poster
                except:
                    pass

                title = request.POST['title']
                if len(str(title)) > 150:
                    messages.error(request, 'Maximum title length 150 characters 🥴')
                    return redirect('edit__track__page', track.track_id)
                else:
                    track.title = title

                track.save()

                # alert
                messages.success(request, f'You have successfully changed the track: <b>{track.title}</b> 😍')
                return redirect('track__page', track.track_id)
            else:
                # alert
                messages.error(request, f'You are not the author of the track: <b>{track.title}</b> 😡')
                return redirect('main__page')
        except:
            return redirect('main__page')


# user tracks page 
class UserTracksView(ListView):
    template_name = 'user/analytics/tracks/tracks.html'
    paginate_by = 10
    queryset = Track
    context_object_name = 'tracks'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Track.objects.filter(creator=self.request.user).order_by('-date_created')
        else:
            return Track.objects.none()

    def get_context_data(self, **kwargs):
        context = super(UserTracksView, self).get_context_data(**kwargs)
        context['title'] = 'Your track 📀'
        return context


# track stats page
class TrackStatsView(TemplateView):
    template_name = 'user/analytics/tracks/track.html'

    def get_context_data(self, **kwargs):
        context = super(TrackStatsView, self).get_context_data(**kwargs)
        track = Track.objects.filter(track_id=self.kwargs['pk'])
        if track:
            track = track[0]
            context['title'] = track.title
            context['track'] = track
            return context
        else:
            # if track not found
            context['error'] = True
            return context


# upload track page
class UploadTrackView(TemplateView):
    template_name = 'music/upload.html'

    def get_context_data(self, **kwargs):
        context = super(UploadTrackView, self).get_context_data(**kwargs)
        context['title'] = 'Upload track 🎤'
        return context

    @method_decorator(login_required)
    def post(self, request):
        try:
            if request.POST['title'] is None or len(request.POST['title'].replace(' ', '')) == 0:
                messages.error(request, 'Track title cannot contain spaces 😈')
                return redirect('upload__track__page')
            else:
                if 'track' not in request.FILES or 'track_poster' not in request.FILES:
                    messages.error(request, 'You must upload <b>track</b> and <b>track poster</b> 😖')
                    return redirect('upload__track__page')
                else:
                    track = request.FILES['track']
                    file_extension = Path(str(track)).suffix
                    if not file_extension in TRACK_EXTENSIONS:
                        messages.error(request,
                                       'This file extension is not supported (<b>track</b>) 😑<br/>You can read more about supported extensions <a href="/faq/">here</a>.')
                        return redirect('upload__track__page')

                    poster = request.FILES['track_poster']
                    file_extension = Path(str(poster)).suffix
                    if not file_extension in IMAGE_EXTENSIONS:
                        messages.error(request,
                                       'This file extension is not supported (<b>poster</b>) 😑<br/>You can read more about supported extensions <a href="/faq/">here</a>.')
                        return redirect('upload__track__page')
                    else:
                        if poster.size > MAX_IMAGE_SIZE:
                            messages.error(request, 'The size of the photo should not exceed 7.5 MB. 💡')
                            return redirect('upload__track__page')

                    title = request.POST['title']
                    if len(str(title)) > 150:
                        messages.error(request, 'Maximum title length 150 characters 🥴')
                        return redirect('upload__track__page')

                    # maximum 5 tracks per day (one user)
                    today = date.today()
                    if Track.objects.filter(creator=request.user, date_created_without_time=today).count() < 5:
                        # create track model
                        track = Track.objects.create(creator=request.user, track=track, track_id=generate_id(32),
                                                     track_poster=poster, title=title)
                        track.save()

                        messages.success(request, f'You have successfully posted a track: <b>{track.title}</b> 🤩')
                        return redirect('track__page', track.track_id)
                    else:
                        messages.success(request, 'You have exceeded the tracks limit for one day today 😥')
                        return redirect('main__page')
        except:
            return redirect('upload__track__page')


# sign up page
class SignUpView(TemplateView):
    template_name = 'user/auth/sign_up.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            return super(SignUpView, self).dispatch(*args, **kwargs)

    def post(self, request):
        try:
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            username = request.POST['username']
            if len(str(password1).replace(' ', '')) < 8 or len(str(password2).replace(' ', '')) < 8:
                messages.error(self.request,
                               'The password must be at least 8 characters long and consist of Latin letters, numbers and special characters ☹️')
                return redirect('sign__up__page')
            else:
                if str(password1) != str(password2):
                    messages.error(self.request, "Passwords don't match 😱")
                    return redirect('sign__up__page')
                else:
                    if len(str(username).replace(' ', '')) == 0:
                        messages.error(self.request, "Username cannot consist of spaces 😖")
                        return redirect('sign__up__page')
                    else:
                        form = CreateUserForm(request.POST)

                        if form.is_valid():
                            obj = form.save(commit=False)
                            obj.user_id = generate_id(24)
                            form.save()

                            # alert
                            messages.success(self.request, 'Account created successfully 😃')
                            return redirect('main__page')
                        else:
                            messages.error(self.request,
                                           "Your password is too simple or similar to your other personal information 😿")
                            return redirect('sign__up__page')
        except:
            pass


# sign in page
class SignInView(TemplateView):
    template_name = 'user/auth/sign_in.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            return super(SignInView, self).dispatch(*args, **kwargs)

    def post(self, request):
        try:
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)

                    # YandexHub Alert
                    if user.telegram:
                        # send alert
                        message = YandexHubAlert(f'Login to your account 🤨\n\n{get_city_and_country_ip(request)}\n\n',
                                                 user.telegram)
                        if message == 200:
                            pass
                        elif message == 400:
                            messages.error(self.request,
                                           '''An error occurred while sending the notification. Check the correctness of your Telegram ID by the <a style='cursor: pointer; color: #0D6EFD;' onclick='transition_link("/bot/")'>link</a> 🤖''')
                        else:
                            messages.error(self.request,
                                           '''An error occurred while sending a notification. You have blocked the bot from sending messages to fix this read the <a style='cursor: pointer; color: #0D6EFD;' onclick='transition_link("/bot/manual/")'>manual</a> 🤖''')
                    else:
                        messages.success(self.request,
                                         '''In order to secure your account, you can connect a <b>YandexHub Alert Bot</b> using the <a style='cursor: pointer; color: #0D6EFD;' onclick='transition_link("/bot/")'>link</a> 😃''')

                    messages.success(self.request, f'You are logged in as: <b>{user.username}</b> 🥳')
                    return redirect('main__page')
                else:
                    return redirect('signin')
            else:
                messages.error(self.request, 'Incorrect email or password 😧')
                return redirect('signin')
        except:
            pass


# sign out
class SignOutView(View):
    @method_decorator(login_required)
    def get(self, request):
        logout(request)

        # send alert
        messages.success(request, 'You have successfully logged out of your account 💀')
        return redirect('main__page')


# 404 error
def error_404_view(request, exception):
    return render(request, '404.html', status=status.HTTP_404_NOT_FOUND)


# 500 error
def error_500_view(request):
    return render(request, '500.html', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
