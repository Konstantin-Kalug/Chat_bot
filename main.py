import requests
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CallbackContext, CommandHandler
import random
import wikipedia
import os
from data import db_session
from data.articles import Article
from data.users import User


class Bot:
    def __init__(self):
        # инициализация бота
        TOKEN = '1695668954:AAGIP9C_rmojFPzHeER7_-UQNGiOnLtA8qI'
        updater = Updater(TOKEN, use_context=True)
        self.db = DataBase("db/info.db")
        self.create_standart_keyboards()
        dp = updater.dispatcher
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                1: [CommandHandler('stop', self.stop), CommandHandler('help', self.help),
                    MessageHandler(Filters.text, self.text_handler_func)],
                2: [CommandHandler('stop', self.stop),
                    MessageHandler(Filters.text, self.wiki_handler_func, pass_user_data=True)],
                3: [CommandHandler('stop', self.stop),
                    MessageHandler(Filters.text, self.map_handler_func, pass_user_data=True)],
                4: [CommandHandler('stop', self.stop),
                    MessageHandler(Filters.text, self.create_articles_title_handler_func,
                                   pass_user_data=True)],
                5: [CommandHandler('stop', self.stop),
                    MessageHandler(Filters.text, self.create_articles_text_handler_func,
                                   pass_user_data=True)],
                6: [CommandHandler('stop', self.stop), CommandHandler('help', self.help),
                    MessageHandler(Filters.text, self.transliteration_handler_func)]
            },
            fallbacks=[CommandHandler('stop', self.stop)]
        )
        dp.add_handler(conv_handler)
        updater.start_polling()
        updater.idle()

    def create_standart_keyboards(self):
        # создание всех основных клавиатур
        reply_keyboard = [['WIKI', 'YANDEX MAP', 'TRANSLITERATION'],
                          ['Создать статью'],
                          ['Изменить статью', 'Удалить статью'],
                          ['Статьи'],
                          ['Вывести статистику'],
                          ['/help', '/stop']]
        self.markup_start = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        reply_keyboard = [['Больше картинок', 'Получить url'], ['Вернуться назад']]
        self.markup_wiki = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        reply_keyboard = [['Спутник', 'Гибрид'], ['Вернуться назад']]
        self.markup_map = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        self.markup_back = ReplyKeyboardMarkup([['Вернуться назад']], one_time_keyboard=False)

    def create_keyboard_articles(self, update, context):
        # создание клавиатуры для просмотра статей
        pass

    def start(self, update, context):
        # привествуем пользователя и добавляем его в базу, если его нет
        update.message.reply_text('Приветствую! Я Инфо_бот, благодаря мне вы сможете найти'
                                  ' нужную вам информацию, не выходя из телеграмма! Напишите /help,'
                                  ' для получения большей информации',
                                  reply_markup=self.markup_start)
        if not(self.db.search_chat(update.message.chat_id)):
            self.db.add_user(update, context)
        return 1

    def stop(self, update, context):
        # завершаем работу бота
        self.close_keyboard(update, context)
        return ConversationHandler.END

    def close_keyboard(self, update, context):
        # скрываем клавиатуру
        update.message.reply_text(
            "Увидимся позже!",
            reply_markup=ReplyKeyboardRemove()
        )

    def help(self, update, context):
        # вывод помощи пользователю
        update.message.reply_text('Я вижу, вам нужна информация?\n1.Нажмите "WIKI" и сообщите'
                                  ' мне то, что вы хотите найти\n2.Нажмите "YANDEX MAP" и сообщите'
                                  ' мне место, которое вы хотите получить, я же выведу вам карту'
                                  ' с этим местом! Также у вас будет возможность получить'
                                  ' дополнительную информацию об этом месте!\n'
                                  '3.Нажмите TRANSLITIRATION'
                                  ', и передайте мне текст, раскладку которого хотите поменять\n'
                                  '4."/help",'
                                  ' чтобы получить эту информацию снова!\n5.Нажмите "/stop",'
                                  ' чтобы выключить меня:(\nЖелаю удачи!',
                                  reply_markup=self.markup_start)
        return 1

    def text_handler_func(self, update, context):
        # проверяем активность начальных кнопок
        if update.message.text == 'WIKI':
            update.message.reply_text('Пожалуйста, сообщите мне, что я должен для вас найти!',
                                      reply_markup=self.markup_wiki)
            return 2
        elif update.message.text == 'YANDEX MAP':
            update.message.reply_text('Пожалуйста, сообщите мне, что я должен для вас найти!',
                                      reply_markup=self.markup_map)
            return 3
        elif update.message.text == 'TRANSLITERATION':
            update.message.reply_text('Пожалуйста,'
                                      ' введите текст, раскладку которого вы хотите поменять!!',
                                      reply_markup=self.markup_back)
            return 6
        elif update.message.text == 'Вывести статистику':
            self.db.get_stat(update.message.chat_id, update, context)
        elif update.message.text == 'Создать статью':
            if self.db.checking_the_number_of_articles(update.message.chat_id):
                update.message.reply_text('Пожалуйста, дайте название своей статье!',
                                          reply_markup=self.markup_back)
                return 4
            else:
                update.message.reply_text('Эй, вы уже слишком много статей создали (20)!')
        elif update.message.text == 'Статьи':
            update.message.reply_text('Выберите, что именно вы хотите посмотреть!',
                                      reply_markup=self.markup_back)

    def create_articles_title_handler_func(self, update, context):
        # проверка ввода названия статьи
        if update.message.text == 'Вернуться назад':
            update.message.reply_text('Ожидаю вашего возвращения!', reply_markup=self.markup_start)
            return 1
        else:
            context.user_data['title_article'] = update.message.text
            update.message.reply_text('Пожалуйста, введите текст вашей статьи!',
                                      reply_markup=self.markup_back)
            return 5

    def create_articles_text_handler_func(self, update, context):
        # проверка ввод названия статьи
        if update.message.text == 'Вернуться назад':
            update.message.reply_text('Ожидаю вашего возвращения!', reply_markup=self.markup_start)
        else:
            # добавляем статью в базу
            context.user_data['text_article'] = update.message.text
            self.db.add_article(update.message.chat_id, update, context)
            update.message.reply_text('Статья создана!', reply_markup=self.markup_start)
            self.db.update_stat(update.message.chat_id, 'art')
        return 1

    def articles_handler_func(self, update, context):
        # роверяем статьи
        pass

    def wiki_handler_func(self, update, context):
        # получение большего количества картинок по запросу
        if update.message.text == 'Больше картинок':
            if 'wiki_req' in context.user_data.keys():
                context.user_data['wiki_req'].get_images(update, context)
            else:
                update.message.reply_text('А я не знаю, что вам отправить!')
        # получение url
        elif update.message.text == 'Получить url':
            if 'wiki_req' in context.user_data.keys():
                context.user_data['wiki_req'].get_url(update, context)
            else:
                update.message.reply_text('Нельзя получить url "никакой" страницы!')
        # возвращение на начальную клавиатуру
        elif update.message.text == 'Вернуться назад':
            update.message.reply_text('Надеюсь, WIKI вам помогла!', reply_markup=self.markup_start)
            return 1
        # выводим контент википедии и сохраняем запрос для последующего возможного использования
        else:
            try:
                wiki = Wiki(update.message.text)
                context.user_data['wiki_req'] = wiki
                context.user_data['wiki_req'].get_content(update, context)
                self.db.update_stat(update.message.chat_id, 'wiki')
            except Exception:
                update.message.reply_text("По данному запросу ничего не найдено!")

    def map_handler_func(self, update, context):
        # возвращаемся
        if update.message.text == 'Вернуться назад':
            update.message.reply_text('Надеюсь, я помог!', reply_markup=self.markup_start)
            return 1
        # меняем тип карты на спутник
        elif update.message.text == 'Спутник':
            if 'map_req' in context.user_data.keys():
                context.user_data['map_req'].set_l('sat', update, context)
            else:
                update.message.reply_text('Я даже не догадываюсь, что отправить!')
        # меняем тип карты на гибрид
        elif update.message.text == 'Гибрид':
            if 'map_req' in context.user_data.keys():
                context.user_data['map_req'].set_l('sat,skl', update, context)
            else:
                update.message.reply_text('Я отказываюсь что-либо отправлять-_-')
        else:
            # создание запроса и отправка карты
            try:
                ymap = YandexMap(update, update.message.text)
                context.user_data['map_req'] = ymap
                ymap.send_map(update, context)
                self.db.update_stat(update.message.chat_id, 'map')
            except Exception:
                update.message.reply_text("По данному запросу ничего не найдено!")

    def transliteration_handler_func(self, update, context):
        mes = update.message.text
        if mes != '' and mes != 'Вернуться назад':
            try:
                translit = Translit()
                new_mes = translit.transliteration(mes)
                update.message.reply_text(new_mes, reply_markup=self.markup_back)
                # self.db.update_stat(update.message.chat_id, 'translits')
                return 6
            except Exception:
                update.message.reply_text("Небольшие неполадки!")
        elif mes == 'Вернуться назад':
            update.message.reply_text('Надеюсь, TRANSLITERATION вам помог!',
                                      reply_markup=self.markup_start)
            return 1


