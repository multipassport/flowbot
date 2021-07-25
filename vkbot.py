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


def answer(event, vk_api):
    if message := detect_intent_texts('game-of-verbs-316712', event.user_id, event.text, 'ru'):
        vk_api.messages.send(
            user_id=event.user_id,
            message=message,
            random_id=random.randint(1, 1000)
        )


def main():
    load_dotenv()

    vk_token = os.getenv('VK_API_TOKEN')
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer(event, vk_api)


if __name__ == '__main__':
    main()