# Модуль `discord_bot_trainger`

## Обзор

Модуль `discord_bot_trainger` представляет собой Discord-бота, который обучает и тестирует модель обработки естественного языка (НЛП), используя данные, предоставленные пользователем. Бот позволяет загружать данные, управлять процессом обучения модели, тестировать ее производительность и предоставлять обратную связь.

## Подробнее

Этот файл содержит код для Discord-бота, который взаимодействует с пользователем и выполняет следующие задачи:

- **Обучение модели**: Бот позволяет пользователю загрузить данные для обучения модели, выбрать положительный или отрицательный набор данных и запустить процесс обучения.
- **Тестирование модели**: После обучения модель можно проверить, используя тестовые данные. Бот выводит результаты прогнозирования модели.
- **Архивирование данных**: Бот может архивировать файлы и данные, используемые для обучения и тестирования.
- **Выбор набора данных**: Бот позволяет пользователю выбрать и загрузить набор данных для обучения.
- **Инструкции**: Бот может отобразить инструкции по использованию модели.
- **Исправление ошибок**: Бот позволяет пользователю исправить предыдущие ответы модели, предоставляя  ID сообщения и исправление.
- **Обратная связь**: Бот позволяет пользователю отправить обратную связь по поводу ответов модели.
- **Файлы**: Бот может отправлять файлы из указанного пути.
- **Распознавание речи**: Бот может загрузить и распознать аудиофайлы, превращая их в текст.
- **Текстовое воспроизведение**: Бот может преобразовать текст в речь и воспроизвести его в голосовом канале.
- **Обработка сообщений**: Бот обрабатывает входящие сообщения, реагирует на команды и отвечает на запросы пользователя.


## Классы

### `Model`

**Описание**: Класс `Model` представляет собой модель обработки естественного языка, обученная на предоставленных данных.

**Атрибуты**:

- `model_name` (str): Название модели НЛП.
- `model_type` (str): Тип модели НЛП.
- `model_params` (dict): Параметры модели НЛП.
- `training_data` (list): Список данных для обучения модели.
- `test_data` (list): Список данных для тестирования модели.

**Методы**:

- `train()`: Обучает модель с использованием предоставленных данных.
- `predict()`: Выполняет прогнозирование с использованием обученной модели.
- `save_job_id()`: Сохраняет ID задачи обучения.
- `handle_errors()`: Обрабатывает ошибки при прогнозировании.
- `archive_files()`: Архивирует файлы в указанной директории.
- `select_dataset_and_archive()`: Выбирает и архивирует набор данных для обучения.

## Функции

### `recognizer` 
**Назначение**:  Функция загружает аудиофайл и распознает речь, используя Google Speech Recognition.

**Параметры**:

- `audio_url` (str): URL-адрес аудиофайла.
- `language` (str): Язык аудиофайла. По умолчанию `ru-RU`.

**Возвращает**:

- `str`: Распознанный текст.

**Вызывает исключения**:

- `sr.UnknownValueError`: Если Google Speech Recognition не смог распознать речь.
- `sr.RequestError`: Если произошла ошибка при запросе к Google Speech Recognition.

**Пример**:

```python
audio_url = "https://example.com/audio.ogg"
recognized_text = recognizer(audio_url)
print(f"Распознанный текст: {recognized_text}")
```


### `text_to_speech_and_play`
**Назначение**: Функция преобразует текст в речь и воспроизводит его в голосовом канале.

**Параметры**:

- `text` (str): Текст для преобразования.
- `channel` (discord.VoiceChannel): Голосовой канал для воспроизведения.

**Возвращает**:

- `None`.

**Как работает функция**:

1. Создается объект `gTTS` для преобразования текста в речь на выбранном языке.
2. Сохраняется аудиофайл в временной директории.
3. Подключается к голосовому каналу, если бот еще не подключен.
4. Воспроизводится аудиофайл, используя `discord.FFmpegPCMAudio`.
5. Ожидается завершения воспроизведения аудиофайла.
6. Отключается от голосового канала.

**Пример**:

```python
text = "Привет, мир!"
channel = discord.VoiceChannel()  # Замените на нужный канал
await text_to_speech_and_play(text, channel)
```

### `store_correction`
**Назначение**: Функция записывает исправления в файл для дальнейшего использования при переобучении модели.

**Параметры**:

- `original_text` (str): Исходный текст.
- `correction` (str): Исправление.

**Возвращает**:

- `None`.

**Пример**:

```python
original_text = "Неправильный текст"
correction = "Правильный текст"
store_correction(original_text, correction)
```

## Методы класса

### `on_ready`
**Описание**: Метод вызывается, когда бот готов к работе.

**Параметры**:

- `ctx` (commands.Context): Контекст команды.

**Возвращает**:

- `None`.

**Пример**:

```python
@bot.event
async def on_ready():
    """Вызывается, когда бот готов к работе."""
    logger.info(f'Logged in as {bot.user}')
```

### `hi`
**Описание**: Метод вызывается при выполнении команды `hi`.

**Параметры**:

- `ctx` (commands.Context): Контекст команды.

**Возвращает**:

- `bool`: `True`, если команда была успешно обработана.

**Пример**:

```python
@bot.command(name='hi')
async def hi(ctx):
    """Приветственное сообщение."""
    logger.info(f'hi({ctx})')
    await ctx.send('HI!')
    return True
```

### `join`
**Описание**: Метод вызывается при выполнении команды `join`. Подключает бота к голосовому каналу.

**Параметры**:

- `ctx` (commands.Context): Контекст команды.

**Возвращает**:

- `None`.

**Пример**:

```python
@bot.command(name='join')
async def join(ctx):
    """Подключение бота к голосовому каналу."""
    logger.info(f'join({ctx})')
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f'Joined {channel}')
    else:
        await ctx.send('You are not in a voice channel.')
```

### `leave`
**Описание**: Метод вызывается при выполнении команды `leave`. Отключает бота от голосового канала.

**Параметры**:

- `ctx` (commands.Context): Контекст команды.

**Возвращает**:

- `None`.

**Пример**:

```python
@bot.command(name='leave')
async def leave(ctx):
    """Отключение бота от голосового канала."""
    logger.info(f'leave({ctx})')
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send('Disconnected from the voice channel.')
    else:
        await ctx.send('I am not in a voice channel.')
```

### `train`
**Описание**: Метод вызывается при выполнении команды `train`. Обучает модель с использованием предоставленных данных.

**Параметры**:

- `ctx` (commands.Context): Контекст команды.
- `data` (str): Путь к данным для обучения или сами данные.
- `data_dir` (str): Путь к директории с данными для обучения (если используется не один файл).
- `positive` (bool): Флаг, указывающий на то, что данные положительные.
- `attachment` (discord.Attachment): Прикрепленный файл.

**Возвращает**:

- `None`.

**Пример**:

```python
@bot.command(name='train')
async def train(ctx, data: str = None, data_dir: str = None, positive: bool = True, attachment: discord.Attachment = None):
    """Обучение модели с использованием предоставленных данных."""
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

### `test`
**Описание**: Метод вызывается при выполнении команды `test`. Тестирует модель с использованием тестовых данных.

**Параметры**:

- `ctx` (commands.Context): Контекст команды.
- `test_data` (str): Тестовые данные в формате JSON.

**Возвращает**:

- `None`.

**Пример**:

```python
@bot.command(name='test')
async def test(ctx, test_data: str):
    """Тестирование модели с использованием предоставленных тестовых данных."""
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

### `archive`
**Описание**: Метод вызывается при выполнении команды `archive`. Архивирует файлы в указанной директории.

**Параметры**:

- `ctx` (commands.Context): Контекст команды.
- `directory` (str): Путь к директории, файлы которой нужно архивировать.

**Возвращает**:

- `None`.

**Пример**:

```python
@bot.command(name='archive')
async def archive(ctx, directory: str):
    """Архивирование файлов в указанной директории."""
    logger.info(f'archive({ctx})')
    try:
        await model.archive_files(directory)
        await ctx.send(f'Files in {directory} have been archived.')
    except Exception as ex:
        await ctx.send(f'An error occurred while archiving files: {ex}')
```

