# Документация модуля discord_bot_trainger

## Обзор

Модуль `discord_bot_trainger.py` предназначен для создания Discord-бота, способного выполнять различные задачи, такие как приветствие пользователей, подключение к голосовым каналам, обучение модели машинного обучения, тестирование модели, архивирование файлов и отправка инструкций. Бот также обрабатывает голосовые команды и текстовые сообщения, взаимодействуя с пользователями через текстовые и голосовые каналы.

## Подробнее

Этот модуль является основным компонентом Discord-бота в проекте `hypotez`. Он использует библиотеку `discord.py` для интеграции с Discord, а также другие библиотеки, такие как `speech_recognition`, `pydub`, `gTTS` и `requests`, для обработки аудио и выполнения других задач. Модуль содержит обработчики команд, позволяющие пользователям взаимодействовать с ботом, а также логику для обучения и тестирования моделей машинного обучения.

## Классы

В данном модуле классы не определены.

## Функции

### `on_ready`

```python
@bot.event
async def on_ready():
    """Called when the bot is ready."""
    logger.info(f'Logged in as {bot.user}')
```

**Назначение**:
Функция вызывается, когда бот Discord успешно подключился и готов к работе.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
- Функция регистрирует информацию о том, что бот вошел в систему, используя объект `bot.user`.

**Примеры**:
```python
# Пример использования:
# Бот автоматически вызывает эту функцию при успешном подключении.
```

### `hi`

```python
@bot.command(name='hi')
async def hi(ctx):
    """Welcome message."""
    logger.info(f'hi({ctx})')
    await ctx.send('HI!')
    return True
```

**Назначение**:
Функция отправляет приветственное сообщение в текстовый канал, где была вызвана команда `!hi`.

**Параметры**:
- `ctx` (discord.ext.commands.Context): Контекст команды, содержащий информацию о канале, пользователе и сервере.

**Возвращает**:
- `bool`: Возвращает `True` после отправки приветственного сообщения.

**Как работает функция**:
- Функция отправляет приветственное сообщение "HI!" в канал, из которого была вызвана команда.

**Примеры**:
```python
# Пример использования:
# Пользователь вводит команду !hi в текстовом канале.
```

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

**Назначение**:
Функция подключает бота к голосовому каналу, в котором находится автор команды.

**Параметры**:
- `ctx` (discord.ext.commands.Context): Контекст команды, содержащий информацию о канале, пользователе и сервере.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
- Функция проверяет, находится ли автор команды в голосовом канале.
- Если автор находится в голосовом канале, бот подключается к этому каналу и отправляет сообщение об успешном подключении.
- Если автор не находится в голосовом канале, бот отправляет сообщение об ошибке.

**Примеры**:
```python
# Пример использования:
# Пользователь вводит команду !join, находясь в голосовом канале.
```

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

**Назначение**:
Функция отключает бота от голосового канала.

**Параметры**:
- `ctx` (discord.ext.commands.Context): Контекст команды, содержащий информацию о канале, пользователе и сервере.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
- Функция проверяет, подключен ли бот к голосовому каналу.
- Если бот подключен к голосовому каналу, он отключается от него и отправляет сообщение об успешном отключении.
- Если бот не подключен к голосовому каналу, он отправляет сообщение об ошибке.

**Примеры**:
```python
# Пример использования:
# Пользователь вводит команду !leave, когда бот находится в голосовом канале.
```

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

**Назначение**:
Функция запускает обучение модели с использованием предоставленных данных.

**Параметры**:
- `ctx` (discord.ext.commands.Context): Контекст команды, содержащий информацию о канале, пользователе и сервере.
- `data` (str, optional): Текстовые данные для обучения модели. По умолчанию `None`.
- `data_dir` (str, optional): Путь к каталогу с данными для обучения модели. По умолчанию `None`.
- `positive` (bool, optional): Указывает, являются ли предоставленные данные положительными. По умолчанию `True`.
- `attachment` (discord.Attachment, optional): Файл, прикрепленный к сообщению, содержащий данные для обучения. По умолчанию `None`.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
1. Функция проверяет, есть ли прикрепленный файл. Если файл есть, он сохраняется во временный каталог `/tmp` и путь к файлу используется в качестве данных для обучения.
2. Функция вызывает метод `model.train()` для запуска обучения модели с использованием предоставленных данных.
3. Если обучение успешно запущено, функция отправляет сообщение с идентификатором задачи (Job ID).
4. Если запуск обучения не удался, функция отправляет сообщение об ошибке.

