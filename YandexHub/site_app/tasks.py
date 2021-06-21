from YandexHub.celery import app
from .service import bot


@app.task
def send_notification(text, telegram_id):
    bot(text, telegram_id)
