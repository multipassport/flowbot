import random
import os
import vk_api as vk

from detect_intents import detect_intent_texts
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1, 1000)
    )


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
    project_id = os.getenv('PROJECT_ID')

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer(event, vk_api, project_id)


if __name__ == '__main__':
    main()
