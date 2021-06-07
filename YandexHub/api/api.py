# DRF
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser, FormParser

# DRF AUTH
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token

# DJNAGO
from django.http import FileResponse

# MODELS
from django.db.models import Q
from mainapp.models import *

# DATE/TIME
from datetime import date, datetime, timedelta

# MESSAGES
from django.contrib import messages

# VIEWS FUNCS
from mainapp.views import bot, DOMEN, MAX_IMAGE_SIZE, MAX_VIDEO_SIZE

# SERIALIZERS
from .serializers import *

# HELPERS
from mainapp.helpers import generate_id

# LIKES FORMAT
from mainapp.templatetags.poll_extras import brief_likes_format

# TASKS
from mainapp.tasks import send_notification


# subscribe to user
class SubscribeApi(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'channel_id' in request.data:
            channel = CustomUser.objects.filter(
                user_id=request.data.get('channel_id'))
            if channel:
                channel = channel[0]
                if request.user != channel:
                    subscribe = Subscribe.objects.filter(
                        subscriber=request.user,
                        channel=channel
                    )

                    if subscribe.count() > 0:
                        channel.all_subscribers -= 1
                        channel.save()
                        subscribe.delete()
                        return Response({
                            'data': {
                                'subscribe': 0
                            },
                            'message': 'Subscription removed 🤡',
                            'status': 'ok'
                        }, status=status.HTTP_200_OK)

                    elif subscribe.count() == 0:
                        channel.all_subscribers += 1
                        channel.save()
                        Subscribe.objects.create(
                            subscriber=request.user,
                            channel=channel
                        )
                        return Response({
                            'data': {
                                'subscribe': 1
                            },
                            'message': 'Subscription added 🤗',
                            'status': 'ok'
                        }, status=status.HTTP_200_OK)

                    else:
                        return Response({'data': {}, 'status': 'err'}, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'data': {},
                        'message': 'Unable to subscribe to yourself 😬',
                        'status': 'err'
                    }, status=status.HTTP_200_OK)
            else:
                return Response({'data': {}, 'message': 'User nor found', 'status': 'err'}, status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# notifications
class NotificationsApi(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'user_id' in request.data:
            channel = CustomUser.objects.filter(
                user_id=request.data.get('user_id'))
            if channel:
                channel = channel[0]
                notification = Notification.objects.filter(
                    notification_user=request.user,
                    notification_channel=channel
                )

                if notification.count() > 0:
                    channel.all_notifications -= 1
                    channel.save()
                    notification.delete()
                    return Response({
                        'data': {
                            'notification': 0
                        },
                        'message': 'Notifications turned off for this channel 😬',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                elif notification.count() == 0:
                    channel.all_notifications += 1
                    channel.save()
                    Notification.objects.create(
                        notification_channel=channel, notification_user=request.user)
                    return Response({
                        'data': {
                            'notification': 1
                        },
                        'message': 'You’ll get all notifications 😃',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                else:
                    return Response({'data': {}, 'status': 'err'}, status=status.HTTP_200_OK)
            else:
                return Response({'data': {}, 'message': 'User nor found', 'status': 'err'}, status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# delete video
class DeleteVideoApi(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'video_id' in request.data:
            video = Video.objects.filter(video_id=request.data.get('video_id'))
            if video.count() > 0:
                if video[0].creator == request.user:
                    title = video[0].title
                    video[0].delete()
                    messages.success(
                        request, f'<b>{title}</b>, successfully deleted! 🎃'
                    )
                    return Response({'data': {}, 'status': 'ok'}, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'data': {},
                        'message': 'You are not authorized to delete this video because you are not its creator',
                        'status': 'err'
                    })
            else:
                return Response({'data': {}, 'message': 'Video not found', 'status': 'err'}, status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# delete track
class DeleteTrackApi(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'track_id' in request.data:
            track = Track.objects.filter(track_id=request.data.get('track_id'))
            if track.count() > 0:
                if track[0].creator == request.user:
                    title = track[0].title
                    track[0].delete()
                    messages.success(
                        request, f'<b>{title}</b>, successfully deleted! 🎃'
                    )
                    return Response({'data': {}, 'status': 'ok'}, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'data': {},
                        'message': 'You are not authorized to delete this track because you are not its creator',
                        'status': 'err'
                    })
            else:
                return Response({
                    'data': {},
                    'message': 'Track not found',
                    'status': 'err'
                }, status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# save video
class SaveVideoApi(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'video_id' in request.data:
            video = Video.objects.filter(video_id=request.data.get('video_id'))
            if video.count() > 0:
                video = video[0]
                save = SavedVideo.objects.filter(
                    saved_video=video,
                    saved_user=request.user
                )

                if save.count() > 0:
                    save.delete()
                    return Response({
                        'data': {
                            'save': 0
                        },
                        'message': 'Removed from Saved videos ✂️',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                elif save.count() == 0:
                    SavedVideo.objects.create(
                        saved_video=video, saved_user=request.user)
                    return Response({
                        'data': {
                            'save': 1
                        },
                        'message': 'Added to Saved videos 📌',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                else:
                    return Response({'data': {}, 'status': 'err'}, status=status.HTTP_200_OK)
            else:
                return Response({'data': {}, 'message': 'Video not found', 'status': 'err'}, status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# like video
class LikeVideoApi(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'video_id' in request.data:
            video = Video.objects.filter(video_id=request.data.get('video_id'))
            if video.count() > 0:
                video = video[0]
                like = Like.objects.filter(
                    liked_video=video,
                    liked_user=request.user
                )
                dislike = Dislike.objects.filter(
                    disliked_video=video,
                    disliked_user=request.user
                )

                if like.count() == 0 and dislike.count() == 0:
                    like = Like.objects.create(
                        liked_video=video,
                        liked_user=request.user
                    )
                    if like:
                        video.likes += 1
                        video.save()
                        video.creator.all_likes += 1
                        video.creator.save()
                    return Response({
                        'data': {
                            'like': 1,
                            'dislike': 0,
                            'stats': {
                                'likes': brief_likes_format(video.likes),
                                'dislikes': brief_likes_format(video.dislikes)
                            }
                        },
                        'message': 'Added to Liked videos 👍',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                elif like.count() == 1 and dislike.count() == 0:
                    like[0].delete()
                    video.likes -= 1
                    video.save()
                    video.creator.all_likes -= 1
                    video.creator.save()
                    return Response({
                        'data': {
                            'like': 0,
                            'dislike': 0,
                            'stats': {
                                'likes': brief_likes_format(video.likes),
                                'dislikes': brief_likes_format(video.dislikes)
                            }
                        },
                        'message': 'Removed from Liked videos 👀',
                        'status': 'ok'
                    },  status=status.HTTP_200_OK)

                elif like.count() == 0 and dislike.count() == 1:
                    video.dislikes -= 1
                    video.likes += 1
                    video.save()

                    video.creator.all_dislikes -= 1
                    video.creator.all_likes += 1
                    video.creator.save()

                    dislike[0].delete()
                    like = Like.objects.create(
                        liked_video=video, liked_user=request.user)
                    return Response({
                        'data': {
                            'like': 1,
                            'dislike': 0,
                            'stats': {
                                'likes': brief_likes_format(video.likes),
                                'dislikes': brief_likes_format(video.dislikes)
                            }
                        },
                        'message': 'Added to Liked videos 👍',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                else:
                    return Response({'data': {}, 'status': 'err'}, status=status.HTTP_200_OK)
            else:
                return Response({'data': {}, 'message': 'Video not found', 'status': 'err'}, status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# dislike video
class DislikeVideoApi(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'video_id' in request.data:
            video = Video.objects.filter(video_id=request.data.get('video_id'))
            if video.count() > 0:
                video = video[0]
                like = Like.objects.filter(
                    liked_video=video,
                    liked_user=request.user
                )
                dislike = Dislike.objects.filter(
                    disliked_video=video,
                    disliked_user=request.user
                )

                if like.count() == 0 and dislike.count() == 0:
                    dislike = Dislike.objects.create(
                        disliked_video=video,
                        disliked_user=request.user
                    )
                    if dislike:
                        video.dislikes += 1
                        video.save()
                        video.creator.all_dislikes += 1
                        video.creator.save()
                    return Response({
                        'data': {
                            'like': 0,
                            'dislike': 1,
                            'stats': {
                                'likes': brief_likes_format(video.likes),
                                'dislikes': brief_likes_format(video.dislikes)
                            }
                        },
                        'message': 'You dislike this video 👎',
                        'status': 'ok'}, status=status.HTTP_200_OK)

                elif dislike.count() == 1 and like.count() == 0:
                    dislike[0].delete()
                    video.dislikes -= 1
                    video.save()
                    video.creator.all_dislikes -= 1
                    video.creator.save()
                    return Response({
                        'data': {
                            'like': 0,
                            'dislike': 0,
                            'stats': {
                                'likes': brief_likes_format(video.likes),
                                'dislikes': brief_likes_format(video.dislikes)
                            }
                        },
                        'message': 'Dislike removed 😎',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                elif dislike.count() == 0 and like.count() == 1:
                    video.likes -= 1
                    video.dislikes += 1
                    video.save()

                    video.creator.all_likes -= 1
                    video.creator.all_dislikes += 1
                    video.creator.save()

                    like[0].delete()
                    dislike = Dislike.objects.create(
                        disliked_video=video,
                        disliked_user=request.user
                    )
                    return Response({
                        'data': {
                            'like': 0,
                            'dislike': 1,
                            'stats': {
                                'likes': brief_likes_format(video.likes),
                                'dislikes': brief_likes_format(video.dislikes)
                            }
                        },
                        'message': 'You dislike this video 👎',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                else:
                    return Response({'data': {}, 'status': 'err'}, status=status.HTTP_200_OK)
            else:
                return Response({'data': {}, 'message': 'Video not found', 'status': 'err'}, status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# add comment
class AddCommentApi(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'video_id' in request.data and 'text' in request.data:
            video = Video.objects.filter(video_id=request.data.get('video_id'))
            if video.count() > 0:
                video = video[0]
                text = request.data.get('text')
                if len(text) < 500:
                    if text.replace(' ', '') != '' and text is not None:
                        # maximum 10 comments per day (one user)
                        today = date.today()
                        if Comment.objects.filter(
                            commented_video=video,
                            creator=request.user,
                            date_created_without_time=today
                        ).count() < 10:
                            Comment.objects.create(
                                commented_video=video,
                                creator=request.user,
                                comment_id=generate_id(32),
                                comment_text=text
                            )
                            video.comments += 1
                            video.save()
                            video.creator.all_comments += 1
                            video.creator.save()
                            return Response({'data': {}, 'message': 'Comment added 🌚', 'status': 'ok'})
                        else:
                            return Response({
                                'data': {},
                                'message': 'You have exceeded the comment limit for one video today 😥',
                                'status': 'err'
                            }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            'data': {},
                            'message': 'Comment cannot contain spaces or be empty 🙉',
                            'status': 'err'
                        }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'data': {},
                        'message': 'Maximum text length 500 characters 🥴',
                        'status': 'err'
                    }, status=status.HTTP_200_OK)
            else:
                return Response({'data': {}, 'message': 'Video not found', 'status': 'err'}, status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# like comment
class LikeCommentApi(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'comment_id' in request.data:
            comment = Comment.objects.filter(
                comment_id=request.data.get('comment_id'))
            if comment.count() > 0:
                comment = comment[0]
                like = CommentLike.objects.filter(
                    liked_comment=comment,
                    liked_user=request.user
                )
                dislike = CommentDislike.objects.filter(
                    disliked_comment=comment,
                    disliked_user=request.user
                )

                if like.count() == 0 and dislike.count() == 0:
                    like = CommentLike.objects.create(
                        liked_comment=comment,
                        liked_user=request.user
                    )
                    if like:
                        comment.likes += 1
                        comment.save()
                    return Response({
                        'data': {
                            'like': 1,
                            'dislike': 0,
                            'stats': {
                                'likes': brief_likes_format(comment.likes),
                                'dislikes': brief_likes_format(comment.dislikes)
                            }
                        },
                        'message': '',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                elif like.count() == 1 and dislike.count() == 0:
                    like[0].delete()
                    comment.likes -= 1
                    comment.save()
                    return Response({
                        'data': {
                            'like': 0,
                            'dislike': 0,
                            'stats': {
                                'likes': brief_likes_format(comment.likes),
                                'dislikes': brief_likes_format(comment.dislikes)
                            }
                        },
                        'message': '',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                elif like.count() == 0 and dislike.count() == 1:
                    comment.dislikes -= 1
                    comment.likes += 1
                    comment.save()
                    dislike[0].delete()
                    like = CommentLike.objects.create(
                        liked_comment=comment,
                        liked_user=request.user
                    )
                    return Response({
                        'data': {
                            'like': 1,
                            'dislike': 0,
                            'stats': {
                                'likes': brief_likes_format(comment.likes),
                                'dislikes': brief_likes_format(comment.dislikes)
                            }
                        },
                        'message': '',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                else:
                    return Response({'data': {}, 'status': 'err'}, status=status.HTTP_200_OK)
            else:
                return Response({'data': {}, 'message': 'Comment not found', 'status': 'err'}, status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# dislike comment
class DislikeCommentApi(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'comment_id' in request.data:
            comment = Comment.objects.filter(
                comment_id=request.data.get('comment_id'))
            if comment.count() > 0:
                comment = comment[0]
                like = CommentLike.objects.filter(
                    liked_comment=comment,
                    liked_user=request.user
                )
                dislike = CommentDislike.objects.filter(
                    disliked_comment=comment,
                    disliked_user=request.user
                )

                if like.count() == 0 and dislike.count() == 0:
                    dislike = CommentDislike.objects.create(
                        disliked_comment=comment,
                        disliked_user=request.user
                    )
                    if dislike:
                        comment.dislikes += 1
                        comment.save()
                    return Response({
                        'data': {
                            'like': 0,
                            'dislike': 1,
                            'stats': {
                                'likes': brief_likes_format(comment.likes),
                                'dislikes': brief_likes_format(comment.dislikes)
                            }
                        },
                        'message': '',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                elif dislike.count() == 1 and like.count() == 0:
                    dislike[0].delete()
                    comment.dislikes -= 1
                    comment.save()
                    return Response({
                        'data': {
                            'like': 0,
                            'dislike': 0,
                            'stats': {
                                'likes': brief_likes_format(comment.likes),
                                'dislikes': brief_likes_format(comment.dislikes)
                            }
                        },
                        'message': '',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                elif dislike.count() == 0 and like.count() == 1:
                    comment.likes -= 1
                    comment.dislikes += 1
                    comment.save()
                    like[0].delete()
                    dislike = CommentDislike.objects.create(
                        disliked_comment=comment,
                        disliked_user=request.user
                    )
                    return Response({
                        'data': {
                            'like': 0,
                            'dislike': 1,
                            'stats': {
                                'likes': brief_likes_format(comment.likes),
                                'dislikes': brief_likes_format(comment.dislikes)
                            }
                        },
                        'message': '',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                else:
                    return Response({'data': {}, 'status': 'err'}, status=status.HTTP_200_OK)
            else:
                return Response({
                    'data': {},
                    'message': 'Comment not found',
                    'status': 'err'
                }, status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# delete comment
class DeleteCommentApi(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'comment_id' in request.data:
            comment = Comment.objects.filter(
                comment_id=request.data.get('comment_id'))
            if comment.count() > 0:
                if comment[0].creator == request.user:
                    video = comment[0].commented_video
                    video.comments -= (1 + comment[0].replies)
                    video.save()
                    video.creator.all_comments -= 1
                    video.creator.save()
                    comment[0].delete()
                    return Response({
                        'data': {},
                        'message': 'Comment has been deleted 🧸',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'data': {},
                        'message': 'You are not authorized to delete this comment because you are not its creator',
                        'status': 'err'
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'data': {},
                    'message': 'Comment not found',
                    'status': 'err'
                }, status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# add reply comment
class AddReplyCommentApi(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'video_id' in request.data and 'comment_id' in request.data and 'text' in request.data:
            video = Video.objects.filter(video_id=request.data.get('video_id'))
            if video.count() > 0:
                video = video[0]
                comment = Comment.objects.filter(
                    comment_id=request.data.get('comment_id'))
                if comment.count() > 0:
                    comment = comment[0]
                    text = request.data.get('text')
                    if len(text) < 500:
                        if text.replace(' ', '') != '' and text is not None:
                            # maximum 10 replies per day (one user)
                            today = date.today()
                            if ReplyComment.objects.filter(
                                reply_commented_video=video,
                                comment_parent=comment,
                                creator=request.user,
                                date_created_without_time=today
                            ).count() < 10:
                                ReplyComment.objects.create(
                                    reply_commented_video=video,
                                    comment_parent=comment,
                                    creator=request.user,
                                    reply_comment_id=generate_id(32),
                                    comment_text=text
                                )
                                comment.replies += 1
                                comment.save()
                                video.comments += 1
                                video.save()
                                video.creator.all_comments += 1
                                video.creator.save()
                                return Response({
                                    'data': {},
                                    'message': 'Reply to comment added ⛄️',
                                    'status': 'ok'
                                }, status=status.HTTP_200_OK)
                            else:
                                return Response({
                                    'data': {},
                                    'message': 'You have exceeded the replies limit for one video today 😥',
                                    'status': 'err'
                                }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                'data': {},
                                'message': 'Comment cannot contain spaces or be empty 🙉',
                                'status': 'err'
                            }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            'data': {},
                            'message': 'Maximum text length 500 characters 🥴',
                            'status': 'err'
                        }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'data': {},
                        'message': 'Comment not found',
                        'status': 'err'
                    }, status=status.HTTP_200_OK)
            else:
                return Response({'data': {}, 'message': 'Video not found', 'status': 'err'}, status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# like reply comment
class LikeReplyCommentApi(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'reply_comment_id' in request.data:
            comment = ReplyComment.objects.filter(
                reply_comment_id=request.data.get('reply_comment_id'))
            if comment.count() > 0:
                comment = comment[0]
                like = ReplyCommentLike.objects.filter(
                    liked_reply_comment=comment,
                    liked_user=request.user
                )
                dislike = ReplyCommentDislike.objects.filter(
                    disliked_reply_comment=comment,
                    disliked_user=request.user
                )

                if like.count() == 0 and dislike.count() == 0:
                    like = ReplyCommentLike.objects.create(
                        liked_reply_comment=comment,
                        liked_user=request.user
                    )
                    if like:
                        comment.likes += 1
                        comment.save()
                    return Response({
                        'data': {
                            'like': 1,
                            'dislike': 0,
                            'stats': {
                                'likes': brief_likes_format(comment.likes),
                                'dislikes': brief_likes_format(comment.dislikes)
                            }
                        },
                        'message': '',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                elif like.count() == 1 and dislike.count() == 0:
                    like[0].delete()
                    comment.likes -= 1
                    comment.save()
                    return Response({
                        'data': {
                            'like': 0,
                            'dislike': 0,
                            'stats': {
                                'likes': brief_likes_format(comment.likes),
                                'dislikes': brief_likes_format(comment.dislikes)
                            }
                        },
                        'message': '',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                elif like.count() == 0 and dislike.count() == 1:
                    comment.dislikes -= 1
                    comment.likes += 1
                    comment.save()
                    dislike[0].delete()
                    like = ReplyCommentLike.objects.create(
                        liked_reply_comment=comment,
                        liked_user=request.user
                    )
                    return Response({
                        'data': {
                            'like': 1,
                            'dislike': 0,
                            'stats': {
                                'likes': brief_likes_format(comment.likes),
                                'dislikes': brief_likes_format(comment.dislikes)
                            }
                        },
                        'message': '',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                else:
                    return Response({'data': {}, 'status': 'err'}, status=status.HTTP_200_OK)
            else:
                return Response({
                    'data': {},
                    'message': 'Reply comment not found',
                    'status': 'err'
                }, status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# dislike comment
class DislikeReplyCommentApi(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'reply_comment_id' in request.data:
            comment = ReplyComment.objects.filter(
                reply_comment_id=request.data.get('reply_comment_id'))
            if comment.count() > 0:
                comment = comment[0]
                like = ReplyCommentLike.objects.filter(
                    liked_reply_comment=comment,
                    liked_user=request.user
                )
                dislike = ReplyCommentDislike.objects.filter(
                    disliked_reply_comment=comment,
                    disliked_user=request.user
                )

                if like.count() == 0 and dislike.count() == 0:
                    dislike = ReplyCommentDislike.objects.create(
                        disliked_reply_comment=comment,
                        disliked_user=request.user
                    )
                    if dislike:
                        comment.dislikes += 1
                        comment.save()
                    return Response({
                        'data': {
                            'like': 0,
                            'dislike': 1,
                            'stats': {
                                'likes': brief_likes_format(comment.likes),
                                'dislikes': brief_likes_format(comment.dislikes)
                            }
                        },
                        'message': '',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                elif dislike.count() == 1 and like.count() == 0:
                    dislike[0].delete()
                    comment.dislikes -= 1
                    comment.save()
                    return Response({
                        'data': {
                            'like': 0,
                            'dislike': 0,
                            'stats': {
                                'likes': brief_likes_format(comment.likes),
                                'dislikes': brief_likes_format(comment.dislikes)
                            }
                        },
                        'message': '',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                elif dislike.count() == 0 and like.count() == 1:
                    comment.likes -= 1
                    comment.dislikes += 1
                    comment.save()
                    like[0].delete()
                    dislike = ReplyCommentDislike.objects.create(
                        disliked_reply_comment=comment,
                        disliked_user=request.user
                    )
                    return Response({
                        'data': {
                            'like': 0,
                            'dislike': 1,
                            'stats': {
                                'likes': brief_likes_format(comment.likes),
                                'dislikes': brief_likes_format(comment.dislikes)}},
                        'message': '',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                else:
                    return Response({'data': {}, 'status': 'err'}, status=status.HTTP_200_OK)
            else:
                return Response({
                    'data': {},
                    'message': 'Reply comment not found',
                    'status': 'err'
                }, status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# delete comment
class DeleteReplyCommentApi(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'reply_comment_id' in request.data:
            comment = ReplyComment.objects.filter(
                reply_comment_id=request.data.get('reply_comment_id'))
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
                    return Response({
                        'data': {},
                        'message': 'Comment has been deleted 🧸',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'data': {},
                        'message': 'You are not authorized to delete this comment because you are not its creator',
                        'status': 'err'
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'data': {},
                    'message': 'Comment not found', 'status': 'err'
                }, status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# get video stats
class VideoStatsApi(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'video_id' in request.data:
            video = Video.objects.filter(video_id=request.data.get('video_id'))
            if video.count() > 0:
                video = video[0]
                if request.user == video.creator:
                    views_stats = {}
                    comments_stats = {}
                    likes_stats = {}
                    dislikes_stats = {}

                    today = date.today()
                    for i in range(10):
                        day = today - timedelta(days=i)
                        views = VideoViewModel.objects.filter(
                            watched_video=video,
                            date_created_without_time__gt=day
                        )
                        comments = Comment.objects.filter(
                            commented_video=video,
                            date_created_without_time__gt=(day)
                        )
                        reply_comments = ReplyComment.objects.filter(
                            reply_commented_video=video,
                            date_created_without_time__gt=(day)
                        )
                        likes = Like.objects.filter(
                            liked_video=video,
                            date_created_without_time__gt=(day)
                        )
                        dislikes = Dislike.objects.filter(
                            disliked_video=video,
                            date_created_without_time__gt=(day)
                        )

                        if day >= video.date_created_without_time:
                            views_stats[str(day)] = video.views - views.count()
                            comments_stats[
                                str(day)
                            ] = video.comments - (comments.count() + reply_comments.count())
                            likes_stats[str(day)] = video.likes - likes.count()
                            dislikes_stats[
                                str(day)
                            ] = video.dislikes - dislikes.count()

                    return Response({
                        'data': {
                            'views': views_stats,
                            'comments': comments_stats,
                            'likes': likes_stats,
                            'dislikes': dislikes_stats
                        },
                        'message': '',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'data': {},
                        'message': 'You do not have permission to view statistics because you are not its author',
                        'status': 'err'
                    }, status=status.HTTP_200_OK)
            else:
                return Response({'data': {}, 'message': 'Video not found', 'status': 'err'}, status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# get article stats
class ArticleStatsApi(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'article_id' in request.data:
            article = Article.objects.filter(
                article_id=request.data.get('article_id'))
            if article.count() > 0:
                article = article[0]
                if request.user == article.creator:
                    likes_stats = {}
                    dislikes_stats = {}

                    today = date.today()
                    for i in range(10):
                        day = today - timedelta(days=i)
                        likes = ArticleLike.objects.filter(
                            liked_article=article,
                            date_created_without_time__gt=(day)
                        )
                        dislikes = ArticleDislike.objects.filter(
                            disliked_article=article,
                            date_created_without_time__gt=(day)
                        )

                        if day >= article.date_created_without_time:
                            likes_stats[
                                str(day)
                            ] = article.likes - likes.count()
                            dislikes_stats[
                                str(day)
                            ] = article.dislikes - dislikes.count()

                    return Response({
                        'data': {
                            'likes': likes_stats,
                            'dislikes': dislikes_stats
                        },
                        'message': '',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'data': {},
                        'message': 'You do not have permission to view statistics because you are not its author',
                        'status': 'err'
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'data': {},
                    'message': 'Article not found',
                    'status': 'err'
                }, status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# get track stats
class TrackStatsApi(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'track_id' in request.data:
            track = Track.objects.filter(track_id=request.data.get('track_id'))
            if track.count() > 0:
                track = track[0]
                if request.user == track.creator:
                    auditions_stats = {}

                    today = date.today()
                    for i in range(10):
                        day = today - timedelta(days=i)
                        auditions = TrackListenModel.objects.filter(
                            listened_track=track,
                            date_created_without_time__gt=(day)
                        )

                        if day >= track.date_created_without_time:
                            auditions_stats[
                                str(day)
                            ] = track.auditions - auditions.count()

                    return Response({
                        'data': {
                            'auditions': auditions_stats
                        },
                        'message': '',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'data': {},
                        'message': 'You do not have permission to view statistics because you are not its author',
                        'status': 'err'
                    }, status=status.HTTP_200_OK)
            else:
                return Response({'data': {}, 'message': 'Track not found', 'status': 'err'}, status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# like film
class LikeFilmApi(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'film_id' in request.data:
            film = Film.objects.filter(film_id=request.data.get('film_id'))
            if film.count() > 0:
                film = film[0]
                like = FilmLike.objects.filter(
                    liked_film=film, liked_user=request.user)
                dislike = FilmDislike.objects.filter(
                    disliked_film=film,
                    disliked_user=request.user
                )

                if like.count() == 0 and dislike.count() == 0:
                    like = FilmLike.objects.create(
                        liked_film=film,
                        liked_user=request.user
                    )
                    if like:
                        film.likes += 1
                        film.save()
                    return Response({
                        'data': {
                            'like': 1,
                            'dislike': 0,
                            'stats': {
                                'likes': brief_likes_format(film.likes),
                                'dislikes': brief_likes_format(film.dislikes)
                            }
                        },
                        'message': 'Your liked this film 🧡',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                elif like.count() == 1 and dislike.count() == 0:
                    like[0].delete()
                    film.likes -= 1
                    film.save()
                    return Response({
                        'data': {
                            'like': 0,
                            'dislike': 0,
                            'stats': {
                                'likes': brief_likes_format(film.likes),
                                'dislikes': brief_likes_format(film.dislikes)
                            }
                        },
                        'message': 'Like removed 🧸',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                elif like.count() == 0 and dislike.count() == 1:
                    film.dislikes -= 1
                    film.likes += 1
                    film.save()
                    dislike[0].delete()
                    like = FilmLike.objects.create(
                        liked_film=film,
                        liked_user=request.user
                    )
                    return Response({
                        'data': {
                            'like': 1,
                            'dislike': 0,
                            'stats': {
                                'likes': brief_likes_format(film.likes),
                                'dislikes': brief_likes_format(film.dislikes)
                            }
                        },
                        'message': 'Your liked this film 🧡',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                else:
                    return Response({'data': {}, 'status': 'err'}, status=status.HTTP_200_OK)
            else:
                return Response({'data': {}, 'message': 'Film not found', 'status': 'err'}, status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# dislike film
class DislikeFilmApi(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'film_id' in request.data:
            film = Film.objects.filter(film_id=request.data.get('film_id'))
            if film.count() > 0:
                film = film[0]
                like = FilmLike.objects.filter(
                    liked_film=film,
                    liked_user=request.user
                )
                dislike = FilmDislike.objects.filter(
                    disliked_film=film,
                    disliked_user=request.user
                )

                if like.count() == 0 and dislike.count() == 0:
                    dislike = FilmDislike.objects.create(
                        disliked_film=film,
                        disliked_user=request.user
                    )
                    if dislike:
                        film.dislikes += 1
                        film.save()
                    return Response({
                        'data': {
                            'like': 0,
                            'dislike': 1,
                            'stats': {
                                'likes': brief_likes_format(film.likes),
                                'dislikes': brief_likes_format(film.dislikes)
                            }
                        },
                        'message': 'Your disliked this film 💔',
                        'status': 'ok'}, status=status.HTTP_200_OK)

                elif dislike.count() == 1 and like.count() == 0:
                    dislike[0].delete()
                    film.dislikes -= 1
                    film.save()
                    return Response({
                        'data': {
                            'like': 0,
                            'dislike': 0,
                            'stats': {
                                'likes': brief_likes_format(film.likes),
                                'dislikes': brief_likes_format(film.dislikes)
                            }
                        },
                        'message': 'Dislike removed 🥶',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                elif dislike.count() == 0 and like.count() == 1:
                    film.likes -= 1
                    film.dislikes += 1
                    film.save()
                    like[0].delete()
                    dislike = FilmDislike.objects.create(
                        disliked_film=film,
                        disliked_user=request.user
                    )
                    return Response({
                        'data': {
                            'like': 0,
                            'dislike': 1,
                            'stats': {
                                'likes': brief_likes_format(film.likes),
                                'dislikes': brief_likes_format(film.dislikes)
                            }
                        },
                        'message': 'Your disliked this film 💔',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                else:
                    return Response({'data': {}, 'status': 'err'}, status=status.HTTP_200_OK)
            else:
                return Response({'data': {}, 'message': 'Film not found', 'status': 'err'}, status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# buy film
class BuyFilmApi(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'film_id' in request.data:
            film = Film.objects.filter(film_id=request.data.get('film_id'))
            if film.count() > 0:
                film = film[0]
                if BuyFilm.objects.filter(buy_user=request.user, buy_film=film).count() == 0:
                    BuyFilm.objects.create(
                        buy_user=request.user,
                        buy_film=film
                    )

                    if request.user.telegram:
                        now = datetime.now()
                        date = now.strftime('%d-%m-%Y %H:%M:%S')
                        send_notification.delay(
                            f'You purchased the movie: {film.title} 🥳\nDate: {date}\nPrice: USD {film.price}\n\n{DOMEN}film/{film.film_id}/',
                            request.user.telegram
                        )

                    messages.success(
                        self.request, f'You purchased the movie: <b>{film.title}</b> 🥳')
                    return Response({'data': {}, 'status': 'ok'}, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'data': {},
                        'message': 'You have already bought this film',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)
            else:
                return Response({'data': {}, 'message': 'Film not found', 'status': 'err'}, status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# delete article
class DeleteArticleApi(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'article_id' in request.data:
            article_id = request.data.get('article_id')
            article = Article.objects.filter(article_id=article_id)
            if article.count() > 0:
                if article[0].creator == request.user:
                    article[0].delete()
                    messages.success(
                        request, f'Article successfully deleted! 🩸')
                    return Response({
                        'data': {
                            'user_id': request.user.user_id
                        },
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'data': {},
                        'message': 'You are not authorized to delete this article because you are not its creator',
                        'status': 'err'
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'data': {},
                    'message': 'Article not found',
                    'status': 'err'
                }, status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# like article
class LikeArticleApi(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'article_id' in request.data:
            article = Article.objects.filter(
                article_id=request.data.get('article_id'))
            if article.count() > 0:
                article = article[0]
                like = ArticleLike.objects.filter(
                    liked_article=article,
                    liked_user=request.user
                )
                dislike = ArticleDislike.objects.filter(
                    disliked_article=article,
                    disliked_user=request.user
                )

                if like.count() == 0 and dislike.count() == 0:
                    like = ArticleLike.objects.create(
                        liked_article=article,
                        liked_user=request.user
                    )
                    if like:
                        article.likes += 1
                        article.save()
                        article.creator.all_posts_likes += 1
                        article.creator.save()
                    return Response({
                        'data': {
                            'like': 1,
                            'dislike': 0,
                            'stats': {
                                'likes': brief_likes_format(article.likes),
                                'dislikes': brief_likes_format(article.dislikes)
                            }
                        },
                        'message': 'You like this article 👍',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                elif like.count() == 1 and dislike.count() == 0:
                    like[0].delete()
                    article.likes -= 1
                    article.save()
                    article.creator.all_posts_likes -= 1
                    article.creator.save()
                    return Response({
                        'data': {
                            'like': 0,
                            'dislike': 0,
                            'stats': {
                                'likes': brief_likes_format(article.likes),
                                'dislikes': brief_likes_format(article.dislikes)
                            }
                        },
                        'message': 'Like removed 👀',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                elif like.count() == 0 and dislike.count() == 1:
                    article.dislikes -= 1
                    article.likes += 1
                    article.save()

                    article.creator.all_posts_dislikes -= 1
                    article.creator.all_posts_likes += 1
                    article.creator.save()

                    dislike[0].delete()
                    like = ArticleLike.objects.create(
                        liked_article=article,
                        liked_user=request.user
                    )
                    return Response({
                        'data': {
                            'like': 1,
                            'dislike': 0,
                            'stats': {
                                'likes': brief_likes_format(article.likes),
                                'dislikes': brief_likes_format(article.dislikes)
                            }
                        },
                        'message': 'You like this article 👍',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                else:
                    return Response({'data': {}, 'status': 'err'}, status=status.HTTP_200_OK)
            else:
                return Response({
                    'data': {},
                    'message': 'Article not found',
                    'status': 'err'
                }, status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# dislike article
class DislikeArticleApi(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'article_id' in request.data:
            article = Article.objects.filter(
                article_id=request.data.get('article_id'))
            if article.count() > 0:
                article = article[0]
                like = ArticleLike.objects.filter(
                    liked_article=article,
                    liked_user=request.user
                )
                dislike = ArticleDislike.objects.filter(
                    disliked_article=article,
                    disliked_user=request.user
                )

                if like.count() == 0 and dislike.count() == 0:
                    dislike = ArticleDislike.objects.create(
                        disliked_article=article,
                        disliked_user=request.user
                    )
                    if dislike:
                        article.dislikes += 1
                        article.save()
                        article.creator.all_posts_dislikes += 1
                        article.creator.save()
                    return Response({
                        'data': {
                            'like': 0,
                            'dislike': 1,
                            'stats': {
                                'likes': brief_likes_format(article.likes),
                                'dislikes': brief_likes_format(article.dislikes)
                            }
                        },
                        'message': 'You dislike this article 👎',
                        'status': 'ok'}, status=status.HTTP_200_OK)

                elif dislike.count() == 1 and like.count() == 0:
                    dislike[0].delete()
                    article.dislikes -= 1
                    article.save()
                    article.creator.all_posts_dislikes -= 1
                    article.creator.save()
                    return Response({
                        'data': {
                            'like': 0,
                            'dislike': 0,
                            'stats': {
                                'likes': brief_likes_format(article.likes),
                                'dislikes': brief_likes_format(article.dislikes)
                            }
                        },
                        'message': 'Dislike removed 😎',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                elif dislike.count() == 0 and like.count() == 1:
                    article.likes -= 1
                    article.dislikes += 1
                    article.save()

                    article.creator.all_posts_likes -= 1
                    article.creator.all_posts_dislikes += 1
                    article.creator.save()

                    like[0].delete()
                    dislike = ArticleDislike.objects.create(
                        disliked_article=article,
                        disliked_user=request.user
                    )
                    return Response({
                        'data': {
                            'like': 0,
                            'dislike': 1,
                            'stats': {
                                'likes': brief_likes_format(article.likes),
                                'dislikes': brief_likes_format(article.dislikes)
                            }
                        },
                        'message': 'You dislike this article 👎',
                        'status': 'ok'
                    }, status=status.HTTP_200_OK)

                else:
                    return Response({'data': {}, 'status': 'err'}, status=status.HTTP_200_OK)
            else:
                return Response({
                    'data': {},
                    'message': 'Article not found',
                    'status': 'err'
                },  status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# create api token
class CreateTokenApi(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        token = Token.objects.filter(user=request.user)
        if token:
            token[0].delete()
        token = Token.objects.create(user=request.user)
        print(token.key)
        return Response({
            'data': {
                'token': token.key
            },
            'message': 'Token successfully updated 🔑',
            'status': 'ok'
        }, status=status.HTTP_200_OK)


# get user info
class UserInfoApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user_data = {}
        user_data['user_id'] = user.user_id
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['date_created'] = user.date_created

        user_data['media'] = {
            'avatar': str(user.avatar),
            'banner': str(user.banner)
        }

        details = {}
        details['description'] = user.description
        details['contact_email'] = user.contact_email
        details['location'] = user.location
        user_data['details'] = details

        links = {}
        links['vk_link'] = user.vk_link
        links['instagram_link'] = user.instagram_link
        links['facebook_link'] = user.facebook_link
        links['reddit_link'] = user.reddit_link
        links['telegram_link'] = user.telegram_link
        links['twitter_link'] = user.twitter_link
        links['website_link'] = user.website_link
        user_data['links'] = links

        user_data['telegram'] = {'telegram': user.telegram}

        user_data['yoomoney'] = {
            'wallet': user.wallet,
            'donat_text': user.donat_text
        }

        stats = {}
        stats['videos'] = {
            'videos': Video.objects.filter(creator=user).count(),
            'views': user.all_views,
            'comments': user.all_comments,
            'likes': user.all_likes,
            'dislikes': user.all_dislikes
        }

        stats['tracks'] = {
            'tracks': Track.objects.filter(creator=user).count(),
            'auditions': user.all_auditions
        }

        stats['posts'] = {
            'posts': Article.objects.filter(creator=user).count(),
            'likes': user.all_posts_likes,
            'dislikes': user.all_posts_dislikes
        }

        stats['subscribers'] = user.all_subscribers
        stats['notifications'] = user.all_notifications
        user_data['stats'] = stats

        return Response({'data': {'user': user_data}, 'status': 'ok'}, status=status.HTTP_200_OK)


# get tranding videos
class TrendingApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        tranding_time = datetime.utcnow() - timedelta(days=2)
        videos = {}
        for i in range(100):
            try:
                video = Video.objects.filter(
                    ~Q(coefficient=0.0),
                    date_created__gt=tranding_time
                ).order_by('-coefficient')[i]
                video_info = {}
                video_info['title'] = video.title
                video_info['description'] = video.description
                video_info['date_created'] = video.date_created
                video_info['date_created_without_time'] = video.date_created_without_time
                video_info['creator'] = {
                    'user_id': video.creator.user_id,
                    'username': video.creator.username
                }
                video_info['media'] = {
                    'video': str(video.video),
                    'banner': str(video.video_banner)
                }
                video_info['stats'] = {
                    'coefficient': video.coefficient,
                    'views': video.views,
                    'comments': video.comments,
                    'likes': video.likes,
                    'dislikes': video.dislikes
                }
                videos[video.video_id] = video_info
            except:
                break

        return Response({'data': {'videos': videos}, 'status': 'ok'}, status=status.HTTP_200_OK)


# get site stats
class SiteStatsApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = {}
        data['users'] = CustomUser.objects.all().count()
        data['subscriptions'] = Subscribe.objects.all().count()
        data['notifications'] = Notification.objects.all().count()
        data['videos'] = {
            'videos': Video.objects.all().count(),
            'views': VideoViewModel.objects.all().count(),
            'likes': Like.objects.all().count(),
            'dislikes': Dislike.objects.all().count(),
            'comments': {
                'total': Comment.objects.all().count() + ReplyComment.objects.all().count(),
                'comments': {
                    'comments': Comment.objects.all().count(),
                    'likes': CommentLike.objects.all().count(),
                    'dislikes': CommentDislike.objects.all().count(),
                },
                'replies': {
                    'comments': ReplyComment.objects.all().count(),
                    'likes': ReplyCommentLike.objects.all().count(),
                    'dislikes': ReplyCommentDislike.objects.all().count(),
                }
            },
            'saves': SavedVideo.objects.all().count()
        }
        data['posts'] = {
            'posts': Article.objects.all().count(),
            'likes': ArticleLike.objects.all().count(),
            'dislikes': ArticleDislike.objects.all().count()
        }
        data['tracks'] = {
            'tracks': Track.objects.all().count(),
            'auditions': TrackListenModel.objects.all().count()
        }
        data['films'] = {
            'films': Film.objects.all().count(),
            'purchases': BuyFilm.objects.all().count(),
            'likes': FilmLike.objects.all().count(),
            'dislikes': FilmDislike.objects.all().count(),
            'actors': Actor.objects.all().count(),
            'producers': Producer.objects.all().count(),
            'writers': Writer.objects.all().count(),
            'genres': Genre.objects.all().count(),
        }

        return Response({'data': data, 'message': '', 'status': 'ok'}, status=status.HTTP_200_OK)


# get user videos
class VideosApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_videos = Video.objects.filter(creator=request.user)
        videos = {}
        if user_videos:
            message = ''
            for video in user_videos:
                try:
                    video_info = {}
                    video_info['title'] = video.title
                    video_info['description'] = video.description
                    video_info['date_created'] = video.date_created
                    video_info['date_created_without_time'] = video.date_created_without_time
                    video_info['media'] = {
                        'video': str(video.video),
                        'banner': str(video.video_banner)
                    }
                    video_info['stats'] = {
                        'coefficient': video.coefficient,
                        'views': video.views,
                        'comments': video.comments,
                        'likes': video.likes,
                        'dislikes': video.dislikes
                    }
                    videos[video.video_id] = video_info
                except:
                    break
        else:
            return Response({
                'data': {},
                'message': 'Videos not found',
                'status': 'err'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'data': {
                'videos': videos
            },
            'message': message,
            'status': 'ok'
        }, status=status.HTTP_200_OK)


# get user liked videos
class LikedVideosApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        liked_videos = Like.objects.filter(liked_user=request.user)
        videos = {}
        if liked_videos:
            message = ''
            for video in liked_videos:
                try:
                    video_info = {}
                    video_info['title'] = video.liked_video.title
                    video_info['description'] = video.liked_video.description
                    video_info['date_created'] = video.liked_video.date_created
                    video_info['date_created_without_time'] = video.liked_video.date_created_without_time
                    video_info['creator'] = {
                        'user_id': video.liked_user.user_id,
                        'username': video.liked_user.username
                    }
                    video_info['media'] = {
                        'video': str(video.liked_video.video),
                        'banner': str(video.liked_video.video_banner)
                    }
                    video_info['stats'] = {
                        'coefficient': video.liked_video.coefficient,
                        'views': video.liked_video.views,
                        'comments': video.liked_video.comments,
                        'likes': video.liked_video.likes,
                        'dislikes': video.liked_video.dislikes
                    }
                    videos[video.liked_video.video_id] = video_info
                except:
                    break
        else:
            return Response({
                'data': {
                    'videos': ''
                },
                'message': 'Liked videos not found',
                'status': 'err'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data': {'videos': videos}, 'message': message, 'status': 'ok'}, status=status.HTTP_200_OK)


# get user disliked videos
class DislikedVideosApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        disliked_videos = Dislike.objects.filter(disliked_user=request.user)
        videos = {}
        if disliked_videos:
            message = ''
            for video in disliked_videos:
                try:
                    video_info = {}
                    video_info['title'] = video.disliked_video.title
                    video_info['description'] = video.disliked_video.description
                    video_info['date_created'] = video.disliked_video.date_created
                    video_info['date_created_without_time'] = video.disliked_video.date_created_without_time
                    video_info['creator'] = {
                        'user_id': video.disliked_user.user_id,
                        'username': video.disliked_user.username
                    }
                    video_info['media'] = {
                        'video': str(video.disliked_video.video),
                        'banner': str(video.disliked_video.video_banner)
                    }
                    video_info['stats'] = {
                        'coefficient': video.disliked_video.coefficient,
                        'views': video.disliked_video.views,
                        'comments': video.disliked_video.comments,
                        'likes': video.disliked_video.likes,
                        'dislikes': video.disliked_video.dislikes
                    }
                    videos[video.disliked_video.video_id] = video_info
                except:
                    break
        else:
            return Response({
                'data': {
                    'videos': ''
                },
                'message': 'Disliked videos not found',
                'status': 'err'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data': {'videos': videos}, 'message': message, 'status': 'ok'}, status=status.HTTP_200_OK)


# get user saved videos
class SavedVideosApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        saved_videos = SavedVideo.objects.filter(saved_user=request.user)
        videos = {}
        if saved_videos:
            message = ''
            for video in saved_videos:
                try:
                    video_info = {}
                    video_info['title'] = video.saved_video.title
                    video_info['description'] = video.saved_video.description
                    video_info['date_created'] = video.saved_video.date_created
                    video_info['date_created_without_time'] = video.saved_video.date_created_without_time
                    video_info['creator'] = {
                        'user_id': video.saved_user.user_id,
                        'username': video.saved_user.username
                    }
                    video_info['media'] = {
                        'video': str(video.saved_video.video),
                        'banner': str(video.saved_video.video_banner)
                    }
                    video_info['stats'] = {
                        'coefficient': video.saved_video.coefficient,
                        'views': video.saved_video.views,
                        'comments': video.saved_video.comments,
                        'likes': video.saved_video.likes,
                        'dislikes': video.saved_video.dislikes
                    }
                    videos[video.saved_video.video_id] = video_info
                except:
                    break
        else:
            return Response({
                'data': {
                    'videos': ''
                },
                'message': 'Saved videos not found',
                'status': 'err'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data': {'videos': videos}, 'message': message, 'status': 'ok'}, status=status.HTTP_200_OK)


# video api
class VideoApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        video = Video.objects.filter(video_id=self.kwargs['pk'])
        video_info = {}
        if video:
            message = ''
            video = video[0]
            video_info = {}
            video_info['id'] = video.video_id
            video_info['title'] = video.title
            video_info['description'] = video.description
            video_info['date_created'] = video.date_created
            video_info['date_created_without_time'] = video.date_created_without_time
            video_info['creator'] = {
                'user_id': video.creator.user_id,
                'username': video.creator.username
            }
            video_info['media'] = {
                'video': str(video.video),
                'banner': str(video.video_banner)
            }
            video_info['stats'] = {
                'coefficient': video.coefficient,
                'views': video.views,
                'comments': video.comments,
                'likes': video.likes,
                'dislikes': video.dislikes
            }
        else:
            return Response({
                'data': {},
                'message': 'Video not found',
                'status': 'err'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data': {'video': video_info}, 'message': message, 'status': 'ok'}, status=status.HTTP_200_OK)


# download video
class DownloadVideoFile(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        video = Video.objects.filter(video_id=self.kwargs['pk'])
        if video:
            path = video[0].video.path
            response = FileResponse(open(path, 'rb'))
            return response
        else:
            return Response({'data': {}, 'message': 'Video not found', 'status': 'ok'}, status=status.HTTP_200_OK)


# download video banner
class DownloadBannerFile(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        video = Video.objects.filter(video_id=self.kwargs['pk'])
        if video:
            path = video[0].video_banner.path
            response = FileResponse(open(path, 'rb'))
            return response
        else:
            return Response({'data': {}, 'message': 'Video not found', 'status': 'ok'}, status=status.HTTP_200_OK)


# upload video
class UploadVideoApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        if 'video' in request.data and 'banner' in request.data and 'title' in request.data and 'description' in request.data:
            video = request.data.get('video')
            if video.size > MAX_VIDEO_SIZE:
                return Response({
                    'data': {},
                    'message': 'The size of the video should not exceed 200 MB.',
                    'status': 'OK'
                })

            banner = request.data.get('banner')
            if banner.size > MAX_IMAGE_SIZE:
                return Response({
                    'data': {},
                    'message': 'The size of the photo should not exceed 7.5 MB.',
                    'status': 'OK'
                })

            # maximum 5 videos per day (one user)
            today = date.today()
            if Video.objects.filter(creator=request.user, date_created_without_time=today).count() < 5:
                data = {
                    'creator': self.request.user.id,
                    'title': request.data.get('title'),
                    'description': request.data.get('description'),
                    'video': video,
                    'video_banner': banner
                }
                file_serializer = VideoSerializer(data=data)
                if file_serializer.is_valid(raise_exception=True):
                    queryset = file_serializer.save()
                    message = 'Videos uploaded successfully'
                else:
                    message = 'An error occured while uploading video'

                return Response({
                    'data': {
                        'id': queryset.video_id
                    },
                    'message': message,
                    'status': 'OK'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'data': {},
                    'message': 'You have exceeded the videos limit for one day today 😥',
                    'status': 'err'
                }, status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# get films
class FilmsApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        site_films = Film.objects.all()
        films = {}
        if site_films:
            for film in site_films:
                try:
                    film_info = {}
                    film_info['title'] = film.title
                    film_info['price'] = film.price
                    film_info['running_time'] = film.running_time
                    film_info['rating'] = film.rating
                    film_info['release_date'] = film.release_date
                    film_info['release_year'] = film.release_year
                    film_info['main_genre'] = str(film.main_genre)
                    film_info['date_created'] = film.date_created
                    film_info['media'] = {
                        'trailer': str(film.trailer),
                        'poster': str(film.film_poster),
                        'banner': str(film.film_banner)
                    }
                    film_info['stats'] = {
                        'likes': film.likes,
                        'dislikes': film.dislikes,
                        'purchases': BuyFilm.objects.filter(buy_film=film).count()
                    }

                    details = {}

                    actors = {}
                    for i in FilmActor.objects.filter(actor_film=film):
                        actors[i.actor_id] = {
                            'name': i.actor.name,
                            'gender': i.actor.gender,
                            'photo': str(i.actor.photo)
                        }

                    producers = {}
                    for i in FilmProducer.objects.filter(producer_film=film):
                        producers[i.producer_id] = {
                            'name': i.producer.name,
                            'gender': i.producer.gender,
                            'photo': str(i.producer.photo)
                        }

                    writers = {}
                    for i in FilmWriter.objects.filter(writer_film=film):
                        writers[i.writer_id] = {
                            'name': i.writer.name,
                            'gender': i.writer.gender,
                            'photo': str(i.writer.photo)
                        }

                    genres = []
                    for i in FilmGenre.objects.filter(genre_film=film):
                        genres.append(i.genre.name)

                    details['actors'] = actors
                    details['producers'] = producers
                    details['writers'] = writers
                    details['genres'] = genres

                    film_info['details'] = details
                    films[film.film_id] = film_info
                except:
                    break
        else:
            return Response({
                'data': {},
                'message': 'Films not found',
                'status': 'err'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data': {'films': films}, 'message': '', 'status': 'ok'}, status=status.HTTP_200_OK)


# films api
class FilmApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        film = Film.objects.filter(film_id=self.kwargs['pk'])
        film_info = {}
        if film:
            film = film[0]
            film_info = {}
            film_info['id'] = film.film_id
            film_info['title'] = film.title
            film_info['price'] = film.price
            film_info['running_time'] = film.running_time
            film_info['rating'] = film.rating
            film_info['release_date'] = film.release_date
            film_info['release_year'] = film.release_year
            film_info['main_genre'] = str(film.main_genre)
            film_info['date_created'] = film.date_created
            film_info['media'] = {
                'trailer': str(film.trailer),
                'poster': str(film.film_poster),
                'banner': str(film.film_banner)
            }
            film_info['stats'] = {
                'likes': film.likes,
                'dislikes': film.dislikes,
                'purchases': BuyFilm.objects.filter(buy_film=film).count()
            }

            details = {}

            actors = {}
            for i in FilmActor.objects.filter(actor_film=film):
                actors[i.actor_id] = {
                    'name': i.actor.name,
                    'gender': i.actor.gender,
                    'photo': str(i.actor.photo)
                }

            producers = {}
            for i in FilmProducer.objects.filter(producer_film=film):
                producers[i.producer_id] = {
                    'name': i.producer.name,
                    'gender': i.producer.gender,
                    'photo': str(i.producer.photo)
                }

            writers = {}
            for i in FilmWriter.objects.filter(writer_film=film):
                writers[i.writer_id] = {
                    'name': i.writer.name,
                    'gender': i.writer.gender,
                    'photo': str(i.writer.photo)
                }

            genres = []
            for i in FilmGenre.objects.filter(genre_film=film):
                genres.append(i.genre.name)

            details['actors'] = actors
            details['producers'] = producers
            details['writers'] = writers
            details['genres'] = genres

            film_info['details'] = details
        else:
            return Response({
                'data': {},
                'message': 'Film not found',
                'status': 'err'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data': {'film': film_info}, 'message': '', 'status': 'ok'}, status=status.HTTP_200_OK)


# liked films
class LikedFilmsApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        liked_films = FilmLike.objects.filter(liked_user=request.user)
        films = {}
        if liked_films:
            for film in liked_films:
                film = film.liked_film

                film_info = {}
                film_info['title'] = film.title
                film_info['price'] = film.price
                film_info['running_time'] = film.running_time
                film_info['rating'] = film.rating
                film_info['release_date'] = film.release_date
                film_info['release_year'] = film.release_year
                film_info['main_genre'] = str(film.main_genre)
                film_info['date_created'] = film.date_created
                film_info['media'] = {
                    'trailer': str(film.trailer),
                    'poster': str(film.film_poster),
                    'banner': str(film.film_banner)
                }
                film_info['stats'] = {
                    'likes': film.likes,
                    'dislikes': film.dislikes,
                    'purchases': BuyFilm.objects.filter(buy_film=film).count()
                }

                details = {}

                actors = {}
                for i in FilmActor.objects.filter(actor_film=film):
                    actors[i.actor_id] = {
                        'name': i.actor.name,
                        'gender': i.actor.gender,
                        'photo': str(i.actor.photo)
                    }

                producers = {}
                for i in FilmProducer.objects.filter(producer_film=film):
                    producers[i.producer_id] = {
                        'name': i.producer.name,
                        'gender': i.producer.gender,
                        'photo': str(i.producer.photo)
                    }

                writers = {}
                for i in FilmWriter.objects.filter(writer_film=film):
                    writers[i.writer_id] = {
                        'name': i.writer.name,
                        'gender': i.writer.gender,
                        'photo': str(i.writer.photo)
                    }

                genres = []
                for i in FilmGenre.objects.filter(genre_film=film):
                    genres.append(i.genre.name)

                details['actors'] = actors
                details['producers'] = producers
                details['writers'] = writers
                details['genres'] = genres

                film_info['details'] = details
                films[film.film_id] = film_info
        else:
            return Response({
                'data': {},
                'message': 'Liked films not found',
                'status': 'err'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data': {'films': films}, 'message': '', 'status': 'ok'}, status=status.HTTP_200_OK)


# disliked films
class DislikedFilmsApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        disliked_films = FilmDislike.objects.filter(disliked_user=request.user)
        films = {}
        if disliked_films:
            for film in disliked_films:
                film = film.disliked_film

                film_info = {}
                film_info['title'] = film.title
                film_info['price'] = film.price
                film_info['running_time'] = film.running_time
                film_info['rating'] = film.rating
                film_info['release_date'] = film.release_date
                film_info['release_year'] = film.release_year
                film_info['main_genre'] = str(film.main_genre)
                film_info['date_created'] = film.date_created
                film_info['media'] = {
                    'trailer': str(film.trailer),
                    'poster': str(film.film_poster),
                    'banner': str(film.film_banner)
                }
                film_info['stats'] = {
                    'likes': film.likes,
                    'dislikes': film.dislikes,
                    'purchases': BuyFilm.objects.filter(buy_film=film).count()
                }

                details = {}
                actors = {}
                for i in FilmActor.objects.filter(actor_film=film):
                    actors[i.actor_id] = {
                        'name': i.actor.name,
                        'gender': i.actor.gender,
                        'photo': str(i.actor.photo)
                    }

                producers = {}
                for i in FilmProducer.objects.filter(producer_film=film):
                    producers[i.producer_id] = {
                        'name': i.producer.name,
                        'gender': i.producer.gender,
                        'photo': str(i.producer.photo)
                    }

                writers = {}
                for i in FilmWriter.objects.filter(writer_film=film):
                    writers[i.writer_id] = {
                        'name': i.writer.name,
                        'gender': i.writer.gender,
                        'photo': str(i.writer.photo)
                    }

                genres = []
                for i in FilmGenre.objects.filter(genre_film=film):
                    genres.append(i.genre.name)

                details['actors'] = actors
                details['producers'] = producers
                details['writers'] = writers
                details['genres'] = genres

                film_info['details'] = details
                films[film.film_id] = film_info
        else:
            return Response({
                'data': {},
                'message': 'Disliked films not found',
                'status': 'err'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data': {'films': films}, 'message': '', 'status': 'ok'}, status=status.HTTP_200_OK)


# purchased films
class PurchasedFilmsApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        durchased_films = BuyFilm.objects.filter(buy_user=request.user)
        films = {}
        if durchased_films:
            for film in durchased_films:
                film = film.buy_film

                film_info = {}
                film_info['title'] = film.title
                film_info['price'] = film.price
                film_info['running_time'] = film.running_time
                film_info['rating'] = film.rating
                film_info['release_date'] = film.release_date
                film_info['release_year'] = film.release_year
                film_info['main_genre'] = str(film.main_genre)
                film_info['date_created'] = film.date_created
                film_info['media'] = {
                    'trailer': str(film.trailer),
                    'poster': str(film.film_poster),
                    'banner': str(film.film_banner)
                }
                film_info['stats'] = {
                    'likes': film.likes,
                    'dislikes': film.dislikes,
                    'purchases': BuyFilm.objects.filter(buy_film=film).count()
                }

                details = {}

                actors = {}
                for i in FilmActor.objects.filter(actor_film=film):
                    actors[i.actor_id] = {
                        'name': i.actor.name,
                        'gender': i.actor.gender,
                        'photo': str(i.actor.photo)
                    }

                producers = {}
                for i in FilmProducer.objects.filter(producer_film=film):
                    producers[i.producer_id] = {
                        'name': i.producer.name,
                        'gender': i.producer.gender,
                        'photo': str(i.producer.photo)
                    }

                writers = {}
                for i in FilmWriter.objects.filter(writer_film=film):
                    writers[i.writer_id] = {
                        'name': i.writer.name,
                        'gender': i.writer.gender,
                        'photo': str(i.writer.photo)
                    }

                genres = []
                for i in FilmGenre.objects.filter(genre_film=film):
                    genres.append(i.genre.name)

                details['actors'] = actors
                details['producers'] = producers
                details['writers'] = writers
                details['genres'] = genres

                film_info['details'] = details
                films[film.film_id] = film_info
        else:
            return Response({
                'data': {},
                'message': 'Purchased films not found',
                'status': 'err'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data': {'films': films}, 'message': '', 'status': 'ok'}, status=status.HTTP_200_OK)


# download film banner
class DownloadFilmBannerFile(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        film = Film.objects.filter(film_id=self.kwargs['pk'])
        if film:
            path = film[0].film_banner.path
            response = FileResponse(open(path, 'rb'))
            return response
        else:
            return Response({
                'data': {},
                'message': 'Film not found',
                'status': 'err'
            }, status=status.HTTP_400_BAD_REQUEST)


# download film poster
class DownloadFilmPosterFile(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        film = Film.objects.filter(film_id=self.kwargs['pk'])
        if film:
            path = film[0].film_poster.path
            response = FileResponse(open(path, 'rb'))
            return response
        else:
            return Response({
                'data': {},
                'message': 'Film not found',
                'status': 'err'
            }, status=status.HTTP_400_BAD_REQUEST)


# download film trailer
class DownloadFilmTrailerFile(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        film = Film.objects.filter(film_id=self.kwargs['pk'])
        if film:
            path = film[0].trailer.path
            response = FileResponse(open(path, 'rb'))
            return response
        else:
            return Response({
                'data': {},
                'message': 'Film not found',
                'status': 'err'
            }, status=status.HTTP_400_BAD_REQUEST)


# download film
class DownloadFilmFile(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        film = Film.objects.filter(film_id=self.kwargs['pk'])
        if film:
            if BuyFilm.objects.filter(buy_user=request.user, buy_film=film[0]):
                path = film[0].film.path
                response = FileResponse(open(path, 'rb'))
                return response
            else:
                return Response({
                    'data': {},
                    'message': 'You did not buy this film',
                    'status': 'err'
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({
                'data': {},
                'message': 'Film not found',
                'status': 'err'
            }, status=status.HTTP_400_BAD_REQUEST)


# article api
class ArticleApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        article = Article.objects.filter(article_id=self.kwargs['pk'])
        article_info = {}
        if article:
            message = ''
            article = article[0]
            article_info = {}
            article_info['id'] = article.article_id
            article_info['title'] = article.text
            article_info['date_created'] = article.date_created
            article_info['date_created_without_time'] = article.date_created_without_time
            article_info['creator'] = {
                'user_id': article.creator.user_id,
                'username': article.creator.username
            }
            article_info['stats'] = {
                'likes': article.likes,
                'dislikes': article.dislikes
            }
        else:
            return Response({
                'data': {},
                'message': 'Article not found',
                'status': 'err'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'data': {
                'article': article_info
            },
            'message': message,
            'status': 'ok'
        }, status=status.HTTP_200_OK)


# create article
class CreateArticleApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'text' in request.data:
            text = request.data.get('text')
            if len(text) > 1000000:
                return Response({
                    'data': {},
                    'message': 'Maximum text length 1000000 characters.',
                    'status': 'err'
                }, status=status.HTTP_200_OK)

            # maximum 10 articles per day (one user)
            today = date.today()
            if Article.objects.filter(creator=request.user, date_created_without_time=today).count() < 10:
                data = {
                    'creator': self.request.user.id,
                    'text': request.data.get('text')
                }
                article_serializer = ArticleSerializer(data=data)
                if article_serializer.is_valid(raise_exception=True):
                    queryset = article_serializer.save()
                    message = 'Article created successfully'
                else:
                    message = 'An error occured while create article'

                return Response({
                    'data': {
                        'id': queryset.article_id
                    },
                    'message': message,
                    'status': 'OK'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'data': {},
                    'message': 'You have exceeded the articles limit for one day today 😥',
                    'status': 'err'
                }, status=status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'status': 'err'}, status=status.HTTP_400_BAD_REQUEST)


# get user tracks
class TracksApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_tracks = Track.objects.filter(creator=request.user)
        tracks = {}
        if user_tracks:
            message = ''
            for track in user_tracks:
                try:
                    track_info = {}
                    track_info['title'] = track.title
                    track_info['date_created'] = track.date_created
                    track_info['date_created_without_time'] = track.date_created_without_time
                    track_info['media'] = {'poster': str(track.track_poster)}
                    track_info['stats'] = {
                        'auditions': track.auditions
                    }
                    tracks[track.track_id] = track_info
                except:
                    break
        else:
            return Response({
                'data': {},
                'message': 'Tracks not found',
                'status': 'err'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'data': {
                'tracks': tracks
            },
            'message': message,
            'status': 'ok'
        }, status=status.HTTP_200_OK)
