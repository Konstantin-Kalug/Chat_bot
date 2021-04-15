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
        updater = Updater(TOKEN, use_context=True)
        dp = updater.dispatcher
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                1: [CommandHandler('stop', self.stop), CommandHandler('help', self.help),
                    MessageHandler(Filters.text, self.text_handler_func)],
                2: [CommandHandler('stop', self.stop),
                    MessageHandler(Filters.text, self.wiki_handler_func, pass_user_data=True)]
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


if __name__ == '__main__':
    bot = Bot()
