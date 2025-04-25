# Модуль OnelaBot
## Обзор

Модуль для взаимодействия с моделью ассистента программиста через чат Telegram.

Модуль содержит класс :class:`OnelaBot`, который используется для обработки текстовых сообщений и документов. 
## Классы
### `OnelaBot`
**Описание**: Взаимодействие с моделью ассистента программиста.

**Наследует**: :class:`TelegramBot`

**Атрибуты**:

- `model` (:class:`GoogleGenerativeAi`): Модель, используемая для обработки запросов. 

**Методы**:
- `__init__()`: Инициализация объекта OnelaBot.
- `handle_message(update: Update, context: CallbackContext)`: Обработка текстовых сообщений.
- `handle_document(update: Update, context: CallbackContext)`: Обработка загруженных документов.
## Функции
### `__main__`
**Назначение**: Точка входа в скрипт.

**Как работает функция**:
- Создает объект класса :class:`OnelaBot`.
- Запускает Telegram-бота в режиме опроса (polling).

**Примеры**:
- `bot = OnelaBot()` - создание объекта Telegram-бота.
- `asyncio.run(bot.application.run_polling())` - запуск бота в режиме опроса.


## Методы класса
### `__init__`
```python
    def __init__(self) -> None:
        """
        Инициализация объекта OnelaBot.
        """
        super().__init__(gs.credentials.telegram.onela_bot)
```
**Назначение**: Инициализация объекта OnelaBot.
**Параметры**:
- `self` (OnelaBot): Объект класса OnelaBot.
**Возвращает**:
- `None`

**Как работает функция**:
- Вызывает метод инициализации базового класса :class:`TelegramBot`, передавая в него токен доступа для Telegram-бота.

### `handle_message`
```python
    async def handle_message(self, update: Update, context: CallbackContext) -> None:
        """
        Обработка текстовых сообщений.

        Args:
            update (Update): Данные обновления Telegram.
            context (CallbackContext): Контекст выполнения.
        """
        q: str = update.message.text
        user_id: int = update.effective_user.id
        try:
            # Получение ответа от модели
            answer: str = await self.model.chat(q)
            await update.message.reply_text(answer)
        except Exception as ex:
            logger.error('Ошибка обработки текстового сообщения: ', ex)
            ...
```
**Назначение**: Обработка текстовых сообщений, полученных от пользователя.
**Параметры**:
- `self` (OnelaBot): Объект класса OnelaBot.
- `update` (:class:`Update`): Данные обновления Telegram.
- `context` (:class:`CallbackContext`): Контекст выполнения.
**Возвращает**:
- `None`

**Как работает функция**:
- Извлекает текст сообщения (`q`) и ID пользователя (`user_id`) из обновления Telegram.
- Вызывает метод `chat` модели ассистента (`self.model.chat(q)`) для получения ответа на заданный вопрос (`q`).
- Отправляет ответ модели (`answer`) пользователю в Telegram-чат.
- В случае ошибки логирует её с помощью `logger`.

### `handle_document`
```python
    async def handle_document(self, update: Update, context: CallbackContext) -> None:
        """
        Обработка загруженных документов.

        Args:
            update (Update): Данные обновления Telegram.
            context (CallbackContext): Контекст выполнения.
        """
        try:
            file = await update.message.document.get_file()
            tmp_file_path: Path = await file.download_to_drive()  # Сохранение файла локально
            answer: str = await update.message.reply_text(file)
            update.message.reply_text(answer)
        except Exception as ex:
            logger.error('Ошибка обработки документа: ', ex)
            ...
```
**Назначение**: Обработка документов, загруженных пользователем в Telegram-чат.

**Параметры**:
- `self` (OnelaBot): Объект класса OnelaBot.
- `update` (:class:`Update`): Данные обновления Telegram.
- `context` (:class:`CallbackContext`): Контекст выполнения.

**Возвращает**:
- `None`

**Как работает функция**:
- Извлекает файл документа из обновления Telegram.
- Сохраняет файл локально на диск.
- Отправляет пользователю сообщение о получении файла. 
- В случае ошибки логирует её с помощью `logger`.