class Translit(Bot):
    def __init__(self):
        self.keymap = {'f': 'а', ',': 'б', 'd': 'в', 'u': 'г', 'l': 'д', 't': 'е', '`': 'ё', ';': 'ж',
                  'p': 'з', 'b': 'и',
                  'q': 'й', 'r': 'к', 'k': 'л', 'v': 'м', 'y': 'н', 'j': 'о', 'g': 'п', 'h': 'р',
                  'c': 'с', 'n': 'т',
                  'e': 'у', 'a': 'ф', '[': 'х', 'w': 'ц', 'x': 'ч', 'i': 'ш', 'o': 'щ', ']': 'ъ',
                  's': 'ы', 'm': 'ь',
                  "'": 'э', '.': 'ю', 'z': 'я', }

    def transliteration(self, message):
        new_mes = ''
        for i in message:
            if i.isupper():
                new_mes += (self.keymap[i.lower()]).upper()
            elif i not in self.keymap:
                new_mes += i
            else:
                new_mes += self.keymap[i]
        return new_mes


class Wiki(Bot):
    def __init__(self, request):
        # переменные вывода
        wikipedia.set_lang("ru")
        wikipage = wikipedia.page(request)
        self.images = wikipage.images
        self.url = wikipage.url
        self.content = wikipage.content

    def get_images(self, update, context):
        # отправляем до 10 картинок, если можем
        if len(self.images) != 0:
            for i in range(len(self.images) % 10):
                try:
                    context.bot.send_photo(
                        update.message.chat_id,
                        self.images[i],
                        caption=""
                    )
                except Exception:
                    pass
        else:
            update.message.reply_text('К сожалению, фотографий не нашлось!')

    def get_url(self, update, context):
        # отправляем url
        update.message.reply_text(self.url)

    def get_content(self, update, context):
        # отправляем основной контент
        if len(self.images) != 0:
            for i in range(len(self.images) % 10):
                try:
                    context.bot.send_photo(
                        update.message.chat_id,
                        self.images[i],
                        caption=""
                    )
                    break
                except Exception:
                    pass
        update.message.reply_text(self.content[:4096])


