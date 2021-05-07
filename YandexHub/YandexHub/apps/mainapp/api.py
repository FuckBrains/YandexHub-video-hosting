# DRF
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

# MODELS
from .models import *

# DATE/TIME
from datetime import date, datetime, timedelta, timezone

# MESSAGES
from django.contrib import messages

# views funcs
from .views import YandexHubAlert, get_city_and_country_ip, get_client_ip, get_ip_info, DOMEN

# HELPERS
from .helpers import generate_id

# subscribe to user
class SubscribeApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        channel = CustomUser.objects.get(user_id=request.data.get('channel_id'))
        subscribe = Subscribe.objects.filter(subscriber=request.user, channel=channel)

        if subscribe.count() > 0:
            channel.all_subscribers -= 1
            channel.save()
            subscribe.delete()
            return Response({'data': {'subscribe': 0}, 'message': 'Subscription removed 🤡', 'status': 'ok'})

        elif subscribe.count() == 0:
            channel.all_subscribers += 1
            channel.save()
            Subscribe.objects.create(subscriber=request.user, channel=channel)
            return Response({'data': {'subscribe': 1}, 'message': 'Subscription added 🤗', 'status': 'ok'})

        else:
            return Response({'data': {}, 'status': 'err'})

# notifications
class NotificationsApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        channel = CustomUser.objects.get(user_id=request.data.get('user_id'))
        notification = Notification.objects.filter(notification_user=request.user, notification_channel=channel)

        if notification.count() > 0:
            channel.all_notifications -= 1
            channel.save()
            notification.delete()
            return Response({'data': {'notification': 0}, 'message': 'Notifications turned off for this channel 😬', 'status': 'ok'})

        elif notification.count() == 0:
            channel.all_notifications += 1
            channel.save()
            Notification.objects.create(notification_channel=channel, notification_user=request.user)
            return Response({'data': {'notification': 1}, 'message': 'You’ll get all notifications 😃', 'status': 'ok'})

        else:
            return Response({'data': {}, 'status': 'err'})


# delete video
class DeleteVideoApi(APIView):
    def post(self, request):
        video_id = request.data.get('video_id')
        video = Video.objects.filter(video_id=video_id)
        if video.count() > 0:
            if video[0].creator == request.user:
                title = video[0].title
                video[0].delete()
                messages.success(request, f'<b>{title}</b>, successfully deleted! 🎃')
                return Response({'data': {}, 'status': 'ok'})
            else:
                return Response({'data': {}, 'message': 'You are not authorized to delete this video because you are not its creator', 'status': 'err'})
        else:
            return Response({'data': {}, 'message': 'Video not found', 'status': 'err'})

# save video
class SaveVideoApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        video = Video.objects.get(video_id=request.data.get('video_id'))
        save = SavedVideo.objects.filter(saved_video=video, saved_user=request.user)

        if save.count() > 0:
            save.delete()
            return Response({'data': {'save': 0}, 'message': 'Removed from Saved videos ✂️', 'status': 'ok'})

        elif save.count() == 0:
            SavedVideo.objects.create(saved_video=video, saved_user=request.user)
            return Response({'data': {'save': 1}, 'message': 'Added to Saved videos 📌', 'status': 'ok'})

        else:
            return Response({'data': {}, 'status': 'err'})

# like video
class LikeVideoApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        video = Video.objects.get(video_id=request.data.get('video_id'))
        like = Like.objects.filter(liked_video=video, liked_user=request.user)
        dislike = Dislike.objects.filter(disliked_video=video, disliked_user=request.user)

        if like.count() == 0 and dislike.count() == 0:
            like = Like.objects.create(liked_video=video, liked_user=request.user)
            if like:
                video.likes += 1
                video.save()
                video.creator.all_likes += 1
                video.creator.save()
            return Response({'data': {'like': 1, 'dislike': 0, 'stats': {'likes': video.likes, 'dislikes': video.dislikes}}, 'message': 'Added to Liked videos 👍', 'status': 'ok'})

        elif like.count() == 1 and dislike.count() == 0:
            like[0].delete()
            video.likes -= 1
            video.save()
            video.creator.all_likes -= 1
            video.creator.save()
            return Response({'data': {'like': 0, 'dislike': 0, 'stats': {'likes': video.likes, 'dislikes': video.dislikes}}, 'message': 'Removed from Liked videos 👀', 'status': 'ok'})

        elif like.count() == 0 and dislike.count() == 1:
            video.dislikes -= 1
            video.likes += 1
            video.save()

            video.creator.all_dislikes -= 1
            video.creator.all_likes += 1
            video.creator.save()

            dislike[0].delete()
            like = Like.objects.create(liked_video=video, liked_user=request.user)
            return Response({'data': {'like': 1, 'dislike': 0, 'stats': {'likes': video.likes, 'dislikes': video.dislikes}}, 'message': 'Added to Liked videos 👍', 'status': 'ok'})

        else:
            return Response({'data': {}, 'status': 'err'})