### `select_dataset`
**Описание**: Метод вызывается при выполнении команды `select_dataset`. Выбирает набор данных для обучения модели.

**Параметры**:

- `ctx` (commands.Context): Контекст команды.
- `path_to_dir_positive` (str): Путь к директории с положительными данными.
- `positive` (bool): Флаг, указывающий на то, что данные положительные.

**Возвращает**:

- `None`.

**Пример**:

```python
@bot.command(name='select_dataset')
async def select_dataset(ctx, path_to_dir_positive: str, positive: bool = True):
    """Выбор набора данных для обучения модели."""
    logger.info(f'select_dataset({ctx})')
    dataset = await model.select_dataset_and_archive(path_to_dir_positive, positive)
    if dataset:
        await ctx.send(f'Dataset selected and archived. Dataset: {dataset}')
    else:
        await ctx.send('Failed to select dataset.')
```

### `instruction`
**Описание**: Метод вызывается при выполнении команды `instruction`. Отображает инструкции по использованию модели.

**Параметры**:

- `ctx` (commands.Context): Контекст команды.

**Возвращает**:

- `None`.

**Пример**:

```python
@bot.command(name='instruction')
async def instruction(ctx):
    """Отображение инструкции по использованию модели."""
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

### `correct`
**Описание**: Метод вызывается при выполнении команды `correct`. Исправляет предыдущий ответ модели, предоставляя ID сообщения и исправление.

**Параметры**:

- `ctx` (commands.Context): Контекст команды.
- `message_id` (int): ID сообщения, которое нужно исправить.
- `correction` (str): Исправление.

**Возвращает**:

- `None`.

**Пример**:

```python
@bot.command(name='correct')
async def correct(ctx, message_id: int, *, correction: str):
    """Исправление предыдущего ответа, предоставляя ID сообщения и исправление."""
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

### `feedback`
**Описание**: Метод вызывается при выполнении команды `feedback`. Отправляет обратную связь по поводу ответов модели.

**Параметры**:

- `ctx` (commands.Context): Контекст команды.
- `feedback_text` (str): Текст обратной связи.

**Возвращает**:

- `None`.

**Пример**:

```python
@bot.command(name='feedback')
async def feedback(ctx, *, feedback_text: str):
    """Отправка обратной связи по поводу ответов модели."""
    logger.info(f'feedback({ctx})')
    store_correction("Feedback", feedback_text)
    await ctx.send('Thank you for your feedback. We will use it to improve the model.')
```

### `getfile`
**Описание**: Метод вызывается при выполнении команды `getfile`. Отправляет файл из указанного пути.

**Параметры**:

- `ctx` (commands.Context): Контекст команды.
- `file_path` (str): Путь к файлу.

**Возвращает**:

- `None`.

**Пример**:

```python
@bot.command(name='getfile')
async def getfile(ctx, file_path: str):
    """Отправка файла из указанного пути."""
    logger.info(f'getfile({ctx})')
    file_to_attach = Path(file_path)
    if file_to_attach.exists():
        await ctx.send("Here is the file you requested:", file=discord.File(file_to_attach))
    else:
        await ctx.send(f'File not found: {file_path}')
```

### `on_message`
**Описание**: Метод обрабатывает входящие сообщения, реагирует на команды и отвечает на запросы пользователя.

**Параметры**:

- `message` (discord.Message): Входящее сообщение.

**Возвращает**:

- `None`.

**Пример**:

```python
@bot.event
async def on_message(message):
    """Обработка входящих сообщений и ответы на голосовые команды."""
    #logger.info(f'on_message({message})')
    if message.author == bot.user:
        return  # Игнорируем сообщения от самого себя

    if message.content.startswith(PREFIX):
        await bot.process_commands(message)
        return  # Обрабатываем команды

    if message.attachments:
        # Check if it's an audio attachment
        if message.attachments[0].content_type.startswith('audio/'):
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