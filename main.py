import requests
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CallbackContext, CommandHandler
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
        wikipedia.set_lang("ru")
        TOKEN = '1695668954:AAGIP9C_rmojFPzHeER7_-UQNGiOnLtA8qI'
        reply_keyboard = [['WIKI', 'YANDEX MAP'],
                          ['/help', '/stop']]
        self.markup_start = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        reply_keyboard = [['Больше картинок', 'Получить url'], ['Вернуться назад']]
        self.markup_wiki = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        reply_keyboard = [['Больше информации'], ['Спутник', 'Гибрид'], ['Вернуться назад']]
        self.markup_map = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        updater = Updater(TOKEN, use_context=True)
        dp = updater.dispatcher
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                1: [CommandHandler('stop', self.stop), CommandHandler('help', self.help),
                    MessageHandler(Filters.text, self.text_handler_func)],
                2: [CommandHandler('stop', self.stop),
                    MessageHandler(Filters.text, self.wiki_handler_func, pass_user_data=True)],
                3: [CommandHandler('stop', self.stop),
                    MessageHandler(Filters.text, self.map_handler_func, pass_user_data=True)]
            },
            fallbacks=[CommandHandler('stop', self.stop)]
        )
        dp.add_handler(conv_handler)
        updater.start_polling()
        updater.idle()

    def start(self, update, context):
        update.message.reply_text('Приветствую! Я Инфо_бот, благодаря мне вы сможете найти'
                                  ' нужную вам информацию, не выходя из телеграмма! Напишите /help,'
                                  ' для получения большей информации',
                                  reply_markup=self.markup_start)
        return 1

    def stop(self, update, context):
        self.close_keyboard(update, context)
        return ConversationHandler.END

    def close_keyboard(self, update, context):
        update.message.reply_text(
            "Увидимся позже!",
            reply_markup=ReplyKeyboardRemove()
        )

    def help(self, update, context):
        update.message.reply_text('Я вижу, вам нужна информация?\n1.Нажмите "WIKI" и сообщите'
                                  ' мне то, что вы хотите найти\n2.Нажмите "YANDEX MAP" и сообщите'
                                  ' мне место, которое вы хотите получить, я же выведу вам карту'
                                  ' с этим местом! Также у вас будет возможность получить'
                                  ' дополнительную информацию об этом месте!\n3.Нажмите "/help",'
                                  ' чтобы получить эту информацию снова!\n4.Нажмите "/stop",'
                                  ' чтобы выключить меня:(\nЖелаю удачи!',
                                  reply_markup=self.markup_start)
        return 1

    def text_handler_func(self, update, context):
        if update.message.text == 'WIKI':
            update.message.reply_text('Пожалуйста, сообщите мне, что я должен для вас найти!',
                                      reply_markup=self.markup_wiki)
            return 2
        elif update.message.text == 'YANDEX MAP':
            update.message.reply_text('Пожалуйста, сообщите мне, что я должен для вас найти!',
                                      reply_markup=self.markup_map)
            return 3

    def wiki_handler_func(self, update, context):
        # получение материала с википедии стоит перенести в отдельный класс,
        # когда будет выполнен весь функционал библиотеки в программе
        if update.message.text == 'Больше картинок':
            if 'wiki_req' in context.user_data.keys():
                if len(wikipedia.page(context.user_data['wiki_req']).images) != 0:
                    for i in range(len(wikipedia.page(context.user_data['wiki_req']).images) % 10):
                        context.bot.send_photo(
                            update.message.chat_id,
                            wikipedia.page(context.user_data['wiki_req']).images[i],
                            caption=""
                        )
        elif update.message.text == 'Получить url' and 'wiki_req' in context.user_data.keys():
            update.message.reply_text(wikipedia.page(context.user_data['wiki_req']).url)
        elif update.message.text == 'Вернуться назад':
            update.message.reply_text('Надеюсь, я помог!', reply_markup=self.markup_start)
            return 1
        else:
            try:
                wikipage = wikipedia.page(update.message.text)
                context.user_data['wiki_req'] = update.message.text
                if len(wikipage.images) != 0:
                    context.bot.send_photo(
                        update.message.chat_id,
                        wikipage.images[0],
                        caption=""
                    )
                update.message.reply_text(wikipage.content[0:4096])
            except Exception:
                update.message.reply_text('По данному запросу ничего не найдено!')

    def map_handler_func(self, update, context):
        # получение материала с яндекса стоит перенести в отдельный класс,
        # когда будет выполнен весь функционал в программе
        if update.message.text == 'Больше информации' and 'map_req' in context.user_data:
            pass
        if update.message.text == 'Вернуться назад':
            update.message.reply_text('Надеюсь, я помог!', reply_markup=self.markup_start)
            return 1
        if update.message.text == 'Спутник' and 'map_req' in context.user_data.keys():
            l_map = 'sat'
        elif update.message.text == 'Гибрид' and 'map_req' in context.user_data.keys():
            l_map = 'sat,skl'
        else:
            l_map = 'map'
            context.user_data['map_req'] = update.message.text
        try:
            geocoder_uri = geocoder_request_template = "http://geocode-maps.yandex.ru/1.x/"
            response = requests.get(geocoder_uri, params={
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                "format": "json",
                "geocode": context.user_data['map_req']
            })
            toponym = response.json()["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]
            ll, spn = self.get_ll_spn(toponym)
            static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l={l_map}"
            context.bot.send_photo(
                update.message.chat_id,
                static_api_request,
                caption=""
            )
        except Exception:
            update.message.reply_text("По данному запросу ничего не найдено!")

    def get_ll_spn(self, toponym):
        ll = ','.join(toponym["Point"]["pos"].split())
        spn = ','.join([str(float(toponym["boundedBy"]["Envelope"]["upperCorner"].split()[0]) - float(toponym["boundedBy"]["Envelope"]["lowerCorner"].split()[0])),
                        str(float(toponym["boundedBy"]["Envelope"]["upperCorner"].split()[1]) - float(toponym["boundedBy"]["Envelope"]["lowerCorner"].split()[1]))])
        return ll, spn


if __name__ == '__main__':
    bot = Bot()
