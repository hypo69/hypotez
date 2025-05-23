# Модуль ToolBox_send

## Обзор

Этот модуль предназначен для отправки рекламных сообщений пользователям Telegram-бота, которые еще не использовали промокод. Он использует библиотеку `telebot` для взаимодействия с Telegram API и `sqlite3` для работы с базой данных пользователей. Модуль загружает токен бота из переменных окружения и отправляет сообщение с промокодом пользователям, у которых в базе данных не указано использование промокода.

## Подробней

Этот модуль является частью проекта `hypotez` и используется для распространения информации о промоакциях среди пользователей Telegram-бота. Он подключается к базе данных, выбирает пользователей, которые еще не использовали промокод, и отправляет им сообщение с информацией о промокоде. Это позволяет информировать пользователей о новых возможностях и стимулировать их к использованию платных функций бота.

## Классы

В данном модуле классы отсутствуют.

## Функции

### Отправка сообщений пользователям Telegram-бота

```python
import telebot, sqlite3, os
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(token=os.environ['TOKEN'])
conn = sqlite3.connect('UsersData.db')
cursor = conn.cursor()
cursor.execute(f"SELECT id FROM users_data_table WHERE promocode != 1")
users = cursor.fetchall()
for us in users:
    try:
        bot.send_message(chat_id=us[0], text="Успейте воспользоваться промокодом FREE24 до 21 декабря!\n\nПо нему вы получите бесплатный месяц тарифа PRO — это безлимит на генерацию текста и изображений 💥 \n\nЧтобы ввести промокод, перейдите на вкладку Тарифы и нажмите кнопку «Промокод».", parse_mode='html')
    except:
        print(us[0], "no")
    else:
        print(us[0], "yes")
```

**Назначение**: Отправляет рекламные сообщения пользователям Telegram-бота, которые еще не использовали промокод.

**Параметры**:

- Отсутствуют параметры на входе, но используются переменные окружения и данные из базы данных.

**Возвращает**:

- Ничего не возвращает.

**Вызывает исключения**:

- `telebot.apihelper.ApiTelegramException`: Возникает при ошибках при отправке сообщений через Telegram API.

**Как работает функция**:

1.  Импортирует необходимые библиотеки: `telebot`, `sqlite3`, `os` и `dotenv`.
2.  Загружает переменные окружения из файла `.env` с помощью `load_dotenv()`.
3.  Создает экземпляр Telegram-бота `bot` с использованием токена, полученного из переменной окружения `TOKEN`.
4.  Подключается к базе данных SQLite `UsersData.db`.
5.  Создает курсор `cursor` для выполнения SQL-запросов.
6.  Выполняет SQL-запрос для выборки `id` пользователей из таблицы `users_data_table`, у которых значение столбца `promocode` не равно 1 (то есть, они еще не использовали промокод).
7.  Получает список `users` с результатами запроса.
8.  Итерируется по списку пользователей `users`.
9.  Для каждого пользователя пытается отправить сообщение с информацией о промокоде.
10. Если отправка сообщения прошла успешно, выводит в консоль `id` пользователя и "yes".
11. Если при отправке сообщения произошла ошибка, выводит в консоль `id` пользователя и "no".

**Примеры**:

Пример отправки сообщения пользователю с `id` 123456789:

```python
import telebot, sqlite3, os
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(token=os.environ['TOKEN'])
conn = sqlite3.connect('UsersData.db')
cursor = conn.cursor()
cursor.execute(f"SELECT id FROM users_data_table WHERE promocode != 1")
users = cursor.fetchall()
for us in users:
    try:
        bot.send_message(chat_id=us[0], text="Успейте воспользоваться промокодом FREE24 до 21 декабря!\n\nПо нему вы получите бесплатный месяц тарифа PRO — это безлимит на генерацию текста и изображений 💥 \n\nЧтобы ввести промокод, перейдите на вкладку Тарифы и нажмите кнопку «Промокод».", parse_mode='html')
    except:
        print(us[0], "no")
    else:
        print(us[0], "yes")
```

## Параметры модуля

В данном модуле параметры класса отсутствуют.