# TELEGRAM
import telebot
import traceback


def YandexHubAlert(text, telegram_id):
    try:
        '''
        Если бот не будет работать, то...
        1) Создайте своего telegram бота по инструкции https://core.telegram.org/bots#6-botfather
        2) Полученный token вставьте вместо старого 
        '''
        bot = telebot.TeleBot('1785721677:AAF0OeaZ-ZC_Zf5IF0BMaDqacKE3y7OB290')
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
            pass
