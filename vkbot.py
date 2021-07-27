import logging
import random
import os
import vk_api as vk

from intents import detect_intent_texts
from dotenv import load_dotenv
from handler import TelegramBotHandler
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.exceptions import ApiError


logger = logging.getLogger('intents')


def answer(event, vk_api, project_id):
    message, is_fallback = detect_intent_texts(
        project_id, event.user_id, event.text, 'ru')
    if not is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=message,
            random_id=random.randint(1, 1000)
        )


def main():
    load_dotenv()

    vk_token = os.getenv('VK_API_TOKEN')
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
    logbot_token = os.getenv('TG_LOG_BOT_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')

    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramBotHandler(logbot_token, chat_id))

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        try:
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                answer(event, vk_api, project_id)
        except ApiError as error:
            logger.exception(error)


if __name__ == '__main__':
    main()
