# USER
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# VIEWS
from django.views.generic import View, TemplateView, ListView

# HTTP 
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import Http404

# NETWORK
from urllib.request import urlopen

# JSON
import json 

# MESSAGES
from django.contrib import messages

# DRF
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

# RANDOM
import random
from random import choice

# DECORATORS
from .decorators import *

# MODELS
from .models import *
from django.db.models import Q

# FORMS
from .forms import *
from django.contrib.auth.forms import UserCreationForm

# DATE/TIME
from datetime import date, datetime, timedelta, timezone

# OTHER
from itertools import groupby

# TELEGRAM
import telebot

DOMEN = "http://127.0.0.1:8000/"

# Generate random string
def generate_id(num):
    symbols = 'aSfzeKGhxAsBPYMECJmUwQgdcuRbXFHDkLvniytjNqpVWrTZ123456789'
    key = ''.join(choice(symbols) for i in range(num))
    return key

# Get random list
def random_list(x):
    random.shuffle(x)
    return x

# Get recommendations on video page
def get_video_recommendations(channel, video):
    video_channel_recommendations = []
    for i in range(5):
        try:
            channel_video = Video.objects.filter(creator=channel).order_by('-date_created')[i]
            if channel_video == video:
                pass
            else:
                video_channel_recommendations.append(channel_video)
        except:
            pass
    
    video_recommendations = []
    for i in range(30):
        try:
            other_video = Video.objects.order_by('likes', 'comments', 'views', 'date_created')[i]
            if other_video == video:
                pass
            else:
                video_recommendations.append(other_video)
        except:
            pass
    
    return list(set(video_channel_recommendations + random_list(video_recommendations)))

# Add coefficient for video
def coefficient_func(video):
    video.coefficient = video.views / (video.dislikes + video.comments - video.likes + 10)
    video.save()

# view function
def view_func(video, request):
    if request.user.is_authenticated:
        VideoViewModel.objects.create(watched_user=request.user, watched_video=video)
        video.views += 1
        video.save()
        video.creator.all_views += 1
        video.creator.save()

    coefficient_func(video)

# get IP
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# get info about IP
def get_ip_info(ip):
    url = 'https://ipinfo.io/' + ip + '/json'
    res = urlopen(url)
    data = json.load(res)
    response = {}
    if 'country' in data:
        response['country'] = data['country']

    if 'city' in data:
        response['city'] = data['city']

    return response

# bot send message
def YandexHubAlert(text, telegram_id):
    try:
        bot = telebot.TeleBot('1785721677:AAF0OeaZ-ZC_Zf5IF0BMaDqacKE3y7OB290')
        bot.send_message(telegram_id, text)
        return 'ok'
    except:
        return 'err'


#  home page
class HomeView(ListView):
    template_name = 'home.html'
    paginate_by = 20
    model = Video
    context_object_name = "videos"
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['title'] = 'YandexHub'
        return context

# search video system
class SearchView(ListView):
    template_name = "video/search/search.html"
    paginate_by = 10
    queryset = Video
    context_object_name = "videos"

    def get_queryset(self):
        return Video.objects.filter(title__icontains=self.kwargs['pk']).order_by('-coefficient')

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['title'] = self.kwargs['pk']
        return context


# channel page
class ChannelView(ListView):
    template_name = "user/channel.html"
    paginate_by = 1
    queryset = Video
    context_object_name = "videos"

    def get_queryset(self):
        self.channel = CustomUser.objects.get(user_id=self.kwargs['pk'])
        return Video.objects.filter(creator=self.channel).order_by('-date_created')

    def get_context_data(self,**kwargs):
        context = super(ChannelView, self).get_context_data(**kwargs)
        self.videos = Video.objects.filter(creator=self.channel).order_by('-date_created')

        # find subscribe model
        self.subscribe = Subscribe.objects.filter(subscriber=self.request.user.id, channel=self.channel)

        # find notification model 
        self.notifications = Notification.objects.filter(notification_channel=self.channel, notification_user=self.request.user)

        context['notifications'] = self.notifications
        context['subscribe'] = self.subscribe
        context['title'] = self.channel.username
        context['videos'] = self.videos
        context['channel'] = self.channel
        return context     

# subscribe to user
class SubscribeApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        channel = CustomUser.objects.get(user_id=request.data.get("channel_id"))
        subscribe = Subscribe.objects.filter(subscriber=request.user, channel=channel)

        if subscribe.count() > 0:
            channel.all_subscribers -= 1
            channel.save()
            subscribe.delete()
            return Response({"data": {"subscribe": 0}, "message": "Subscription removed 🤡", "status": "ok"})

        elif subscribe.count() == 0:
            channel.all_subscribers += 1
            channel.save()
            Subscribe.objects.create(subscriber=request.user, channel=channel)
            return Response({"data": {"subscribe": 1}, "message": "Subscription added 🤗", "status": "ok"})

        else:
            return Response({"data": {}, "status": "err"})

# notifications
class NotificationsApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        channel = CustomUser.objects.get(user_id=request.data.get("user_id"))
        notification = Notification.objects.filter(notification_user=request.user, notification_channel=channel)

        if notification.count() > 0:
            notification.delete()
            return Response({"data": {"notification": 0}, "message": "Notifications turned off for this channel 😬", "status": "ok"})

        elif notification.count() == 0:
            Notification.objects.create(notification_channel=channel, notification_user=request.user)
            return Response({"data": {"notification": 1}, "message": "You’ll get all notifications 😃", "status": "ok"})

        else:
            return Response({"data": {}, "status": "err"})