# dislike video
class DislikeVideoApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        video = Video.objects.get(video_id=request.data.get('video_id'))
        like = Like.objects.filter(liked_video=video, liked_user=request.user)
        dislike = Dislike.objects.filter(disliked_video=video, disliked_user=request.user)

        if like.count() == 0 and dislike.count() == 0:
            dislike = Dislike.objects.create(disliked_video=video, disliked_user=request.user)
            if dislike:
                video.dislikes += 1
                video.save()
                video.creator.all_dislikes += 1
                video.creator.save()
            return Response({'data': {'like': 0, 'dislike': 1, 'stats': {'likes': video.likes, 'dislikes': video.dislikes}}, 'message': 'You dislike this video 👎', 'status': 'ok'})

        elif dislike.count() == 1 and like.count() == 0:
            dislike[0].delete()
            video.dislikes -= 1
            video.save()
            video.creator.all_dislikes -= 1
            video.creator.save()
            return Response({'data': {'like': 0, 'dislike': 0, 'stats': {'likes': video.likes, 'dislikes': video.dislikes}}, 'message': 'Dislike removed 😎', 'status': 'ok'})

        elif dislike.count() == 0 and like.count() == 1:
            video.likes -= 1
            video.dislikes += 1
            video.save()

            video.creator.all_likes -= 1
            video.creator.all_dislikes += 1
            video.creator.save()

            like[0].delete()
            dislike = Dislike.objects.create(disliked_video=video, disliked_user=request.user)
            return Response({'data': {'like': 0, 'dislike': 1, 'stats': {'likes': video.likes, 'dislikes': video.dislikes}}, 'message': 'You dislike this video 👎', 'status': 'ok'})

        else:
            return Response({'data': {}, 'status': 'err'})


# add comment
class AddCommentApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        video = Video.objects.get(video_id=request.data.get('video_id'))
        text = request.data.get('text')

        if text.replace(' ', '') != '' and text is not None:
            Comment.objects.create(commented_video=video, creator=request.user, comment_id=generate_id(32), comment_text=text)
            video.comments += 1
            video.save()
            video.creator.all_comments += 1
            video.creator.save()
            return Response({'data': {}, 'message': 'Comment added 🌚', 'status': 'ok'})
        else:
            return Response({'data': {}, 'message': 'Comment cannot contain spaces or be empty 🙉', 'status': 'err'})            

# like comment
class LikeCommentApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        comment = Comment.objects.get(comment_id=request.data.get('comment_id'))
        like = CommentLike.objects.filter(liked_comment=comment, liked_user=request.user)
        dislike = CommentDislike.objects.filter(disliked_comment=comment, disliked_user=request.user)

        if like.count() == 0 and dislike.count() == 0:
            like = CommentLike.objects.create(liked_comment=comment, liked_user=request.user)
            if like:
                comment.likes += 1
                comment.save()
            return Response({'data': {'like': 1, 'dislike': 0, 'stats': {'likes': comment.likes, 'dislikes': comment.dislikes}}, 'message': '', 'status': 'ok'})

        elif like.count() == 1 and dislike.count() == 0:
            like[0].delete()
            comment.likes -= 1
            comment.save()
            return Response({'data': {'like': 0, 'dislike': 0, 'stats': {'likes': comment.likes, 'dislikes': comment.dislikes}}, 'message': '', 'status': 'ok'})

        elif like.count() == 0 and dislike.count() == 1:
            comment.dislikes -= 1
            comment.likes += 1
            comment.save()
            dislike[0].delete()
            like = CommentLike.objects.create(liked_comment=comment, liked_user=request.user)
            return Response({'data': {'like': 1, 'dislike': 0, 'stats': {'likes': comment.likes, 'dislikes': comment.dislikes}}, 'message': '', 'status': 'ok'})

        else:
            return Response({'data': {}, 'status': 'err'})

