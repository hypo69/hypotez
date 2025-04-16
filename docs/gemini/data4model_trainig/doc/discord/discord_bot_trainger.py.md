## \\file /src/bots/openai_bots/telegram_bot_trainger.py

# Модуль Telegram-бота для обучения и взаимодействия с моделью OpenAI

```rst
.. module:: src.bots.openai_bots
    :platform: Windows, Unix
    :synopsis: Telegram-бот, использующий OpenAI для обработки текста и голоса, а также для обучения на основе документов.

```

Этот скрипт создает простого Telegram-бота, использующего библиотеку python-telegram-bot.

## Обзор

Модуль `src.bots.openai_bots.telegram_bot_trainger.py` создает Telegram-бота, который может обрабатывать текстовые и голосовые сообщения, а также обучаться на основе загруженных документов, используя OpenAI.

## Подробней

Модуль предоставляет функциональность для взаимодействия с пользователями через Telegram, включая ответы на текстовые и голосовые сообщения, а также обучение модели на основе загруженных документов.

## Функции

### `on_ready`

```python
@bot.event
async def on_ready():
    """Called when the bot is ready."""
    logger.info(f'Logged in as {bot.user}')
```

**Назначение**: Вызывается, когда бот готов к работе.

**Как работает функция**:

1.  Логирует информацию об успешном входе в систему.

### `hi`

```python
@bot.command(name='hi')
async def hi(ctx):
    """Welcome message."""
    logger.info(f'hi({ctx})')
    await ctx.send('HI!')
    return True
```

**Назначение**: Обрабатывает команду `!hi`.

**Как работает функция**:

1.  Логирует информацию о вызове команды.
2.  Отправляет приветственное сообщение.

### `join`

```python
@bot.command(name='join')
async def join(ctx):
    """Connect the bot to the voice channel."""
    logger.info(f'join({ctx})')
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f'Joined {channel}')
    else:
        await ctx.send('You are not in a voice channel.')
```

**Назначение**: Подключает бота к голосовому каналу.

**Как работает функция**:

1.  Логирует информацию о вызове команды.
2.  Если автор сообщения находится в голосовом канале, подключает бота к этому каналу и отправляет подтверждающее сообщение.
3.  Если автор не находится в голосовом канале, отправляет сообщение об ошибке.

### `leave`

```python
@bot.command(name='leave')
async def leave(ctx):
    """Disconnect the bot from the voice channel."""
    logger.info(f'leave({ctx})')
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send('Disconnected from the voice channel.')
    else:
        await ctx.send('I am not in a voice channel.')
```

**Назначение**: Отключает бота от голосового канала.

**Как работает функция**:

1.  Логирует информацию о вызове команды.
2.  Если бот находится в голосовом канале, отключает его и отправляет подтверждающее сообщение.
3.  Если бот не находится в голосовом канале, отправляет сообщение об ошибке.

### `train`

```python
@bot.command(name='train')
async def train(ctx, data: str = None, data_dir: str = None, positive: bool = True, attachment: discord.Attachment = None):
    """Train the model with the provided data."""
    logger.info(f'train({ctx})')
    if attachment:
        file_path = f"/tmp/{attachment.filename}"
        await attachment.save(file_path)
        data = file_path

    job_id = model.train(data, data_dir, positive)
    if job_id:
        await ctx.send(f'Model training started. Job ID: {job_id}')
        model.save_job_id(job_id, "Training task started")
    else:
        await ctx.send('Failed to start training.')
```

**Назначение**: Обучает модель на основе предоставленных данных.

**Параметры**:

*   `ctx`: Контекст команды.
*   `data` (str, optional): Текстовые данные для обучения. По умолчанию `None`.
*   `data_dir` (str, optional): Путь к каталогу с данными для обучения. По умолчанию `None`.
*   `positive` (bool, optional): Указывает, являются ли данные положительными или отрицательными. По умолчанию `True`.
*   `attachment` (discord.Attachment, optional): Файл для обучения. По умолчанию `None`.

**Как работает функция**:

1.  Логирует информацию о вызове команды.
2.  Если предоставлен файл, сохраняет его локально и использует его содержимое для обучения.
3.  Запускает обучение модели, используя метод `model.train`.
4.  Отправляет пользователю сообщение с ID задачи обучения.

### `test`

```python
@bot.command(name='test')
async def test(ctx, test_data: str):
    """Test the model with the provided test data."""
    logger.info(f'test({ctx})')
    try:
        test_data = j_loads(test_data)
        predictions = model.predict(test_data)
        if predictions:
            await ctx.send(f'Test complete. Predictions: {predictions}')
            model.handle_errors(predictions, test_data)
        else:
            await ctx.send('Failed to get predictions.')
    except json.JSONDecodeError:
        await ctx.send('Invalid test data format. Please provide a valid JSON string.')
```

**Назначение**: Тестирует модель на основе предоставленных тестовых данных.

**Параметры**:

*   `ctx`: Контекст команды.
*   `test_data` (str): Тестовые данные в формате JSON.