# about channel page
class AboutView(TemplateView):
    template_name = "user/about.html"

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        self.channel = CustomUser.objects.get(user_id=self.kwargs['pk'])

        # find subscribe model 
        self.subscribe = Subscribe.objects.filter(subscriber=self.request.user.id, channel=self.channel)

        # find notification model 
        self.notifications = Notification.objects.filter(notification_channel=self.channel, notification_user=self.request.user)

        context['title'] = f'About - {self.channel.username}'
        context['notifications'] = self.notifications
        context['subscribe'] = self.subscribe
        context['channel'] = self.channel
        return context


# settings page
class SettingsView(TemplateView):
    template_name = 'user/settings/main.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super(SettingsView,self).get_context_data(**kwargs)
            context['title'] = 'Settings ⚙️'
            return context

# channel settings page
class ChannelSettingsView(TemplateView):
    template_name = 'user/settings/channel.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super(ChannelSettingsView,self).get_context_data(**kwargs)
            context['title'] = 'Channel settings 👻'
            context['CustomUserTextArea'] = CustomUserTextArea(instance=self.request.user)
            return context

    def post(self, request):
        user = request.user     
        try:
            user.avatar = request.FILES['avatar']
        except:
            pass
        
        try:
            user.banner = request.FILES['banner']
        except:
            pass

        user.username = request.POST['username'] 
        user.description = request.POST['description']
        user.location = request.POST['location']
        user.contact_email = request.POST['contact_email']
        user.vk_link = request.POST['vk_link']
        user.telegram_link = request.POST['telegram_link']
        user.instagram_link = request.POST['instagram_link']
        user.facebook_link = request.POST['facebook_link']
        user.twitter_link = request.POST['twitter_link']
        user.reddit_link = request.POST['reddit_link']
        user.website_link = request.POST['website_link']

        user.save()

        messages.success(request, "Settings have been saved 👽")
        return redirect('channel__settings__page')
        
# account settings page
class AccountSettingsView(TemplateView):
    template_name = 'user/settings/account.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super(AccountSettingsView,self).get_context_data(**kwargs)
            context['title'] = 'Account settings 🤡'
            return context

    def post(self, request):   
        password = request.POST['password']
        email = request.user.email
        user_id = request.user.user_id
        telegram = request.user.telegram
        user = authenticate(email=email, password=password)

        if user is not None:
            logout(request)
            CustomUser.objects.get(email=email, user_id=user_id).delete()

            # YandexHub Alert
            if telegram:
                # send alert
                ip = get_client_ip(request)
                now = datetime.now() 
                date = now.strftime("%d-%m-%Y %H:%M:%S")
                ip_info = get_ip_info(ip)
                if 'country' in ip_info:
                    country = ip_info['country']
                else:
                    country = '???'

                if 'city' in ip_info:
                    city = ip_info['city']
                else:
                    city = '???'

                message = YandexHubAlert(f"Your YandexHub account has been successfully deleted 💀\n\nDate: {date}\nIP: {ip}\nCountry: {country}\nCity: {city}", telegram)
                if message == 'ok':
                    pass 
                else:
                    pass            
            else:
                pass

            messages.success(request, "Account successfully deleted 😭")
            return redirect('main__page')
        else:
            messages.success(request, "Wrong password entered 😖")
            return redirect('account__settings__page')

# change password page
class ChangePasswordView(TemplateView):
    template_name = 'user/settings/password.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super(ChangePasswordView,self).get_context_data(**kwargs)
            context['title'] = 'Change password 🔒'
            return context

    def post(self, request):   
        password = request.POST['password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']

        if new_password == confirm_new_password:
            if len(new_password) < 8 or len(str(new_password).replace(' ', '')) < 8:
                messages.success(request, "Password cannot contain only spaces or be less than 8 characters 🧸")
                return redirect('change__password__page')
            else:
                email = request.user.email
                user_id = request.user.user_id
                telegram = request.user.telegram
                user = authenticate(email=email, password=password)

                if user is not None:
                    user.set_password(new_password)
                    user.save()
                    
                    logout(request)

                    # YandexHub Alert
                    if telegram:
                        # send alert
                        ip = get_client_ip(request)
                        now = datetime.now() 
                        date = now.strftime("%d-%m-%Y %H:%M:%S")
                        ip_info = get_ip_info(ip)
                        if 'country' in ip_info:
                            country = ip_info['country']
                        else:
                            country = '???'

                        if 'city' in ip_info:
                            city = ip_info['city']
                        else:
                            city = '???'
                        
                        message = YandexHubAlert(f"Your password has been successfully changed 👻\n\nDate: {date}\nIP: {ip}\nCountry: {country}\nCity: {city}", telegram)
                        if message == 'ok':
                            pass 
                        else:
                            pass            
                    else:
                        pass

                    messages.success(request, "Your password has been successfully changed 👻")
                    messages.success(request, """After changing your password, you must re-enter your account using the <a style='cursor: pointer; color: #0D6EFD;' onclick='transition_link("/sign/in/")'>link</a> 📱""")
                    return redirect('main__page')
                else:
                    messages.success(request, "Wrong password entered 😖")
                    return redirect('change__password__page')
        else:
            messages.success(request, "Password mismatch 😿")
            return redirect('change__password__page')