**Примеры**:
```python
# Пример использования:
# Пользователь вводит команду !train с текстовыми данными.
# Пользователь вводит команду !train с прикрепленным файлом.
```

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

**Назначение**:
Функция выполняет тестирование модели с использованием предоставленных тестовых данных.

**Параметры**:
- `ctx` (discord.ext.commands.Context): Контекст команды, содержащий информацию о канале, пользователе и сервере.
- `test_data` (str): Тестовые данные в формате JSON.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
1. Функция пытается загрузить тестовые данные из строки JSON с использованием `j_loads`.
2. Функция вызывает метод `model.predict()` для получения предсказаний модели на основе тестовых данных.
3. Если предсказания получены успешно, функция отправляет сообщение с результатами тестирования и передает предсказания и тестовые данные в метод `model.handle_errors()`.
4. Если не удалось получить предсказания, функция отправляет сообщение об ошибке.
5. Если тестовые данные имеют неверный формат JSON, функция отправляет сообщение об ошибке.

**Примеры**:
```python
# Пример использования:
# Пользователь вводит команду !test с тестовыми данными в формате JSON.
```

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

**Назначение**:
Функция архивирует файлы в указанном каталоге.

**Параметры**:
- `ctx` (discord.ext.commands.Context): Контекст команды, содержащий информацию о канале, пользователе и сервере.
- `directory` (str): Путь к каталогу, который нужно архивировать.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
1. Функция вызывает метод `model.archive_files()` для выполнения архивации файлов в указанном каталоге.
2. Если архивация выполнена успешно, функция отправляет сообщение об успешном завершении операции.
3. Если во время архивации произошла ошибка, функция отправляет сообщение об ошибке.

**Примеры**:
```python
# Пример использования:
# Пользователь вводит команду !archive с указанием каталога для архивации.
```

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

**Назначение**:
Функция выбирает набор данных для обучения модели и архивирует его.

**Параметры**:
- `ctx` (discord.ext.commands.Context): Контекст команды, содержащий информацию о канале, пользователе и сервере.
- `path_to_dir_positive` (str): Путь к каталогу с положительными данными для обучения.
- `positive` (bool, optional): Указывает, являются ли данные положительными. По умолчанию `True`.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
1. Функция вызывает метод `model.select_dataset_and_archive()` для выбора и архивации набора данных.
2. Если выбор и архивация выполнены успешно, функция отправляет сообщение об успешном завершении операции и названии выбранного набора данных.
3. Если не удалось выбрать набор данных, функция отправляет сообщение об ошибке.

**Примеры**:
```python
# Пример использования:
# Пользователь вводит команду !select_dataset с указанием пути к каталогу с данными.
```

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

**Назначение**:
Функция отображает инструкцию из внешнего файла.

**Параметры**:
- `ctx` (discord.ext.commands.Context): Контекст команды, содержащий информацию о канале, пользователе и сервере.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
1. Функция пытается прочитать содержимое файла `_docs/bot_instruction.md`.
2. Если файл существует, его содержимое отправляется в канал Discord.
3. Если файл не существует, отправляется сообщение об ошибке.
4. Если во время чтения файла произошла ошибка, отправляется сообщение об ошибке.

**Примеры**:
```python
# Пример использования:
# Пользователь вводит команду !instruction.
```

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

**Назначение**:
Функция позволяет исправить предыдущий ответ бота, указывая ID сообщения и текст исправления.

**Параметры**:
- `ctx` (discord.ext.commands.Context): Контекст команды, содержащий информацию о канале, пользователе и сервере.
- `message_id` (int): ID сообщения, которое нужно исправить.
- `correction` (str): Текст исправления.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
1. Функция пытается получить сообщение с указанным ID из канала Discord.
2. Если сообщение найдено, функция сохраняет исправление, логирует его и отправляет подтверждение пользователю.
3. Если сообщение не найдено, отправляется сообщение об ошибке.
4. Если во время выполнения произошла ошибка, отправляется сообщение об ошибке.

