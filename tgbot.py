import logging
import os

from dotenv import load_dotenv
from google.cloud import dialogflow
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, CallbackContext)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
load_dotenv()

token = os.getenv('TG_BOT_TOKEN')
project_id = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')


def start(update, context):
    update.message.reply_text('Здравствуйте')


def greet(update, context):
    user_text = update.message.text
    answer = detect_intent_texts(context.bot_data['project_id'], token, user_text, 'ru')
    update.message.reply_text(answer)


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    print("=" * 20)
    print("Query text: {}".format(response.query_result.query_text))
    print(
        "Detected intent: {} (confidence: {})\n".format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        )
    )
    print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
    return response.query_result.fulfillment_text


def main():
    updater = Updater(token)

    dispatcher = updater.dispatcher
    context = CallbackContext(dispatcher)
    context.bot_data['project_id'] = 'game-of-verbs-316712'

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, greet))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