# change email page
class ChangeEmailView(TemplateView):
    template_name = 'user/settings/email.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super(ChangeEmailView,self).get_context_data(**kwargs)
            context['title'] = 'Change email ✉️'
            return context

    def post(self, request):   
        password = request.POST['password']
        new_email = request.POST['new_email']

        email = request.user.email
        telegram = request.user.telegram
        user = authenticate(email=email, password=password)

        if user is not None:
            user.email = new_email
            user.save()
            
            logout(request)

            # YandexHub Alert
            if telegram:
                # send alert
                ip = get_client_ip(request)
                now = datetime.now() 
                date = now.strftime("%d-%m-%Y %H:%M:%S")
                ip_info = get_ip_info(ip)
                if 'country' in ip_info:
                    country = ip_info['country']
                else:
                    country = '???'

                if 'city' in ip_info:
                    city = ip_info['city']
                else:
                    city = '???'
                
                message = YandexHubAlert(f"Your email has been successfully changed 🙃\n\nDate: {date}\nIP: {ip}\nCountry: {country}\nCity: {city}", telegram)
                if message == 'ok':
                    pass 
                else:
                    pass            
            else:
                pass

            messages.success(request, "Your email has been successfully changed 🙃")
            messages.success(request, """After changing your email, you must re-enter your account using the <a style='cursor: pointer; color: #0D6EFD;' onclick='transition_link("/sign/in/")'>link</a> 📱""")
            return redirect('main__page')
  
        else:
            messages.success(request, "Wrong password entered 😖")
            return redirect('change__email__page')


# delete video
class DeleteVideoApi(APIView):
    def post(self, request):
        video_id = request.data.get("video_id")
        video = Video.objects.filter(video_id=video_id)
        if video.count() > 0:
            if video[0].creator == request.user:
                title = video[0].title
                video[0].delete()
                messages.success(request, f"<b>{title}</b>, successfully deleted! 🎃")
                return Response({"data": {}, "status": "ok"})
            else:
                return Response({"data": {}, "message": "You are not authorized to delete this video because you are not its creator", "status": "err"})
        else:
            return Response({"data": {}, "message": "Video not found", "status": "err"})

# save video
class SaveVideoApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        video = Video.objects.get(video_id=request.data.get("video_id"))
        save = SavedVideo.objects.filter(saved_video=video, saved_user=request.user)

        if save.count() > 0:
            save.delete()
            return Response({"data": {"save": 0}, "message": "Removed from Saved videos ✂️", "status": "ok"})

        elif save.count() == 0:
            SavedVideo.objects.create(saved_video=video, saved_user=request.user)
            return Response({"data": {"save": 1}, "message": "Added to Saved videos 📌", "status": "ok"})

        else:
            return Response({"data": {}, "status": "err"})

# like video
class LikeVideoApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        video = Video.objects.get(video_id=request.data.get("video_id"))
        like = Like.objects.filter(liked_video=video, liked_user=request.user)
        dislike = Dislike.objects.filter(disliked_video=video, disliked_user=request.user)

        if like.count() == 0 and dislike.count() == 0:
            like = Like.objects.create(liked_video=video, liked_user=request.user)
            if like:
                video.likes += 1
                video.save()
            return Response({"data": {"like": 1, "dislike": 0, "stats": {"likes": video.likes, "dislikes": video.dislikes}}, "message": "Added to Liked videos 👍", "status": "ok"})

        elif like.count() == 1 and dislike.count() == 0:
            like[0].delete()
            video.likes -= 1
            video.save()
            return Response({"data": {"like": 0, "dislike": 0, "stats": {"likes": video.likes, "dislikes": video.dislikes}}, "message": "Removed from Liked videos 👀", "status": "ok"})

        elif like.count() == 0 and dislike.count() == 1:
            video.dislikes -= 1
            video.likes += 1
            video.save()
            dislike[0].delete()
            like = Like.objects.create(liked_video=video, liked_user=request.user)
            return Response({"data": {"like": 1, "dislike": 0, "stats": {"likes": video.likes, "dislikes": video.dislikes}}, "message": "Added to Liked videos 👍", "status": "ok"})

        else:
            return Response({"data": {}, "status": "err"})

# dislike video
class DislikeVideoApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        video = Video.objects.get(video_id=request.data.get("video_id"))
        like = Like.objects.filter(liked_video=video, liked_user=request.user)
        dislike = Dislike.objects.filter(disliked_video=video, disliked_user=request.user)

        if like.count() == 0 and dislike.count() == 0:
            dislike = Dislike.objects.create(disliked_video=video, disliked_user=request.user)
            if dislike:
                video.dislikes += 1
                video.save()
            return Response({"data": {"like": 0, "dislike": 1, "stats": {"likes": video.likes, "dislikes": video.dislikes}}, "message": "You dislike this video 👎", "status": "ok"})

        elif dislike.count() == 1 and like.count() == 0:
            dislike[0].delete()
            video.dislikes -= 1
            video.save()
            return Response({"data": {"like": 0, "dislike": 0, "stats": {"likes": video.likes, "dislikes": video.dislikes}}, "message": "Dislike removed 😎", "status": "ok"})

        elif dislike.count() == 0 and like.count() == 1:
            video.likes -= 1
            video.dislikes += 1
            video.save()
            like[0].delete()
            dislike = Dislike.objects.create(disliked_video=video, disliked_user=request.user)
            return Response({"data": {"like": 0, "dislike": 1, "stats": {"likes": video.likes, "dislikes": video.dislikes}}, "message": "You dislike this video 👎", "status": "ok"})

        else:
            return Response({"data": {}, "status": "err"})

