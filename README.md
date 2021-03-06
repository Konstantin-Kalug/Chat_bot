# Chat_bot

## Введение
Часто бывает, что во время использования мессенджеров пользователю требуется найти определенную информацию. Если с персонального компьютера или ноутбука требуется только открыть браузер во втором окне,
то для пользователям со смартфонов это сделать труднее, хоть и началось распространение функции разделения экрана. Как же можно поправить эти неудобства? Можно искать информацию прямо в своем любимом мессенджере!
Данный бот позволяет искать информацию и делиться какими-то статьями, не выходя из телеграмма, который продолжает набирать большую популярность среди пользователей мессенджеров.

## Функции бота
1. WIKI - получение информации с википедии, изображений и url статей нужных пользователю статей
2. YANDEX MAP - получение карт с Яндекс.Карт (стандартная, спутниковая и гибридная)
3. TRANSLITERATIONS - исправление раскладки сообщения
4. Создать статью - создание статьи
5. Удалить статью - удаление стать
6. Изменить статью - изменение статей
7. Статьи - просмотр своих и чужих статей
8. Вывести статистику - вывод статистики пользователя (больше информации см.Структура программы - Структура data/db/info.db - Таблица users)
9. /help - вывод помощи по боту
10. /stop - остановка работы бота

## Возможности к улучшению
На данный момент бот имеет достаточное количество функций, которые могут пригодиться пользователям мессенджера. Но все же есть возможности к улучшению бота:
1. Использование большего количества возможностей API Yandex.Geocoder и Yandex.Static в боте
2. Использование большего количество возможностей библиотеки wikipedia
3. Использование большего количества информационных ресурсов
4. Возможность приложить изображения и другие файлы в статью
5. Проверка на плагиат текста статей
6. Большее количество различных сообщений от бота

## Использованные библиотеки
1. requests - создание запросов и получение информации через API
2. python-telegram-bot - основа бота
3. wikipedia - получение контента из википедии
4. sqlalchemy - использование базы данных с orm

## Структура программы
### Структура проекта
Для работы бота используются файлы:
1. requirements.txt - список зависимостей, библиотек
2. main.py - основной файл со всеми алгоритмами
3. Procfile - рабочий файл для деплоя в heroku
4. db/info.db - база данных, где хранится информация о пользователях и их статьях
5. data/users.py - orm для таблицы users в базе данных
6. data/db_session.py - файл для работы с базой данных
7. data/articles.py - orm для таблицы articles в базе данных
8. data/\__all_models.py - файл для использования orm

### Структура main.py
#### Class Bot
Данный класс используется для работы бота: в нем происходят все проверки и процессы, необходимые для взаимодействия с пользователям.
В данном классе используются следующие методы:
1. \__init__() - инициализация бота
2. create_standart_keyboards() - создание всех основных клавиатур, с которыми будет взаимодействовать пользователь
3. start(update, context) - комманда **start**, запускаемая при первом входе пользователя или перезапуска
4. stop(update, context) - комманда **stop**, которая выключает бота
5. help(update, context) - комманда **help**, которая выводит вспомогательную информацию
6. close_keyboard(update, context) - скрытие клавиатуры при остановки выключении бота
7. text_handler_func(update, context) - проверка всех начальных текстового ввода пользователя и клавиатуры для перехода в работу других функций
8. create_articles_title_handler_func(update, context) - проверка текстового ввода пользователя и клавиатуры, чтобы дать название статье
9. create_articles_text_handler_func(update, context) - проверка текстового ввода пользователя и клавиатуры, чтобы указать текст статьи
10. delete_articles_handler_func(update, context) - проверка текстового ввода пользователя и клавиатуры, чтобы удалить статью
11. update_articles_text_handler_func(update, context) - проверка текстового ввода пользователя и клавиатуры, чтобы изменить текст статьи
12. articles_handler_func(update, context) - проверка текстового ввода пользователя и клавиатуры, чтобы выбрать, чьи статьи смотреть
13. output_articles_handler_func(update, context) - проверка текстового ввода пользователя и клавиатуры, чтобы выбрать, какую статью вывести или изменить
14. wiki_handler_func(update, context) - проверка текстового ввода пользователя и клавиатуры, чтобы выполнить запрос в википедию или получить изображения и url статьи
15. map_handler_func(update, context) - проверка текстового ввода пользователя и клавиатуры, чтобы выполнить запрос в яндекс.карты или изменить тип карты (гибрид и спутник)
16. transliteration_handler_func(update, context) - проверка текстового ввода пользователя и клавиатуры, чтобы исправить раскладку сообщения