# dislike comment
class DislikeCommentApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        comment = Comment.objects.get(comment_id=request.data.get('comment_id'))
        like = CommentLike.objects.filter(liked_comment=comment, liked_user=request.user)
        dislike = CommentDislike.objects.filter(disliked_comment=comment, disliked_user=request.user)

        if like.count() == 0 and dislike.count() == 0:
            dislike = CommentDislike.objects.create(disliked_comment=comment, disliked_user=request.user)
            if dislike:
                comment.dislikes += 1
                comment.save()
            return Response({'data': {'like': 0, 'dislike': 1, 'stats': {'likes': comment.likes, 'dislikes': comment.dislikes}}, 'message': '', 'status': 'ok'})

        elif dislike.count() == 1 and like.count() == 0:
            dislike[0].delete()
            comment.dislikes -= 1
            comment.save()
            return Response({'data': {'like': 0, 'dislike': 0, 'stats': {'likes': comment.likes, 'dislikes': comment.dislikes}}, 'message': '', 'status': 'ok'})

        elif dislike.count() == 0 and like.count() == 1:
            comment.likes -= 1
            comment.dislikes += 1
            comment.save()
            like[0].delete()
            dislike = CommentDislike.objects.create(disliked_comment=comment, disliked_user=request.user)
            return Response({'data': {'like': 0, 'dislike': 1, 'stats': {'likes': comment.likes, 'dislikes': comment.dislikes}}, 'message': '', 'status': 'ok'})

        else:
            return Response({'data': {}, 'status': 'err'})

# delete comment
class DeleteCommentApi(APIView):
    def post(self, request):
        comment_id = request.data.get('comment_id')
        comment = Comment.objects.filter(comment_id=comment_id)
        if comment.count() > 0:
            if comment[0].creator == request.user:
                video = comment[0].commented_video 
                video.comments -= (1 + comment[0].replies)
                video.save()
                video.creator.all_comments -= 1
                video.creator.save()
                comment[0].delete()
                return Response({'data': {}, 'message': 'Comment has been deleted 🧸', 'status': 'ok'})
            else:
                return Response({'data': {}, 'message': 'You are not authorized to delete this comment because you are not its creator', 'status': 'err'})
        else:
            return Response({'data': {}, 'message': 'Comment not found', 'status': 'err'})

# add reply comment
class AddReplyCommentApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        video = Video.objects.get(video_id=request.data.get('video_id'))
        comment = Comment.objects.get(comment_id=request.data.get('comment_id'))
        text = request.data.get('text')

        if text.replace(' ', '') != '' and text is not None:
            ReplyComment.objects.create(reply_commented_video=video, comment_parent=comment, creator=request.user, reply_comment_id=generate_id(32), comment_text=text)
            comment.replies += 1
            comment.save()
            video.comments += 1
            video.save()    
            video.creator.all_comments += 1
            video.creator.save()
            return Response({'data': {}, 'message': 'Reply to comment added ⛄️', 'status': 'ok'})
        else:
            return Response({'data': {}, 'message': 'Comment cannot contain spaces or be empty 🙉', 'status': 'err'})            