# video page
class VideoView(ListView):
    template_name = "video/video.html"
    paginate_by = 10
    queryset = Comment
    context_object_name = "comments"

    def get_queryset(self, **kwargs):
        video = Video.objects.get(video_id=self.kwargs['pk'])
        return Comment.objects.filter(commented_video=video).order_by('-likes')

    def get_context_data(self, **kwargs):
        context = super(VideoView, self).get_context_data(**kwargs)
        video = Video.objects.get(video_id=self.kwargs['pk'])

        view_func(video, self.request) # view video
        
        context['title'] = f'{video.title}'
        context['video'] = video
        context['video_recommendations'] = get_video_recommendations(video.creator, video)
        if self.request.user.is_authenticated:
            context['subscribe'] = Subscribe.objects.filter(subscriber=self.request.user, channel=video.creator)
            context['saved_video'] = SavedVideo.objects.filter(saved_user=self.request.user, saved_video=video)
            context['liked'] = Like.objects.filter(liked_user=self.request.user, liked_video=video)
            context['disliked'] = Dislike.objects.filter(disliked_user=self.request.user, disliked_video=video)
        return context

# create video page
class CreateVideoView(TemplateView):
    template_name = 'video/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateVideoView, self).get_context_data(**kwargs)
        context['title'] = 'Upload video 📲'
        context['VideoTextArea'] = VideoTextArea()
        return context
    
    def post(self, request):
        if request.POST['title'] is None or len(request.POST['title'].replace(' ', '')) == 0:
            messages.success(request, "Video title cannot contain spaces 😈")
            return redirect('create__video__page')
        else:
            if 'video' not in request.FILES or 'video_banner' not in request.FILES:
                messages.success(request, "You must upload <b>video</b> and <b>banner</b> 😖")
                return redirect('create__video__page')
            else:
                # create video model
                video = Video.objects.create(creator=request.user, video_id=generate_id(32), video=request.FILES['video'], video_banner=request.FILES['video_banner'], title=request.POST['title'], description=request.POST['description'])
                video.save()
                
                # send notification
                subscribers = Subscribe.objects.filter(channel=video.creator)
                for i in subscribers:
                    if i.subscriber.telegram:
                        YandexHubAlert(f'A new video has been released on the {video.creator.username} channel 🥳\n{DOMEN}video/{video.video_id}/', i.subscriber.telegram)

                messages.success(request, f"You have successfully posted a video: <b>{video.title}</b> 🤩")
                return redirect('video__page', video.video_id)

# change video page
class ChangeVideoView(TemplateView):
    template_name = "video/change.html"

    def get_context_data(self, **kwargs):
        context = super(ChangeVideoView, self).get_context_data(**kwargs)
        video = Video.objects.get(video_id=self.kwargs['pk'])
        context['video'] = video
        context['title'] = f'Change - {video.title}'
        context['VideoTextArea'] = VideoTextArea(instance=video)
        return context

    def post(self, request, **kwargs):
        video = Video.objects.get(video_id=self.kwargs['pk'])

        if video.creator == self.request.user:
            try:
                video.video_banner = request.FILES['video_banner']
            except:
                pass
        
            video.title = request.POST['title'] 
            video.description = request.POST['description'] 
            video.save()    

            # alert
            messages.success(request, f"You have successfully changed the video: <b>{video.title}</b> 😍")
            return redirect('video__page', video.video_id)

        else:
            # alert
            messages.success(request, f"You are not the author of the video: <b>{video.title}</b> 😡")
            return redirect('main__page')


# add comment
class AddCommentApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        video = Video.objects.get(video_id=request.data.get("video_id"))
        text = request.data.get("text")

        if text.replace(" ", "") != '' and text is not None:
            Comment.objects.create(comment_id=generate_id(32), commented_video=video, creator=request.user, comment_text=text)
            video.comments += 1
            video.save()
            return Response({"data": {}, "message": "Comment added 🌚", "status": "ok"})
        else:
            return Response({"data": {}, "message": "Comment cannot contain spaces or be empty 🙉", "status": "err"})            

# like comment
class LikeCommentApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        comment = Comment.objects.get(comment_id=request.data.get("comment_id"))
        like = CommentLike.objects.filter(liked_comment=comment, liked_user=request.user)
        dislike = CommentDislike.objects.filter(disliked_comment=comment, disliked_user=request.user)

        if like.count() == 0 and dislike.count() == 0:
            like = CommentLike.objects.create(liked_comment=comment, liked_user=request.user)
            if like:
                comment.likes += 1
                comment.save()
            return Response({"data": {"like": 1, "dislike": 0, "stats": {"likes": comment.likes, "dislikes": comment.dislikes}}, "message": "", "status": "ok"})

        elif like.count() == 1 and dislike.count() == 0:
            like[0].delete()
            comment.likes -= 1
            comment.save()
            return Response({"data": {"like": 0, "dislike": 0, "stats": {"likes": comment.likes, "dislikes": comment.dislikes}}, "message": "", "status": "ok"})

        elif like.count() == 0 and dislike.count() == 1:
            comment.dislikes -= 1
            comment.likes += 1
            comment.save()
            dislike[0].delete()
            like = CommentLike.objects.create(liked_comment=comment, liked_user=request.user)
            return Response({"data": {"like": 1, "dislike": 0, "stats": {"likes": comment.likes, "dislikes": comment.dislikes}}, "message": "", "status": "ok"})

        else:
            return Response({"data": {}, "status": "err"})

