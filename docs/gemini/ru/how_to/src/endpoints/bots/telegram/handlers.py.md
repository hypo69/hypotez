### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код содержит класс `BotHandler`, который обрабатывает различные команды и сообщения, отправленные через Telegram-бота. Он включает в себя обработку URL-адресов, текстовых сообщений, голосовых сообщений, документов и команд, таких как `/start`, `/help` и `/sendpdf`.

Шаги выполнения
-------------------------
1. **Инициализация `BotHandler`**:
   - Создается экземпляр класса `BotHandler`.
   - В конструкторе происходит инициализация необходимых параметров.
     ```python
     handler = BotHandler()
     ```

2. **Обработка URL**:
   - Метод `handle_url` обрабатывает URL-адреса, отправленные пользователем.
   - Вызывает соответствующие функции для обработки URL.
     ```python
     await handler.handle_url(update, context)
     ```

3. **Обработка текстовых сообщений**:
   - Метод `handle_message` обрабатывает любые текстовые сообщения, отправленные пользователем.
   - Логирует полученное сообщение и отвечает пользователю.
     ```python
     await handler.handle_message(update, context)
     ```

4. **Обработка команды `/start`**:
   - Метод `start` обрабатывает команду `/start`.
   - Отвечает пользователю приветственным сообщением.
     ```python
     await handler.start(update, context)
     ```

5. **Обработка команды `/help`**:
   - Метод `help_command` обрабатывает команду `/help`.
   - Отвечает пользователю списком доступных команд.
     ```python
     await handler.help_command(update, context)
     ```

6. **Обработка команды `/sendpdf`**:
   - Метод `send_pdf` обрабатывает команду `/sendpdf`.
   - Отправляет пользователю PDF-файл.
   - Обрабатывает возможные ошибки при отправке файла.
     ```python
     await handler.send_pdf(update, context)
     ```

7. **Обработка голосовых сообщений**:
   - Метод `handle_voice` обрабатывает голосовые сообщения, отправленные пользователем.
   - Получает файл голосового сообщения, скачивает его и транскрибирует текст.
   - Отвечает пользователю распознанным текстом.
     ```python
     await handler.handle_voice(update, context)
     ```

8. **Обработка документов**:
   - Метод `handle_document` обрабатывает документы, отправленные пользователем.
   - Получает файл документа, скачивает его и сохраняет локально.
   - Отвечает пользователю сообщением об успешном сохранении файла.
     ```python
     await handler.handle_document(update, context)
     ```

9. **Обработка логов**:
   - Метод `handle_log` обрабатывает логи, отправленные пользователем.
   - Логирует полученное сообщение и отвечает пользователю.
     ```python
     await handler.handle_log(update, context)
     ```

Пример использования
-------------------------

```python
from telegram import Update
from telegram.ext import CallbackContext
from src.endpoints.bots.telegram.handlers import BotHandler

# Пример использования BotHandler для обработки команды /start
async def start_command(update: Update, context: CallbackContext):
    handler = BotHandler()
    await handler.start(update, context)

# Пример использования BotHandler для обработки текстового сообщения
async def text_message(update: Update, context: CallbackContext):
    handler = BotHandler()
    await handler.handle_message(update, context)