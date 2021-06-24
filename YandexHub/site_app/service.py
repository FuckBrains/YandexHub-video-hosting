# telebot
import telebot

# python
import traceback

# moviepy
from moviepy.editor import *
from moviepy.config import change_settings

# models 
from .models import Video

# work with file path
import ntpath
import os

from django.core.files import File


def bot(text, telegram_id):

    try:
        bot = telebot.TeleBot('...')
        bot.send_message(telegram_id, text)
        return 200
    except Exception as e:
        # bot was blocked by the user
        if traceback.format_exc().find('403') != -1:
            return 403

        # chat not found
        elif traceback.format_exc().find('400') != -1:
            return 400

        else:
            return 500


# processing video
def processing_video(video_id):

    # if you use Windows OS, if not delete it
    try:
        change_settings(
            {"IMAGEMAGICK_BINARY": "C:\Program Files\ImageMagick-7.1.0-Q16-HDRI\magick.exe"}
        )
    except:
        pass

    # get all video models
    video = Video.objects.filter(id=video_id)

    # get video model
    video = video.first()

    # get variables
    video_path = video.video.path
    video_name = ntpath.basename(video.video.name)

    _video = VideoFileClip(video_path)

    final_video = _video.resize(
        (_video.w * 0.75, _video.h * 0.75)
        ).write_videofile(
        f"media/videos/processed/{video_name}",
        fps=30,
        codec="libx264"
    )

    # add final video in video model
    video.video = File(
        open(f"media/videos/processed/{video_name}", mode="rb"),
        name=f"processed/{video_name}"
    )
    video.save()

    # delete first file
    os.remove(f"media/videos/{video_name}")
    os.remove(f"media/videos/processed/{video_name}")