**Как работает функция**:

1.  Логирует информацию о вызове команды.
2.  Пытается загрузить тестовые данные из JSON-строки.
3.  Выполняет тестирование модели, используя метод `model.predict`.
4.  Отправляет пользователю сообщение с результатами тестирования.

### `archive`

```python
@bot.command(name='archive')
async def archive(ctx, directory: str):
    """Archive files in the specified directory."""
    logger.info(f'archive({ctx})')
    try:
        await model.archive_files(directory)
        await ctx.send(f'Files in {directory} have been archived.')
    except Exception as ex:
        await ctx.send(f'An error occurred while archiving files: {ex}')
```

**Назначение**: Архивирует файлы в указанном каталоге.

**Параметры**:

*   `ctx`: Контекст команды.
*   `directory` (str): Путь к каталогу для архивации.

**Как работает функция**:

1.  Логирует информацию о вызове команды.
2.  Выполняет архивацию файлов, используя метод `model.archive_files`.
3.  Отправляет пользователю сообщение об успешной архивации.

### `select_dataset`

```python
@bot.command(name='select_dataset')
async def select_dataset(ctx, path_to_dir_positive: str, positive: bool = True):
    """Select a dataset for training the model."""
    logger.info(f'select_dataset({ctx})')
    dataset = await model.select_dataset_and_archive(path_to_dir_positive, positive)
    if dataset:
        await ctx.send(f'Dataset selected and archived. Dataset: {dataset}')
    else:
        await ctx.send('Failed to select dataset.')
```

**Назначение**: Выбирает набор данных для обучения модели.

**Параметры**:

*   `ctx`: Контекст команды.
*   `path_to_dir_positive` (str): Путь к каталогу с положительными данными.
*   `positive` (bool, optional): Указывает, являются ли данные положительными или отрицательными. По умолчанию `True`.

**Как работает функция**:

1.  Логирует информацию о вызове команды.
2.  Выбирает набор данных и архивирует его, используя метод `model.select_dataset_and_archive`.
3.  Отправляет пользователю сообщение об успешном выборе набора данных.

### `instruction`

```python
@bot.command(name='instruction')
async def instruction(ctx):
    """Display the instruction message from an external file."""
    logger.info(f'instruction({ctx})')
    try:
        instructions_path = Path("_docs/bot_instruction.md")
        if instructions_path.exists():
            with instructions_path.open("r") as file:
                instructions = file.read()
            await ctx.send(instructions)
        else:
            await ctx.send('Instructions file not found.')
    except Exception as ex:
        await ctx.send(f'An error occurred while reading the instructions: {ex}')
```

**Назначение**: Отображает сообщение с инструкциями из внешнего файла.

**Параметры**:

*   `ctx`: Контекст команды.

**Как работает функция**:

1.  Логирует информацию о вызове команды.
2.  Пытается прочитать содержимое файла `_docs/bot_instruction.md`.
3.  Отправляет содержимое файла пользователю.

### `correct`

```python
@bot.command(name='correct')
async def correct(ctx, message_id: int, *, correction: str):
    """Correct a previous response by providing the message ID and the correction."""
    logger.info(f'correct({ctx})')
    try:
        message = await ctx.fetch_message(message_id)
        if message:
            # Log or store the correction
            logger.info(f"Correction for message ID {message_id}: {correction}")
            store_correction(message.content, correction)
            await ctx.send(f"Correction received: {correction}")
        else:
            await ctx.send("Message not found.")
    except Exception as ex:
        await ctx.send(f'An error occurred: {ex}')
```

**Назначение**: Исправляет предыдущий ответ бота, предоставляя ID сообщения и исправление.

**Параметры**:

*   `ctx`: Контекст команды.
*   `message_id` (int): ID сообщения, которое нужно исправить.
*   `correction` (str): Текст исправления.

**Как работает функция**:

1.  Логирует информацию о вызове команды.
2.  Пытается получить сообщение по ID.
3.  Если сообщение найдено, сохраняет исправление и отправляет подтверждающее сообщение пользователю.

### `store_correction`

```python
def store_correction(original_text: str, correction: str):
    """Store the correction for future reference or retraining."""
    logger.info('store_correction()')
    correction_file = Path("corrections_log.txt")
    with correction_file.open("a") as file:
        file.write(f"Original: {original_text}\\nCorrection: {correction}\\n\\n")
```

**Назначение**: Сохраняет исправление для будущего использования или переобучения.

**Параметры**:

*   `original_text` (str): Оригинальный текст сообщения.
*   `correction` (str): Текст исправления.

**Как работает функция**:

1.  Логирует информацию о вызове функции.
2.  Записывает оригинальный текст и исправление в файл `corrections_log.txt`.

### `feedback`

```python
@bot.command(name='feedback')
async def feedback(ctx, *, feedback_text: str):
    """Submit feedback about the model's response."""
    logger.info(f'feedback({ctx})')
    store_correction("Feedback", feedback_text)
    await ctx.send('Thank you for your feedback. We will use it to improve the model.')
```

