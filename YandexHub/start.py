#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'YandexHub.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'runserver'])


if __name__ == '__main__':
    main()