# dislike comment
class DislikeCommentApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        comment = Comment.objects.get(comment_id=request.data.get("comment_id"))
        like = CommentLike.objects.filter(liked_comment=comment, liked_user=request.user)
        dislike = CommentDislike.objects.filter(disliked_comment=comment, disliked_user=request.user)

        if like.count() == 0 and dislike.count() == 0:
            dislike = CommentDislike.objects.create(disliked_comment=comment, disliked_user=request.user)
            if dislike:
                comment.dislikes += 1
                comment.save()
            return Response({"data": {"like": 0, "dislike": 1, "stats": {"likes": comment.likes, "dislikes": comment.dislikes}}, "message": "", "status": "ok"})

        elif dislike.count() == 1 and like.count() == 0:
            dislike[0].delete()
            comment.dislikes -= 1
            comment.save()
            return Response({"data": {"like": 0, "dislike": 0, "stats": {"likes": comment.likes, "dislikes": comment.dislikes}}, "message": "", "status": "ok"})

        elif dislike.count() == 0 and like.count() == 1:
            comment.likes -= 1
            comment.dislikes += 1
            comment.save()
            like[0].delete()
            dislike = CommentDislike.objects.create(disliked_comment=comment, disliked_user=request.user)
            return Response({"data": {"like": 0, "dislike": 1, "stats": {"likes": comment.likes, "dislikes": comment.dislikes}}, "message": "", "status": "ok"})

        else:
            return Response({"data": {}, "status": "err"})

# delete comment
class DeleteCommentApi(APIView):
    def post(self, request):
        comment_id = request.data.get("comment_id")
        comment = Comment.objects.filter(comment_id=comment_id)
        if comment.count() > 0:
            if comment[0].creator == request.user:
                video = comment[0].commented_video 
                video.comments -= (1 + comment[0].replies)
                video.save()
                comment[0].delete()
                return Response({"data": {}, "message": "Comment has been deleted 🧸", "status": "ok"})
            else:
                return Response({"data": {}, "message": "You are not authorized to delete this comment because you are not its creator", "status": "err"})
        else:
            return Response({"data": {}, "message": "Comment not found", "status": "err"})

# add reply comment
class AddReplyCommentApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        video = Video.objects.get(video_id=request.data.get("video_id"))
        comment = Comment.objects.get(comment_id=request.data.get("comment_id"))
        text = request.data.get("text")

        if text.replace(" ", "") != '' and text is not None:
            ReplyComment.objects.create(reply_comment_id=generate_id(32), reply_commented_video=video, comment_parent=comment, creator=request.user, comment_text=text)
            comment.replies += 1
            comment.save()
            video.comments += 1
            video.save()    
            return Response({"data": {}, "message": "Reply to comment added ⛄️", "status": "ok"})
        else:
            return Response({"data": {}, "message": "Comment cannot contain spaces or be empty 🙉", "status": "err"})            

# like reply comment
class LikeReplyCommentApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        comment = ReplyComment.objects.get(reply_comment_id=request.data.get("reply_comment_id"))
        like = ReplyCommentLike.objects.filter(liked_reply_comment=comment, liked_user=request.user)
        dislike = ReplyCommentDislike.objects.filter(disliked_reply_comment=comment, disliked_user=request.user)

        if like.count() == 0 and dislike.count() == 0:
            like = ReplyCommentLike.objects.create(liked_reply_comment=comment, liked_user=request.user)
            if like:
                comment.likes += 1
                comment.save()
            return Response({"data": {"like": 1, "dislike": 0, "stats": {"likes": comment.likes, "dislikes": comment.dislikes}}, "message": "", "status": "ok"})

        elif like.count() == 1 and dislike.count() == 0:
            like[0].delete()
            comment.likes -= 1
            comment.save()
            return Response({"data": {"like": 0, "dislike": 0, "stats": {"likes": comment.likes, "dislikes": comment.dislikes}}, "message": "", "status": "ok"})

        elif like.count() == 0 and dislike.count() == 1:
            comment.dislikes -= 1
            comment.likes += 1
            comment.save()
            dislike[0].delete()
            like = ReplyCommentLike.objects.create(liked_reply_comment=comment, liked_user=request.user)
            return Response({"data": {"like": 1, "dislike": 0, "stats": {"likes": comment.likes, "dislikes": comment.dislikes}}, "message": "", "status": "ok"})

        else:
            return Response({"data": {}, "status": "err"})

# dislike comment
class DislikeReplyCommentApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        comment = ReplyComment.objects.get(reply_comment_id=request.data.get("reply_comment_id"))
        like = ReplyCommentLike.objects.filter(liked_reply_comment=comment, liked_user=request.user)
        dislike = ReplyCommentDislike.objects.filter(disliked_reply_comment=comment, disliked_user=request.user)

        if like.count() == 0 and dislike.count() == 0:
            dislike = ReplyCommentDislike.objects.create(disliked_reply_comment=comment, disliked_user=request.user)
            if dislike:
                comment.dislikes += 1
                comment.save()
            return Response({"data": {"like": 0, "dislike": 1, "stats": {"likes": comment.likes, "dislikes": comment.dislikes}}, "message": "", "status": "ok"})

        elif dislike.count() == 1 and like.count() == 0:
            dislike[0].delete()
            comment.dislikes -= 1
            comment.save()
            return Response({"data": {"like": 0, "dislike": 0, "stats": {"likes": comment.likes, "dislikes": comment.dislikes}}, "message": "", "status": "ok"})

        elif dislike.count() == 0 and like.count() == 1:
            comment.likes -= 1
            comment.dislikes += 1
            comment.save()
            like[0].delete()
            dislike = ReplyCommentDislike.objects.create(disliked_reply_comment=comment, disliked_user=request.user)
            return Response({"data": {"like": 0, "dislike": 1, "stats": {"likes": comment.likes, "dislikes": comment.dislikes}}, "message": "", "status": "ok"})

        else:
            return Response({"data": {}, "status": "err"})