**Примеры**:
```python
# Пример использования:
# Пользователь вводит команду !correct 1234567890 Текст исправления.
```

### `store_correction`

```python
def store_correction(original_text: str, correction: str):
    """Store the correction for future reference or retraining."""
    logger.info('store_correction()')
    correction_file = Path("corrections_log.txt")
    with correction_file.open("a") as file:
        file.write(f"Original: {original_text}\\nCorrection: {correction}\\n\\n")
```

**Назначение**:
Функция сохраняет исправление для дальнейшего использования или переобучения модели.

**Параметры**:
- `original_text` (str): Оригинальный текст сообщения.
- `correction` (str): Текст исправления.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
1. Функция записывает оригинальный текст и текст исправления в файл `corrections_log.txt`.

**Примеры**:
```python
# Пример использования:
# store_correction("Привет", "Здравствуйте");
```

### `feedback`

```python
@bot.command(name='feedback')
async def feedback(ctx, *, feedback_text: str):
    """Submit feedback about the model's response."""
    logger.info(f'feedback({ctx})')
    store_correction("Feedback", feedback_text)
    await ctx.send('Thank you for your feedback. We will use it to improve the model.')
```

**Назначение**:
Функция позволяет отправить отзыв о ответе модели.

**Параметры**:
- `ctx` (discord.ext.commands.Context): Контекст команды, содержащий информацию о канале, пользователе и сервере.
- `feedback_text` (str): Текст отзыва.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
1. Функция сохраняет отзыв с помощью функции `store_correction`.
2. Функция отправляет сообщение благодарности пользователю за отзыв.

**Примеры**:
```python
# Пример использования:
# Пользователь вводит команду !feedback Мне не понравился ответ модели.
```

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

**Назначение**:
Функция отправляет файл из указанного пути в канал Discord.

**Параметры**:
- `ctx` (discord.ext.commands.Context): Контекст команды, содержащий информацию о канале, пользователе и сервере.
- `file_path` (str): Путь к файлу, который нужно отправить.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
1. Функция проверяет, существует ли файл по указанному пути.
2. Если файл существует, он отправляется в канал Discord.
3. Если файл не существует, отправляется сообщение об ошибке.

**Примеры**:
```python
# Пример использования:
# Пользователь вводит команду !getfile /path/to/file.txt
```

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

**Назначение**:
Функция преобразует текст в речь и воспроизводит его в голосовом канале.

**Параметры**:
- `text` (str): Текст, который нужно преобразовать в речь.
- `channel` (discord.VoiceChannel): Голосовой канал, в котором нужно воспроизвести речь.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
1. Функция использует библиотеку `gTTS` для преобразования текста в речь.
2. Функция сохраняет аудиофайл во временном каталоге.
3. Функция подключается к голосовому каналу, если бот еще не подключен.
4. Функция воспроизводит аудиофайл в голосовом канале.
5. Функция ждет окончания воспроизведения.
6. Функция отключается от голосового канала.

**Примеры**:
```python
# Пример использования:
# await text_to_speech_and_play("Привет, мир!", voice_channel);
```

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
```

**Назначение**:
Функция обрабатывает входящие сообщения и отвечает на голосовые команды.

**Параметры**:
- `message` (discord.Message): Объект сообщения, содержащий информацию об авторе, содержимом и канале сообщения.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
1. Функция игнорирует сообщения, отправленные самим ботом.
2. Если сообщение начинается с префикса команды, функция обрабатывает команду с помощью `bot.process_commands()`.
3. Если к сообщению прикреплены файлы, функция проверяет, является ли один из файлов аудиофайлом. Если это так, функция распознает речь в аудиофайле и отправляет распознанный текст в модель для получения ответа.
4. Если к сообщению нет прикрепленных файлов, функция отправляет содержимое сообщения в модель для получения ответа.
5. Если автор сообщения находится в голосовом канале, функция преобразует ответ в речь и воспроизводит его в голосовом канале.
6. В противном случае функция отправляет ответ в текстовый канал.

**Примеры**:
```python
# Пример использования:
# Пользователь отправляет текстовое сообщение в канал.
# Пользователь отправляет аудиофайл в канал.