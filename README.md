# YandexHub video hosting 👻

## What is it?
YandexHub is a video hosting service that provides users with video storage and display services. Users
can upload, view, rate, comment, add to favorites, and share certain
videos. The site features videos, movies, and music.

## Real website
https://yandexhub.ru

## What used?
* Python 3.7+
* Django 3
* Django Rest Framework
* Django Channels
* Celery
* Redis
* JavaScript ES9
* JS Fetch Api
* CSS 3
* HTML 5
* Bootstrap 4

## How to run?
In order to run this project you need:
1) Install `requirements.txt` file with the `pip install -r requirements.txt` command
2) In `YandexHub/mainapp/bot.py` file enter `bot token` 
```python
  bot = telebot.TeleBot('...')
```
3) In `YandexHub/YandexHub/settings.py` file enter your `email` and `email password` for `smtp`
```python
  EMAIL_USE_TLS = True
  EMAIL_HOST = 'smtp.gmail.com'
  EMAIL_PORT = 587
  EMAIL_HOST_USER = '...'
  EMAIL_HOST_PASSWORD = '...'
```
4) Run `YandexHub` with the `python manage.py runserver` command
5) Run `Redis` in `Docker` with port `6379`
6) Run `Celery` with `celery -A YandexHub worker -l info` command

## Admin account (test account)
* Email: example@example.com
* Password: KLaf32!M@42
