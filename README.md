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
* JavaScript ES9
* JS Fetch Api
* CSS 3
* HTML 5
* Bootstrap 4

## How to run?
In order to run this project you need:
1) Installation `requarements.txt` file with the `pip install -r requarements.txt` command
2) In `SocketServer/settings.py` enter your `email` and `email password` for `smtp`
3) Run `SocketServer` with the `python manage.py runserver 9000` command
4) Run `YandexHub` with the `python manage.py runserver 8000` command

## How to test?
* In `http://127.0.0.1:8000/` enter some name and email, then click `Send` button

## Admin account (test account)
* Email: example@example.com
* Password: KLaf32!M@42
