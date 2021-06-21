from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime
from ..models import *
import re

register = template.Library()


# Time format
@register.filter(name='time_func')
@stringfilter
def time_func(arg):
    now = datetime.utcnow()
    time = now - datetime.strptime(arg, '%Y-%m-%d %H:%M:%S.%f+00:00')
    if time.seconds < 86400 and time.days == 0:
        if time.seconds == 1:
            return "1 second ago"

        elif time.seconds < 60:
            return f'{time.seconds} seconds ago'

        elif time.seconds < 120:
            return "1 minute ago"

        elif time.seconds < 3600:
            return f'{time.seconds // 60} minutes ago'

        elif time.seconds < 7200:
            return '1 hour ago'

        elif time.seconds < 86400:
            return f'{time.seconds // 3600} hours ago'

    if time.days < 730:
        if time.days < 2:
            return '1 day ago'

        elif time.days < 7:
            return f'{time.days} days ago'

        elif time.days < 14:
            return '1 week ago'

        elif time.days < 30:
            return f'{time.days // 7} weeks ago'

        elif time.days < 60:
            return '1 month ago'

        elif time.days < 365:
            return f'{time.days // 30} months ago'

        elif time.days < 730:
            return '1 year ago'

    else:
        return f'{time.days // 365} years ago'


# Date format
@register.filter(name='date_func')
@stringfilter
def date_func(arg):
    now = datetime.utcnow()
    date = datetime.strptime(arg, '%Y-%m-%d %H:%M:%S.%f+00:00')
    time = now - date

    if time.seconds < 86400 and time.days == 0:
        if time.seconds == 1:
            return "1 second ago"

        elif time.seconds < 60:
            return f'{time.seconds} seconds ago'

        elif time.seconds < 120:
            return "1 minute ago"

        elif time.seconds < 3600:
            return f'{time.seconds // 60} minutes ago'

        elif time.seconds < 7200:
            return '1 hour ago'

        elif time.seconds < 86400:
            return f'{time.seconds // 3600} hours ago'
    else:
        return date.strftime('%b %d, %Y')


# Views format
@register.filter(name='integer_format')
@stringfilter
def integer_format(arg):
    if int(arg) == 1:
        return '1'
    else:
        return '{:,}'.format(int(arg))


# Comments format
@register.filter(name='comments_format')
@stringfilter
def comments_format(arg):
    if int(arg) == 1:
        return '1 Comment'
    else:
        return '{:,}'.format(int(arg)) + ' Comments'


# string fixed
def str_fixed(f: float, arg=0, n=0, name=''):
    a, b = str(f).split('.')
    if name == 'views':
        if int(b) > 500 and arg < 1000000:
            return '{}.{}{}'.format(a, b[:n], '0' * (n - len(b)))

        elif int(b) > 500000 and arg < 1000000000:
            return '{}.{}{}'.format(a, b[:n], '0' * (n - len(b)))

        elif int(b) > 500000000 and arg < 1000000000000:
            return '{}.{}{}'.format(a, b[:n], '0' * (n - len(b)))

        else:
            return a

    else:
        if arg < 1000000:
            return '{}.{}{}'.format(a, b[:n], '0' * (n - len(b)))

        elif arg < 1000000000:
            return '{}.{}{}'.format(a, b[:n], '0' * (n - len(b)))

        elif arg < 1000000000000:
            return '{}.{}{}'.format(a, b[:n], '0' * (n - len(b)))

        else:
            return a


# Brief views format
@register.filter(name='brief_views_format')
@stringfilter
def brief_views_format(arg):
    if int(arg) < 1000000:
        if int(arg) == 1:
            return '1 view'

        elif int(arg) < 1000:
            return f'{arg} views'

        else:
            return f"{str_fixed(float(int(arg) / 1000), int(arg), 1, 'views')}K views"

    elif int(arg) < 1000000000:
        return f"{str_fixed(float(int(arg) / 1000000), int(arg), 1, 'views')}M views"

    elif int(arg) < 1000000000000:
        return f"{str_fixed(float(int(arg) / 1000000000), int(arg), 1, 'views')}B views"

    else:
        return ''