#### Class Wiki
Данный класс используется для создания запросов в википедию и вывода информацию с энциклопедии.
В данном классе используются следуюие методы:
1. \__init__(request) - инициализация запроса
2. get_images(update, context) - получение большего количества изображений из википедии
3. get_url(update, context) - получение url оригинальной статьи
4. get_content(update, context) - получение основного контента из википедии

#### Class YandexMap
Данный класс используется для создания запросов в яндекс.карты и вывода карт с ресурса.
В данном классе используются следующие методы:
1. \__init__(update, request) - инициализация запроса
2. set_l(type, update, context) - изменение типа карты (гибрид и спутник)
3. send_map(update, context) - вывод пользователю фрагмента карты
4. get_ll_spn(self, toponym) - получение координат и масштаба места

#### Class Translit
Данный класс используется для изменения раскладки сообщения.
В данном классе используются следующие методы:
1. \__init__() - инициализация раскладок
2. transliteration(message) - замена символов на другую раскладку

#### DataBase
Данный класс используется для работы с базой данных:
В данном классе используются следующие методы:
1. \__init__(address) - инициализация базы данных
2. create_keyboard(context, update) - создание списка статей для клавиатуры
3. output_arciles(title) - получение статьи для последующего вывода
4. add_user(update, context) - добавление пользователя в базу данных
5. add_article(chat_id, update, context) - добавление статьи в базу данных
6. del_article(chat_id, title) - удаление статьи из базы данных
7. update_article(title, text) - изменение текста статьи в базе данных
8. checking_the_number_of_articles(chat_id) - проверка количества статей у пользователя (не больше 20-и)
9. check_articles_titles(title) - проверка на повторение названия статьи
10. search_chat(chat_id) - проверка на нахождение пользователя в базу данных
11. get_stat(chat_id, update, context) - вывод статистики пользователя
12. update_stat(chat_id, type) - обновление статистики пользователя

### Структура data/users.py
#### Class User
Данный клас используется для добавления таблицы с пользователями в базу данных. Класс реализуется для работы с orm и не содержит дополнительных методов.

### Структура data/db_session.py
#### def global_init(db_file)
Данная функция служит для инициализации и создания базы данных с нужными нам таблицами.

#### def create_session()
Данная функция служит для начала работы с базой данных внутри программы.

### Структура data/articles.py
#### Class Article
Данный клас используется для добавления таблицы со статьями в базу данных. Класс реализуется для работы с orm и не содержит дополнительных методов.

### Структура data/\__all_models.py
Данный файл используется для взаимодействия с базой данных и orm. Не содержит функций и классов.

### Структура data/db/info.db
#### Таблица users
Данная таблица содержит в себе информацию о пользователях, которые используют бота. Содержит следующие поля:
1. id - id записи
2. chat_id - id чата
3. wiki_requests - количество запросов в википедию от пользователя
4. maps_requests - количество запросов в яндекс карты от пользователя
5. articles - количество созданных статей (не уменьшается при удалении статей)
6. translits_requests - количество использований функции transliteration
7. overall_rating  - общий рейтинг пользователя (не является суммой предыдущих данных)

#### Таблица articles
Данная таблица содержит в себе информацию о статьях, созданных пользователями, которые используют бота. Содержит следующие поля:
1. id - id записи
2. title - название статьи
3. content - текст статьи
4. user - id чата, пользователь которого создал статью

## Заключение
Бот работает полностью исправно без каких-либо нареканий. Имеется достаточное количество функций для комфортной работы. К тому же имеется большое количество возможностей для последующего улучшения бота с малым количеством рамок и ограничений. Сам же код имеет все признаки хорошего кода:
1. Говорящие имена переменных
2. Большое количество комментариев
3. Понятный порядок функций и классов
4. Удобная структура проекта
