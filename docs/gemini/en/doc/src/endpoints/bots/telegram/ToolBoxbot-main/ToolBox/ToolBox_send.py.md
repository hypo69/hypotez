# ToolBox_send.py

## Overview

This module is responsible for sending promotional messages to Telegram users who have not yet activated a promocode.

## Details

This script uses the `telebot` and `sqlite3` libraries to interact with a Telegram bot and a local SQLite database. It retrieves a list of users from the `users_data_table` who have not activated a promocode (`promocode != 1`). For each user, the script attempts to send a promotional message explaining the benefits of the PRO tariff and how to activate the `FREE24` promocode. If the message is sent successfully, it logs the user ID with "yes"; otherwise, it logs the user ID with "no."

## Functions

### `send_promo_messages`

```python
def send_promo_messages():
    """
    Отправляет рекламные сообщения Telegram-пользователям, которые не активировали промокод.

    Эта функция использует библиотеки `telebot` и `sqlite3` для взаимодействия с Telegram-ботом и локальной базой данных SQLite. 
    Она извлекает список пользователей из таблицы `users_data_table`, у которых не активирован промокод (`promocode != 1`). 
    Для каждого пользователя функция пытается отправить рекламное сообщение с описанием преимуществ тарифа PRO и инструкциями по 
    активации промокода `FREE24`. Если сообщение отправлено успешно, она записывает в журнал ID пользователя с "yes"; 
    в противном случае - с "no".

    Raises:
        Exception: Если возникает ошибка при отправке сообщения.
    """
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
            bot.send_message(chat_id=us[0], text="Успейте воспользоваться промокодом FREE24 до 21 декабря!\\n\\nПо нему вы получите бесплатный месяц тарифа PRO — это безлимит на генерацию текста и изображений 💥 \\n\\nЧтобы ввести промокод, перейдите на вкладку Тарифы и нажмите кнопку «Промокод».", parse_mode='html')
        except:
            print(us[0], "no")
        else:
            print(us[0], "yes")
```

## Parameter Details

- `chat_id` (int): ID пользователя Telegram, которому отправляется сообщение.
- `text` (str): Текст сообщения, отправляемого пользователю.
- `parse_mode` (str, optional): Формат парсинга текста. По умолчанию `None`.

## Examples

```python
# Пример вызова функции send_promo_messages():
send_promo_messages()
```

## How the Function Works

1. **Import Libraries:** Imports the necessary libraries: `telebot`, `sqlite3`, and `os`.
2. **Load Environment Variables:** Loads environment variables from a `.env` file using the `load_dotenv()` function. This is assumed to contain the Telegram bot token.
3. **Initialize Telegram Bot:** Creates a `TeleBot` instance using the loaded bot token.
4. **Connect to Database:** Establishes a connection to the `UsersData.db` SQLite database.
5. **Retrieve Users:** Executes an SQL query to select user IDs from the `users_data_table` where the `promocode` field is not equal to 1 (meaning the promocode is not activated).
6. **Iterate through Users:** Loops through the retrieved user IDs.
7. **Send Message:** Attempts to send a promotional message to each user using the `bot.send_message()` function.
8. **Log Results:** Prints the user ID and "yes" if the message was sent successfully or "no" if an error occurred.

## Principle of Operation

The function iterates through a list of Telegram users who have not yet activated a promocode. For each user, it attempts to send a promotional message. The success or failure of each message is logged.

## Conclusion

This module is a simple yet effective way to send targeted promotional messages to Telegram users. It relies on the `telebot` library for interaction with Telegram and `sqlite3` for database access. The code is well-structured and easy to understand.