# Brief likes format
@register.filter(name='brief_likes_format')
@stringfilter
def brief_likes_format(arg):
    if int(arg) < 1000000:
        if int(arg) == 1:
            return '1'

        elif int(arg) < 1000:
            return arg

        else:
            return f"{str_fixed(float(int(arg) / 1000), int(arg), 1, 'views')}K"

    elif int(arg) < 1000000000:
        return f"{str_fixed(float(int(arg) / 1000000), int(arg), 1, 'views')}M"

    elif int(arg) < 1000000000000:
        return f"{str_fixed(float(int(arg) / 1000000000), int(arg), 1, 'views')}B"

    else:
        return ''


# Subscribers format
@register.filter(name='subscribers_format')
@stringfilter
def subscribers_format(arg):
    if int(arg) < 1000000:
        if int(arg) == 0:
            return '0 subscribers'

        elif int(arg) == 1:
            return '1 subscriber'

        elif int(arg) < 1000:
            return f'{arg} subscribers'

        elif int(arg) < 10000:
            return f"{str_fixed(float(int(arg) / 1000), int(arg), 2, 'subscribers')}K subscribers"

        else:
            return f"{str_fixed(float(int(arg) / 1000), int(arg), 1, 'subscribers')}K subscribers"

    elif int(arg) < 1000000000:
        return f"{str_fixed(float(int(arg) / 1000000), int(arg), 1, 'subscribers')}M subscribers"

    elif int(arg) < 1000000000000:
        return f"{str_fixed(float(int(arg) / 1000000000), int(arg), 1, 'subscribers')}B subscribers"

    else:
        return ''


# ratio of likes and dislikes
@register.filter(name='ratio')
@stringfilter
def ratio(likes, dislikes):
    if int(dislikes) + int(likes) != 0:
        ratio = 1.4 * (int(dislikes) * 100 / (int(likes) + int(dislikes)))
        return int(ratio)
    else:
        return 0


# check comment like
@register.filter(name='check_comment_like')
@stringfilter
def check_comment_like(comment_id, user_id):
    return CommentLike.objects.filter(liked_comment=Comment.objects.get(comment_id=comment_id),
                                      liked_user=CustomUser.objects.get(user_id=user_id))


# check comment dislike
@register.filter(name='check_comment_dislike')
@stringfilter
def check_comment_dislike(comment_id, user_id):
    return CommentDislike.objects.filter(disliked_comment=Comment.objects.get(comment_id=comment_id),
                                         disliked_user=CustomUser.objects.get(user_id=user_id))


# check reply comment like
@register.filter(name='check_reply_comment_like')
@stringfilter
def check_reply_comment_like(reply_comment_id, user_id):
    return ReplyCommentLike.objects.filter(
        liked_reply_comment=ReplyComment.objects.get(reply_comment_id=reply_comment_id),
        liked_user=CustomUser.objects.get(user_id=user_id))


# check reply comment dislike
@register.filter(name='check_reply_comment_dislike')
@stringfilter
def check_reply_comment_dislike(reply_comment_id, user_id):
    return ReplyCommentDislike.objects.filter(
        disliked_reply_comment=ReplyComment.objects.get(reply_comment_id=reply_comment_id),
        disliked_user=CustomUser.objects.get(user_id=user_id))


# check article like
@register.filter(name='check_article_like')
@stringfilter
def check_article_like(article_id, user_id):
    return ArticleLike.objects.filter(liked_article=Article.objects.get(article_id=article_id),
                                      liked_user=CustomUser.objects.get(user_id=user_id))


# check article dislike
@register.filter(name='check_article_dislike')
@stringfilter
def check_article_dislike(article_id, user_id):
    return ArticleDislike.objects.filter(disliked_article=Article.objects.get(article_id=article_id),
                                         disliked_user=CustomUser.objects.get(user_id=user_id))


@register.filter(name='html_to_text')
@stringfilter
def html_to_text(html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', html)
    return cleantext
