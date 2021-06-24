from YandexHub.celery import app
from .service import *


@app.task
def send_notification(text, telegram_id):
    bot(text, telegram_id)


@app.task
def processing_video_task(video_id):
    processing_video(video_id)