## Как использовать `BotHandler` в проекте
=========================================================================================

Описание
-------------------------
`BotHandler` - класс, реализующий обработку различных типов сообщений в Telegram-боте.

Шаги выполнения
-------------------------
1. Создается экземпляр класса `BotHandler`, инициализируя сценарий (`Scenario`), модель (`GoogleGenerativeAi`) и список вопросов (`questions_list`).
2. Определяются методы для обработки разных типов сообщений:
    - `handle_message`:  обрабатывает текстовые сообщения, определяет тип сообщения и вызывает соответствующий метод.
    - `_send_user_flowchart`: отправляет схему user_flowchart.
    - `_handle_url`: обрабатывает URL, отправленный пользователем.
    - `_handle_next_command`: обрабатывает команду '--next' и ее аналоги.
    - `help_command`: обрабатывает команду '/help'.
    - `send_pdf`: отправляет PDF-файл.
    - `handle_voice`: обрабатывает голосовые сообщения.
    - `_transcribe_voice`: транскрибирует голосовое сообщение (заглушка).
    - `handle_document`: обрабатывает полученные документы.
3. Используя `telebot` обработчик событий  `bot.message_handler` определяет обработку команд `/start`, `/help`, `/info`, `/time`, `/photo`. 
4. Используя `telebot` обработчик событий  `bot.message_handler` определяет обработку голосовых сообщений `content_types=[\'voice\']` и полученных документов `content_types=[\'document\']`
5. Используя `telebot` обработчик событий  `bot.message_handler` определяет обработку текстовых сообщений `func=lambda message: message.text and not message.text.startswith('/')`
6. Используя `telebot` обработчик событий  `bot.message_handler` определяет обработку текстовых сообщений, начинающихся с "/"  `func=lambda message: message.text and message.text.startswith('/')` 
7. Запускается бот с помощью `bot.polling(none_stop=True)`.

Пример использования
-------------------------
```python
# Создаем экземпляр обработчика
handler = BotHandler()

# Обрабатываем полученное текстовое сообщение
handler.handle_message(bot, message)

# Обрабатываем команду '/help'
handler.help_command(bot, message)

# Отправляем PDF-файл
handler.send_pdf(bot, message, pdf_file)

# Обрабатываем голосовое сообщение
handler.handle_voice(bot, message)

# Обрабатываем полученный документ
handler.handle_document(bot, message)
```