# delete comment
class DeleteReplyCommentApi(APIView):
    def post(self, request):
        reply_comment_id = request.data.get("reply_comment_id")
        comment = ReplyComment.objects.filter(reply_comment_id=reply_comment_id)
        if comment.count() > 0:
            if comment[0].creator == request.user:
                video = comment[0].reply_commented_video 
                comment_parent = comment[0].comment_parent
                comment_parent.replies -= 1
                comment_parent.save()
                video.comments -= 1 
                video.save()
                comment[0].delete()
                return Response({"data": {}, "message": "Comment has been deleted 🧸", "status": "ok"})
            else:
                return Response({"data": {}, "message": "You are not authorized to delete this comment because you are not its creator", "status": "err"})
        else:
            return Response({"data": {}, "message": "Comment not found", "status": "err"})


# alert bot page
class AlertBotView(TemplateView):
    template_name = 'user/bot/main.html'

    def get_context_data(self, **kwargs):
        context = super(AlertBotView,self).get_context_data(**kwargs)
        context['title'] = 'YandexHub Alert Bot 🤖'
        return context

    def post(self, request):
        request.user.telegram = request.POST['telegram']
        request.user.save()

        messages.success(request, "Your Telegram ID has been successfully saved 🤖")
        return redirect('bot__page')

# alert bot manual page
class AlertBotManualView(TemplateView):
    template_name = 'user/bot/manual.html'

    def get_context_data(self, **kwargs):
        context = super(AlertBotManualView,self).get_context_data(**kwargs)
        context['title'] = 'YandexHub Alert Bot - Manual 📋'
        return context


# delete article
class DeleteArticleApi(APIView):
    def post(self, request):
        article_id = request.data.get("article_id")
        article = Article.objects.filter(article_id=article_id)
        if article.count() > 0:
            if article[0].creator == request.user:
                article[0].delete()
                messages.success(request, f"Article successfully deleted! 🩸")
                return Response({"data": {"user_id": request.user.user_id}, "status": "ok"})
            else:
                return Response({"data": {}, "message": "You are not authorized to delete this article because you are not its creator", "status": "err"})
        else:
            return Response({"data": {}, "message": "Article not found", "status": "err"})

# delete article
class DeleteArticleApi(APIView):
    def post(self, request):
        article_id = request.data.get("article_id")
        article = Article.objects.filter(article_id=article_id)
        if article.count() > 0:
            if article[0].creator == request.user:
                article[0].delete()
                messages.success(request, f"Article successfully deleted! 🩸")
                return Response({"data": {"user_id": request.user.user_id}, "status": "ok"})
            else:
                return Response({"data": {}, "message": "You are not authorized to delete this article because you are not its creator", "status": "err"})
        else:
            return Response({"data": {}, "message": "Article not found", "status": "err"})

# like article
class LikeArticleApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        article = Article.objects.get(article_id=request.data.get("article_id"))
        like = ArticleLike.objects.filter(liked_article=article, liked_user=request.user)
        dislike = ArticleDislike.objects.filter(disliked_article=article, disliked_user=request.user)

        if like.count() == 0 and dislike.count() == 0:
            like = ArticleLike.objects.create(liked_article=article, liked_user=request.user)
            if like:
                article.likes += 1
                article.save()
            return Response({"data": {"like": 1, "dislike": 0, "stats": {"likes": article.likes, "dislikes": article.dislikes}}, "message": "You like this article 👍", "status": "ok"})

        elif like.count() == 1 and dislike.count() == 0:
            like[0].delete()
            article.likes -= 1
            article.save()
            return Response({"data": {"like": 0, "dislike": 0, "stats": {"likes": article.likes, "dislikes": article.dislikes}}, "message": "Like removed 👀", "status": "ok"})

        elif like.count() == 0 and dislike.count() == 1:
            article.dislikes -= 1
            article.likes += 1
            article.save()
            dislike[0].delete()
            like = ArticleLike.objects.create(liked_article=article, liked_user=request.user)
            return Response({"data": {"like": 1, "dislike": 0, "stats": {"likes": article.likes, "dislikes": article.dislikes}}, "message": "You like this article 👍", "status": "ok"})

        else:
            return Response({"data": {}, "status": "err"})

# dislike article
class DislikeArticleApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        article = Article.objects.get(article_id=request.data.get("article_id"))
        like = ArticleLike.objects.filter(liked_article=article, liked_user=request.user)
        dislike = ArticleDislike.objects.filter(disliked_article=article, disliked_user=request.user)

        if like.count() == 0 and dislike.count() == 0:
            dislike = ArticleDislike.objects.create(disliked_article=article, disliked_user=request.user)
            if dislike:
                article.dislikes += 1
                article.save()
            return Response({"data": {"like": 0, "dislike": 1, "stats": {"likes": article.likes, "dislikes": article.dislikes}}, "message": "You dislike this article 👎", "status": "ok"})

        elif dislike.count() == 1 and like.count() == 0:
            dislike[0].delete()
            article.dislikes -= 1
            article.save()
            return Response({"data": {"like": 0, "dislike": 0, "stats": {"likes": article.likes, "dislikes": article.dislikes}}, "message": "Dislike removed 😎", "status": "ok"})

        elif dislike.count() == 0 and like.count() == 1:
            article.likes -= 1
            article.dislikes += 1
            article.save()
            like[0].delete()
            dislike = ArticleDislike.objects.create(disliked_article=article, disliked_user=request.user)
            return Response({"data": {"like": 0, "dislike": 1, "stats": {"likes": article.likes, "dislikes": article.dislikes}}, "message": "You dislike this article 👎", "status": "ok"})

        else:
            return Response({"data": {}, "status": "err"})


