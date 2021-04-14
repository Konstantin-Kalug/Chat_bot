import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import wikipedia
import os
from data import db_session


class Requests:
    def __init__(self, message):
        self.req = message


class Wiki(Requests):
    pass


class YandexMap(Requests):
    pass


class Bot:
    def __init__(self):
        self.auth()
        # инициализируем базу данных
        db_session.global_init("db/info.db")
        self.db_sess = db_session.create_session()

    def auth(self):
        TOKEN = 'fe00dcd62f63e92ebabffc7337ed7f96e79997293643' \
                     'd77a4a919aa24ac39789ac7f237dc6c5701b8db36'
        self.vk_session = vk_api.VkApi(token=TOKEN)
        self.longpoll = VkBotLongPoll(self.vk_session, 202901806)

    def send_pictures(self):
        pass

    def longpool_func(self):
        pass

    def keyboard(self):
        keyboard = vk_api.keyboard.VkKeyboard(one_time=False)
        keyboard.add_button("WIKIPEDIA", color=vk_api.keyboard.VkKeyboardColor.DEFAULT)
        keyboard.add_line()  # Обозначает добавление новой строки
        keyboard.add_button("YANDEX MAP", color=vk_api.keyboard.VkKeyboardColor.DEFAULT)
        return keyboard.get_keyboard()