# like reply comment
class LikeReplyCommentApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        comment = ReplyComment.objects.get(reply_comment_id=request.data.get('reply_comment_id'))
        like = ReplyCommentLike.objects.filter(liked_reply_comment=comment, liked_user=request.user)
        dislike = ReplyCommentDislike.objects.filter(disliked_reply_comment=comment, disliked_user=request.user)

        if like.count() == 0 and dislike.count() == 0:
            like = ReplyCommentLike.objects.create(liked_reply_comment=comment, liked_user=request.user)
            if like:
                comment.likes += 1
                comment.save()
            return Response({'data': {'like': 1, 'dislike': 0, 'stats': {'likes': comment.likes, 'dislikes': comment.dislikes}}, 'message': '', 'status': 'ok'})

        elif like.count() == 1 and dislike.count() == 0:
            like[0].delete()
            comment.likes -= 1
            comment.save()
            return Response({'data': {'like': 0, 'dislike': 0, 'stats': {'likes': comment.likes, 'dislikes': comment.dislikes}}, 'message': '', 'status': 'ok'})

        elif like.count() == 0 and dislike.count() == 1:
            comment.dislikes -= 1
            comment.likes += 1
            comment.save()
            dislike[0].delete()
            like = ReplyCommentLike.objects.create(liked_reply_comment=comment, liked_user=request.user)
            return Response({'data': {'like': 1, 'dislike': 0, 'stats': {'likes': comment.likes, 'dislikes': comment.dislikes}}, 'message': '', 'status': 'ok'})

        else:
            return Response({'data': {}, 'status': 'err'})

# dislike comment
class DislikeReplyCommentApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        comment = ReplyComment.objects.get(reply_comment_id=request.data.get('reply_comment_id'))
        like = ReplyCommentLike.objects.filter(liked_reply_comment=comment, liked_user=request.user)
        dislike = ReplyCommentDislike.objects.filter(disliked_reply_comment=comment, disliked_user=request.user)

        if like.count() == 0 and dislike.count() == 0:
            dislike = ReplyCommentDislike.objects.create(disliked_reply_comment=comment, disliked_user=request.user)
            if dislike:
                comment.dislikes += 1
                comment.save()
            return Response({'data': {'like': 0, 'dislike': 1, 'stats': {'likes': comment.likes, 'dislikes': comment.dislikes}}, 'message': '', 'status': 'ok'})

        elif dislike.count() == 1 and like.count() == 0:
            dislike[0].delete()
            comment.dislikes -= 1
            comment.save()
            return Response({'data': {'like': 0, 'dislike': 0, 'stats': {'likes': comment.likes, 'dislikes': comment.dislikes}}, 'message': '', 'status': 'ok'})

        elif dislike.count() == 0 and like.count() == 1:
            comment.likes -= 1
            comment.dislikes += 1
            comment.save()
            like[0].delete()
            dislike = ReplyCommentDislike.objects.create(disliked_reply_comment=comment, disliked_user=request.user)
            return Response({'data': {'like': 0, 'dislike': 1, 'stats': {'likes': comment.likes, 'dislikes': comment.dislikes}}, 'message': '', 'status': 'ok'})

        else:
            return Response({'data': {}, 'status': 'err'})

# delete comment
class DeleteReplyCommentApi(APIView):
    def post(self, request):
        reply_comment_id = request.data.get('reply_comment_id')
        comment = ReplyComment.objects.filter(reply_comment_id=reply_comment_id)
        if comment.count() > 0:
            if comment[0].creator == request.user:
                video = comment[0].reply_commented_video 
                comment_parent = comment[0].comment_parent
                comment_parent.replies -= 1
                comment_parent.save()
                video.comments -= 1 
                video.save()
                video.creator.all_comments -= 1
                video.creator.save()
                comment[0].delete()
                return Response({'data': {}, 'message': 'Comment has been deleted 🧸', 'status': 'ok'})
            else:
                return Response({'data': {}, 'message': 'You are not authorized to delete this comment because you are not its creator', 'status': 'err'})
        else:
            return Response({'data': {}, 'message': 'Comment not found', 'status': 'err'})


# get video stats
class VideoStatsApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        video = Video.objects.get(video_id=request.data.get('video_id'))
 
        views_stats = {}
        comments_stats = {}
        likes_stats = {}
        dislikes_stats = {}

        from django.utils import timezone
        import pytz
        from datetime import date

        #today = datetime.utcnow()
        today = date.today()
   
    
        for i in range(10):
            day = today - timedelta(days=i)
            views = VideoViewModel.objects.filter(watched_video=video, date_created__gt=(day))
            comments = Comment.objects.filter(commented_video=video, date_created__gt=(day))
            reply_comments = ReplyComment.objects.filter(reply_commented_video=video, date_created__gt=(day))
            likes = Like.objects.filter(liked_video=video, date_created__gt=(day))
            dislikes = Dislike.objects.filter(disliked_video=video, date_created__gt=(day))

            views_stats[str(day)] = len(views)
            comments_stats[str(day)] = len(comments) + len(reply_comments)
            likes_stats[str(day)] = len(likes)
            dislikes_stats[str(day)] = len(dislikes)

        return Response({'data': {'views': views_stats, 'comments': comments_stats, 'likes': likes_stats, 'dislikes': dislikes_stats}, 'message': '', 'status': 'ok'})     