# community page
class CommunityView(ListView):
    template_name = "user/community/community.html"
    paginate_by = 10
    model = Article
    context_object_name = "articles"

    def get_queryset(self, **kwargs):
        channel = CustomUser.objects.get(user_id=self.kwargs['pk'])
        return Article.objects.filter(creator=channel).order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super(CommunityView, self).get_context_data(**kwargs)
        self.channel = CustomUser.objects.get(user_id=self.kwargs['pk'])

        # find subscribe model 
        self.subscribe = Subscribe.objects.filter(subscriber=self.request.user.id, channel=self.channel)

        # find notification model 
        self.notifications = Notification.objects.filter(notification_channel=self.channel, notification_user=self.request.user)

        context['title'] = f'Community - {self.channel.username}'
        context['notifications'] = self.notifications
        context['subscribe'] = self.subscribe
        context['channel'] = self.channel
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
        if request.POST['text'] is None or len(request.POST['text'].replace(' ', '')) == 0:
            messages.success(request, "Article text cannot contain spaces 😈")
            return redirect('create__article__page')
        else:
            # create article model
            article = Article.objects.create(creator=request.user, article_id=generate_id(32), text=request.POST['text'])
            article.save()
            
            messages.success(request, f"You have successfully posted a article 🤪")
            return redirect('community__page', request.user.user_id)

# change article page 
class ChangeArticleView(TemplateView):
    template_name = "user/community/change.html"

    def get_context_data(self, **kwargs):
        context = super(ChangeArticleView, self).get_context_data(**kwargs)
        article = Article.objects.get(article_id=self.kwargs['pk'])
        context['article'] = article
        context['title'] = 'Change article 🛠'
        context['ArticleTextArea'] = ArticleTextArea(instance=article)
        return context

    def post(self, request, **kwargs):
        article = Article.objects.get(article_id=self.kwargs['pk'])

        if article.creator == self.request.user:
            article.text = request.POST['text'] 
            article.save()    

            # alert
            messages.success(request, f"You have successfully changed the article 😍")
            return redirect('community__page', article.creator.user_id)

        else:
            # alert
            messages.success(request, f"You are not the author of the article 😡")
            return redirect('main__page')


# saved videos page
class SavedVideosView(ListView):
    template_name = 'user/video/saved.html'
    paginate_by = 10
    queryset = SavedVideo
    context_object_name = "videos"
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return SavedVideo.objects.filter(saved_user=self.request.user).order_by("-date_created")
        else:
            return SavedVideo.objects.none()

    def get_context_data(self,**kwargs):
        context = super(SavedVideosView, self).get_context_data(**kwargs)
        context['title'] = 'Saved videos 💾'
        return context

# liked videos page
class LikedVideosView(ListView):
    template_name = 'user/video/liked.html'
    paginate_by = 10
    queryset = Like
    context_object_name = "videos"
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Like.objects.filter(liked_user=self.request.user).order_by("-date_created")
        else:
            return Like.objects.none()

    def get_context_data(self,**kwargs):
        context = super(LikedVideosView, self).get_context_data(**kwargs)
        context['title'] = 'Liked videos 👍'
        return context

# history page
class HistoryView(ListView):
    template_name = 'user/video/history.html'
    paginate_by = 10
    queryset = VideoViewModel
    context_object_name = "videos"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return VideoViewModel.objects.filter(watched_user=self.request.user).order_by("-date_created")
        else:
            return VideoViewModel.objects.none()

    def get_context_data(self, **kwargs):
        context = super(HistoryView, self).get_context_data(**kwargs)
        context['title'] = 'Watch history 🕓'
        return context

# trending page
class TrendingView(ListView):
    template_name = 'video/other/trending.html'
    paginate_by = 10
    queryset = Video
    context_object_name = "videos"

    def get_queryset(self):
        tranding_time = datetime.utcnow() - timedelta(days=2)
        videos = []
        for i in range(100):
            try:
                video = Video.objects.filter(~Q(coefficient=0.0), date_created__gt=tranding_time).order_by('-coefficient')[i]
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
                for j in Video.objects.filter(creator=i.channel).order_by("-date_created"):
                    videos.append(j)

                n += 1
                if n > 100:
                    break
        else:
            videos = []

        context['title'] = 'Subscriptions 🎞'
        context['videos'] = videos
        return context


# get video stats
class VideoStatsApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        video = Video.objects.get(video_id=request.data.get("video_id"))

        views_stats = {}
        comments_stats = {}
        likes_stats = {}
        dislikes_stats = {}

        now = date.today()
        for i in range(10):
            enddate = now - timedelta(days=i)
            views = VideoViewModel.objects.filter(watched_video=video, date_created__range=(enddate, now))
            comments = Comment.objects.filter(commented_video=video, date_created__range=(enddate, now))
            reply_comments = ReplyComment.objects.filter(reply_commented_video=video, date_created__range=(enddate, now))
            likes = Like.objects.filter(liked_video=video, date_created__range=(enddate, now))
            dislikes = Dislike.objects.filter(disliked_video=video, date_created__range=(enddate, now))

            views_stats[str(now)] = len(views)
            comments_stats[str(now)] = len(comments) + len(reply_comments)
            likes_stats[str(now)] = len(likes)
            dislikes_stats[str(now)] = len(dislikes)
            
            now -= timedelta(days=1)

        return Response({"data": {"views": views_stats, "comments": comments_stats, "likes": likes_stats, "dislikes": dislikes_stats}, "message": "", "status": "ok"})     