**Назначение**: Сохраняет отзыв о работе модели.

**Параметры**:

*   `ctx`: Контекст команды.
*   `feedback_text` (str): Текст отзыва.

**Как работает функция**:

1.  Логирует информацию о вызове команды.
2.  Сохраняет отзыв, используя функцию `store_correction`.
3.  Отправляет пользователю сообщение благодарности за отзыв.

### `getfile`

```python
@bot.command(name='getfile')
async def getfile(ctx, file_path: str):
    """Attach a file from the given path."""
    logger.info(f'getfile({ctx})')
    file_to_attach = Path(file_path)
    if file_to_attach.exists():
        await ctx.send("Here is the file you requested:", file=discord.File(file_to_attach))
    else:
        await ctx.send(f'File not found: {file_path}')
```

**Назначение**: Отправляет файл из указанного пути.

**Параметры**:

*   `ctx`: Контекст команды.
*   `file_path` (str): Путь к файлу.

**Как работает функция**:

1.  Логирует информацию о вызове команды.
2.  Проверяет, существует ли файл по указанному пути.
3.  Если файл существует, отправляет его пользователю.
4.  Если файл не существует, отправляет сообщение об ошибке.

### `text_to_speech_and_play`

```python
async def text_to_speech_and_play(text, channel):
    """Convert text to speech and play it in a voice channel."""
    tts = gTTS(text=text, lang='ru')  # Замените 'ru' на нужный язык
    audio_file_path = f"{tempfile.gettempdir()}/response.mp3"  # Путь к временно созданному файлу
    tts.save(audio_file_path)  # Сохраняем аудиофайл

    voice_channel = channel.guild.voice_client
    if not voice_channel:
        voice_channel = await channel.connect()  # Подключаемся к голосовому каналу

    voice_channel.play(discord.FFmpegPCMAudio(audio_file_path), after=lambda ex: logger.info(f'Finished playing: {ex}'))

    while voice_channel.is_playing():  # Ждем пока играет звук
        await asyncio.sleep(1)

    await voice_channel.disconnect()  # Отключаемся
```

**Назначение**: Преобразует текст в речь и воспроизводит его в голосовом канале.

**Параметры**:

*   `text`: Текст для преобразования в речь.
*   `channel`: Голосовой канал, в котором нужно воспроизвести речь.

**Как работает функция**:

1.  Преобразует текст в речь с помощью библиотеки `gTTS`.
2.  Сохраняет аудиофайл во временный файл.
3.  Подключается к голосовому каналу (если еще не подключен).
4.  Воспроизводит аудиофайл в голосовом канале.
5.  Отключается от голосового канала после завершения воспроизведения.

### `on_message`

```python
@bot.event
async def on_message(message):
    """Handle incoming messages and respond to voice commands."""
    #logger.info(f'on_message({message})')
    if message.author == bot.user:
        return  # Игнорируем сообщения от самого себя

    if message.content.startswith(PREFIX):
        await bot.process_commands(message)
        return  # Обрабатываем команды

    if message.attachments:
        # Check if it\'s an audio attachment
        if message.attachments[0].content_type.startswith(\'audio/\'):
            recognized_text = recognizer(message.attachments[0].url)
            #await message.channel.send(recognized_text)
            response = model.send_message(recognized_text)

    else:
        response = model.send_message(message.content)
    if message.author.voice:
        # Если пользователь находится в голосовом канале, подключаемся и воспроизводим ответ
        await text_to_speech_and_play(response, message.author.voice.channel)
    else:
        await message.channel.send(response)  # Отправляем ответ в текстовый канал
```

**Назначение**: Обрабатывает входящие сообщения и отвечает на голосовые команды.

**Параметры**:

*   `message`: Объект сообщения Discord.

**Как работает функция**:

1.  Игнорирует сообщения от самого себя.
2.  Если сообщение начинается с префикса команды, обрабатывает команду, используя `bot.process_commands`.
3.  Если сообщение содержит аудиофайл, распознает речь из аудио и отправляет распознанный текст в модель.
4.  Иначе отправляет текстовое содержимое сообщения в модель.
5.  Воспроизводит ответ модели в голосовом канале, если пользователь находится в нем, иначе отправляет ответ в текстовый канал.

### `main`

```python
if __name__ == "__main__":
    bot.run(gs.credentials.discord.bot_token)
```

**Назначение**: Запускает Discord-бота.

**Как работает функция**:

1.  Получает токен бота из `gs.credentials.discord.bot_token`.
2.  Запускает бота, используя метод `bot.run`.

## Использование

Для запуска бота необходимо:

1.  Установить необходимые библиотеки, указанные в `requirements.txt`.
2.  Заменить `gs.credentials.discord.bot_token` на реальный токен Discord-бота в файле `src/bots/openai_bots/telegram_bot_trainger.py`.
3.  Запустить файл `discord_bot_trainger.py`.

После запуска бот будет доступен на сервере Discord, и пользователи смогут взаимодействовать с ним, отправляя команды, текстовые и голосовые сообщения, а также документы.