import logging
import os

from detect_intents import detect_intent_texts
from dotenv import load_dotenv
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, CallbackContext)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
load_dotenv()


def start(update, context):
    update.message.reply_text('Здравствуйте')


def greet(update, context):
    user_text = update.message.text
    answer, is_fallback = detect_intent_texts(
        context.bot_data['project_id'],
        context.bot_data['token'], user_text, 'ru')
    update.message.reply_text(answer)


def main():
    token = os.getenv('TG_BOT_TOKEN')
    updater = Updater(token)

    dispatcher = updater.dispatcher
    context = CallbackContext(dispatcher)
    context.bot_data['project_id'] = os.getenv('PROJECT_ID')
    context.bot_data['token'] = os.getenv('TG_BOT_TOKEN')

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, greet))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