# user videos page 
class UserVideosView(ListView):
    template_name = 'user/studio/videos.html'
    paginate_by = 10
    queryset = Video
    context_object_name = "videos"

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
    template_name = 'user/studio/comments.html'
    paginate_by = 25
    queryset = Comment
    context_object_name = "comments"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Comment.objects.filter(commented_video=Video.objects.get(video_id=self.kwargs['pk'])).order_by('-date_created')
        else:
            return Comment.objects.none()

    def get_context_data(self, **kwargs):
        context = super(VideoCommentsView, self).get_context_data(**kwargs)
        video = Video.objects.get(video_id=self.kwargs['pk'])
        context['title'] = 'Video comments 📝'
        context['video'] = video
        return context

# comment page 
class CommentView(ListView):
    template_name = 'user/studio/comment.html'
    paginate_by = 25
    queryset = ReplyComment
    context_object_name = "comments"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return ReplyComment.objects.filter(comment_parent=Comment.objects.get(comment_id=self.kwargs['pk'])).order_by('-date_created')
        else:
            return ReplyComment.objects.none()

    def get_context_data(self, **kwargs):
        context = super(CommentView, self).get_context_data(**kwargs)
        comment = Comment.objects.get(comment_id=self.kwargs['pk'])
        context['title'] = 'Video comments 📝'
        context['comment'] = comment
        return context

# video stats page
class VideoStatsView(TemplateView):
    template_name = 'user/studio/video.html'

    def get_context_data(self, **kwargs):
        context = super(VideoStatsView, self).get_context_data(**kwargs)
        video = Video.objects.get(video_id=self.kwargs['pk'])

        context['title'] = f'{video.title}'
        context['video'] = video
        return context


# films page
class FilmsView(ListView):
    template_name = 'film/films.html'
    paginate_by = 20
    model = Film
    context_object_name = "films"
    
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
    template_name = "film/film.html"
    #paginate_by = 10
    #queryset = Comment
    #context_object_name = "comments"

    #def get_queryset(self, **kwargs):
    #    return Comment.objects.all()

    def get_context_data(self, **kwargs):
        context = super(FilmView, self).get_context_data(**kwargs)
        film = Film.objects.get(film_id=self.kwargs['pk'])
        buy = BuyFilm.objects.filter(buy_film=film, buy_user=self.request.user)

        context['title'] = f'{film.title}'
        context['buy'] = buy
        context['film'] = film

        if self.request.user.is_authenticated:
            #context['liked'] = Like.objects.filter(liked_user=self.request.user, liked_video=video)
            #context['disliked'] = Dislike.objects.filter(disliked_user=self.request.user, disliked_video=video)
            pass

        return context

# buy film
class BuyFilmApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        film = Film.objects.get(film_id=request.data.get("film_id"))
        BuyFilm.objects.create(buy_user=request.user, buy_film=film)

        if request.user.telegram:
            now = datetime.now() 
            date = now.strftime("%d-%m-%Y %H:%M:%S")
            YandexHubAlert(f"You purchased the movie: {film.title} 🥳\nDate: {date}\nPrice: USD {film.price}\n\n{DOMEN}film/{film.film_id}/", request.user.telegram)


        messages.success(self.request, f"You purchased the movie: <b>{film.title}</b> 🥳")
        return Response({"data": {}, "status": "ok"})

   


# sign up page
class SignUpView(TemplateView):
    template_name = "user/auth/sign_up.html"

    def post(self, request):
        form = CreateUserForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user_id = generate_id(24)
            form.save()
            
            # alert
            messages.success(self.request, "Account created successfully 😃")
            return redirect('main__page')
        else:
            return redirect('sign__up__page')

# sign in page
class SignInView(TemplateView):
    template_name = "user/auth/sign_in.html"

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                # YandexHub Alert
                if user.telegram:
                    # send alert
                    ip = get_client_ip(request)
                    now = datetime.now() 
                    date = now.strftime("%d-%m-%Y %H:%M:%S")
                    ip_info = get_ip_info(ip)
                    if 'country' in ip_info:
                        country = ip_info['country']
                    else:
                        country = '???'

                    if 'city' in ip_info:
                        city = ip_info['city']
                    else:
                        city = '???'

                    message = YandexHubAlert(f"Login to your account 🤨\n\nDate: {date}\nIP: {ip}\nCountry: {country}\nCity: {city}", user.telegram)
                    if message == 'ok':
                        pass 
                    else:
                        messages.success(self.request, """An error occurred while sending the notification. Check the correctness of your Telegram ID by the <a style='cursor: pointer; color: #0D6EFD;' onclick='transition_link("/bot/")'>link</a> 🤖""")
                else:
                    messages.success(self.request, """In order to secure your account, you can connect a <b>YandexHub Alert Bot</b> using the <a style='cursor: pointer; color: #0D6EFD;' onclick='transition_link("/bot/")'>link</a> 😃""")

                messages.success(self.request, f"You are logged in as: <b>{user.username}</b> 🥳")
                return redirect('main__page')
            else:
                return redirect('sign__in__page')
        else:
            return redirect('sign__in__page')

# sign out
class SignOutView(View):
    def get(self, request):
        logout(request)

        # send alert
        messages.success(request, "You have successfully logged out of your account 💀")
        return redirect('main__page')



# 404 error
def error_404_view(request, exception):
    return render(request, '404.html')

# 500 error
def error_500_view(request):
    return render(request, '404.html')