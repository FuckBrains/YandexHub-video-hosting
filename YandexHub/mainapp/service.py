# TELEGRAM
import telebot
import traceback


def bot(text, telegram_id):
    try:
        bot = telebot.TeleBot('1785721677:AAGx0BAnxfsPStpIL2aFtgKvkiKSEx-dReQ')
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