class DataBase(Bot):
    def __init__(self, address):
        # нициализируем базу данных
        db_session.global_init(address)
        self.db_sess = db_session.create_session()

    def add_user(self, update, context):
        # добавляем пользователя
        user = User(chat_id=update.message.chat_id)
        self.db_sess.add(user)
        self.db_sess.commit()

    def add_article(self, chat_id, update, context):
        # добавляем статью
        article = Article(title=context.user_data['title_article'],
                          content=context.user_data['text_article'],
                          user_id=chat_id)
        self.db_sess.add(article)
        self.db_sess.commit()

    def checking_the_number_of_articles(self, chat_id):
        if len(self.db_sess.query(Article).filter(Article.user_id == chat_id)) >= 20:
            return False
        return True

    def search_chat(self, chat_id):
        # ищем пользователя в базе
        for user in self.db_sess.query(User).filter(User.chat_id == chat_id):
            return True
        return False

    def get_stat(self, chat_id, update, context):
        # выводим статистику
        for user in self.db_sess.query(User).filter(User.chat_id == chat_id):
            text = f'1.Количество WIKI запросов: {user.wiki_requests}\n' \
                   f'2.Количество YANDEX MAP запросов: {user.maps_requests}\n' \
                   f'3.Количество статей: {user.articles}\n' \
                   f'4.Количество переводов: {user.translits}\n' \
                   f'5.Общий рейтинг: {user.overall_rating}'
            update.message.reply_text(text)

    def update_stat(self, chat_id, type):
        # обновляем статистику
        # функция работает, ошибки возникают в вызове
        for user in self.db_sess.query(User).filter(User.chat_id == chat_id):
            if type == 'wiki':
                user.wiki_requests += 1
                user.overall_rating += 1
            elif type == 'map':
                user.maps_requests += 1
                user.overall_rating += 5
            elif type == 'art':
                user.articles += 1
                user.overall_rating += 10
            elif type == 'translits':
                user.translits += 1
                user.overall_rating += 1
            self.db_sess.commit()


class YandexMap(Bot):
    def __init__(self, update, request):
        # нициализируем запрос
        geocoder_uri = geocoder_request_template = "http://geocode-maps.yandex.ru/1.x/"
        response = requests.get(geocoder_uri, params={
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "format": "json",
            "geocode": request
            })
        toponym = response.json()["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        self.text = 'Адрес:'
        for c in toponym['metaDataProperty']['GeocoderMetaData']['Address']['Components']:
            self.text += f' {c["name"]}'
        self.ll, self.spn = self.get_ll_spn(toponym)
        self.l_map = 'map'

    def set_l(self, type, update, context):
        # меняем тип карты
        self.l_map = type
        self.send_map(update, context)

    def send_map(self, update, context):
        # отправляем пользователю карту
        static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={self.ll}&spn={self.spn}&l={self.l_map}"
        context.bot.send_photo(
            update.message.chat_id,
            static_api_request,
            caption=self.text
        )

    def get_ll_spn(self, toponym):
        # получаем координаты и масштаб
        ll = ','.join(toponym["Point"]["pos"].split())
        spn = ','.join([str(float(toponym["boundedBy"]["Envelope"]["upperCorner"].split()[0])
                            - float(toponym["boundedBy"]["Envelope"]["lowerCorner"].split()[0])),
                        str(float(toponym["boundedBy"]["Envelope"]["upperCorner"].split()[1])
                            - float(toponym["boundedBy"]["Envelope"]["lowerCorner"].split()[1]))])
        return ll, spn





if __name__ == '__main__':
    bot = Bot()
