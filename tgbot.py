import logging
import os

from intents import detect_intent_texts
from dotenv import load_dotenv
from handler import TelegramBotHandler
from telegram.error import NetworkError
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, CallbackContext)


logger = logging.getLogger('intents')


def start(update, context):
    update.message.reply_text('Здравствуйте')


def reply(update, context):
    try:
        user_text = update.message.text
        answer, is_fallback = detect_intent_texts(
            context.bot_data['project_id'],
            context.bot_data['token'], user_text, 'ru')
        update.message.reply_text(answer)
    except NetworkError as error:
        logger.exception(error)


def main():
    load_dotenv()

    tg_token = os.getenv('TG_BOT_TOKEN')
    logbot_token = os.getenv('TG_LOG_BOT_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')

    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramBotHandler(logbot_token, chat_id))

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    context = CallbackContext(dispatcher)

    context.bot_data['project_id'] = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
    context.bot_data['token'] = os.getenv('TG_BOT_TOKEN')

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, reply))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