# like film
class LikeFilmApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        film = Film.objects.get(film_id=request.data.get('film_id'))
        like = FilmLike.objects.filter(liked_film=film, liked_user=request.user)
        dislike = FilmDislike.objects.filter(disliked_film=film, disliked_user=request.user)

        if like.count() == 0 and dislike.count() == 0:
            like = FilmLike.objects.create(liked_film=film, liked_user=request.user)
            if like:
                film.likes += 1
                film.save()
            return Response({'data': {'like': 1, 'dislike': 0, 'stats': {'likes': film.likes, 'dislikes': film.dislikes}}, 'message': 'Your liked this film 🧡', 'status': 'ok'})

        elif like.count() == 1 and dislike.count() == 0:
            like[0].delete()
            film.likes -= 1
            film.save()
            return Response({'data': {'like': 0, 'dislike': 0, 'stats': {'likes': film.likes, 'dislikes': film.dislikes}}, 'message': 'Like removed 🧸', 'status': 'ok'})

        elif like.count() == 0 and dislike.count() == 1:
            film.dislikes -= 1
            film.likes += 1
            film.save()
            dislike[0].delete()
            like = FilmLike.objects.create(liked_film=film, liked_user=request.user)
            return Response({'data': {'like': 1, 'dislike': 0, 'stats': {'likes': film.likes, 'dislikes': film.dislikes}}, 'message': 'Your liked this film 🧡', 'status': 'ok'})

        else:
            return Response({'data': {}, 'status': 'err'})

# dislike film
class DislikeFilmApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        film = Film.objects.get(film_id=request.data.get('film_id'))
        like = FilmLike.objects.filter(liked_film=film, liked_user=request.user)
        dislike = FilmDislike.objects.filter(disliked_film=film, disliked_user=request.user)

        if like.count() == 0 and dislike.count() == 0:
            dislike = FilmDislike.objects.create(disliked_film=film, disliked_user=request.user)
            if dislike:
                film.dislikes += 1
                film.save()
            return Response({'data': {'like': 0, 'dislike': 1, 'stats': {'likes': film.likes, 'dislikes': film.dislikes}}, 'message': 'Your disliked this film 💔', 'status': 'ok'})

        elif dislike.count() == 1 and like.count() == 0:
            dislike[0].delete()
            film.dislikes -= 1
            film.save()
            return Response({'data': {'like': 0, 'dislike': 0, 'stats': {'likes': film.likes, 'dislikes': film.dislikes}}, 'message': 'Dislike removed 🥶', 'status': 'ok'})

        elif dislike.count() == 0 and like.count() == 1:
            film.likes -= 1
            film.dislikes += 1
            film.save()
            like[0].delete()
            dislike = FilmDislike.objects.create(disliked_film=film, disliked_user=request.user)
            return Response({'data': {'like': 0, 'dislike': 1, 'stats': {'likes': film.likes, 'dislikes': film.dislikes}}, 'message': 'Your disliked this film 💔', 'status': 'ok'})

        else:
            return Response({'data': {}, 'status': 'err'})

# buy film
class BuyFilmApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        film = Film.objects.get(film_id=request.data.get('film_id'))
        BuyFilm.objects.create(buy_user=request.user, buy_film=film)

        if request.user.telegram:
            now = datetime.now() 
            date = now.strftime('%d-%m-%Y %H:%M:%S')
            YandexHubAlert(f'You purchased the movie: {film.title} 🥳\nDate: {date}\nPrice: USD {film.price}\n\n{DOMEN}film/{film.film_id}/', request.user.telegram)


        messages.success(self.request, f'You purchased the movie: <b>{film.title}</b> 🥳')
        return Response({'data': {}, 'status': 'ok'})

# delete article
class DeleteArticleApi(APIView):
    def post(self, request):
        article_id = request.data.get('article_id')
        article = Article.objects.filter(article_id=article_id)
        if article.count() > 0:
            if article[0].creator == request.user:
                article[0].delete()
                messages.success(request, f'Article successfully deleted! 🩸')
                return Response({'data': {'user_id': request.user.user_id}, 'status': 'ok'})
            else:
                return Response({'data': {}, 'message': 'You are not authorized to delete this article because you are not its creator', 'status': 'err'})
        else:
            return Response({'data': {}, 'message': 'Article not found', 'status': 'err'})

# like article
class LikeArticleApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        article = Article.objects.get(article_id=request.data.get('article_id'))
        like = ArticleLike.objects.filter(liked_article=article, liked_user=request.user)
        dislike = ArticleDislike.objects.filter(disliked_article=article, disliked_user=request.user)

        if like.count() == 0 and dislike.count() == 0:
            like = ArticleLike.objects.create(liked_article=article, liked_user=request.user)
            if like:
                article.likes += 1
                article.save()
                article.creator.all_posts_likes += 1
                article.creator.save()
            return Response({'data': {'like': 1, 'dislike': 0, 'stats': {'likes': article.likes, 'dislikes': article.dislikes}}, 'message': 'You like this article 👍', 'status': 'ok'})

        elif like.count() == 1 and dislike.count() == 0:
            like[0].delete()
            article.likes -= 1
            article.save()
            article.creator.all_posts_likes -= 1
            article.creator.save()
            return Response({'data': {'like': 0, 'dislike': 0, 'stats': {'likes': article.likes, 'dislikes': article.dislikes}}, 'message': 'Like removed 👀', 'status': 'ok'})

        elif like.count() == 0 and dislike.count() == 1:
            article.dislikes -= 1
            article.likes += 1
            article.save()

            article.creator.all_posts_dislikes -= 1
            article.creator.all_posts_likes += 1
            article.creator.save()

            dislike[0].delete()
            like = ArticleLike.objects.create(liked_article=article, liked_user=request.user)
            return Response({'data': {'like': 1, 'dislike': 0, 'stats': {'likes': article.likes, 'dislikes': article.dislikes}}, 'message': 'You like this article 👍', 'status': 'ok'})

        else:
            return Response({'data': {}, 'status': 'err'})

# dislike article
class DislikeArticleApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        article = Article.objects.get(article_id=request.data.get('article_id'))
        like = ArticleLike.objects.filter(liked_article=article, liked_user=request.user)
        dislike = ArticleDislike.objects.filter(disliked_article=article, disliked_user=request.user)

        if like.count() == 0 and dislike.count() == 0:
            dislike = ArticleDislike.objects.create(disliked_article=article, disliked_user=request.user)
            if dislike:
                article.dislikes += 1
                article.save()
                article.creator.all_posts_dislikes += 1
                article.creator.save()
            return Response({'data': {'like': 0, 'dislike': 1, 'stats': {'likes': article.likes, 'dislikes': article.dislikes}}, 'message': 'You dislike this article 👎', 'status': 'ok'})

        elif dislike.count() == 1 and like.count() == 0:
            dislike[0].delete()
            article.dislikes -= 1
            article.save()
            article.creator.all_posts_dislikes -= 1
            article.creator.save()
            return Response({'data': {'like': 0, 'dislike': 0, 'stats': {'likes': article.likes, 'dislikes': article.dislikes}}, 'message': 'Dislike removed 😎', 'status': 'ok'})

        elif dislike.count() == 0 and like.count() == 1:
            article.likes -= 1
            article.dislikes += 1
            article.save()

            article.creator.all_posts_likes -= 1
            article.creator.all_posts_dislikes += 1
            article.creator.save()
            
            like[0].delete()
            dislike = ArticleDislike.objects.create(disliked_article=article, disliked_user=request.user)
            return Response({'data': {'like': 0, 'dislike': 1, 'stats': {'likes': article.likes, 'dislikes': article.dislikes}}, 'message': 'You dislike this article 👎', 'status': 'ok'})

        else:
            return Response({'data': {}, 'status': 'err'})
