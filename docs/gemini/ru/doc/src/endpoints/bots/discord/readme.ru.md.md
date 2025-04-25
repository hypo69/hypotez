# Модуль Discord-бота

## Обзор

Этот модуль реализует Discord-бота, который предоставляет функциональность для управления моделью машинного обучения, обработки аудио, 
взаимодействия с пользователями в текстовых и голосовых каналах Discord.

## Подробнее

Бот реализован с использованием библиотеки `discord.py`. 
Он  поддерживает следующие функции:

- **Обработка команд:** Бот обрабатывает команды, вводимые пользователями в чате Discord. 
  - Например, команды `!hi`, `!join`, `!leave`, `!train`, `!test`, `!archive`, `!select_dataset`, `!instruction`, 
    `!correct`, `!feedback`, `!getfile` и т.д. 
- **Обработка сообщений:** Бот анализирует входящие сообщения, игнорируя собственные сообщения. 
  - Если пользователь отправляет аудиофайл, бот распознает речь и отправляет текст в ответ. 
  - Если пользователь находится в голосовом канале, бот преобразует текст в речь и воспроизводит его в голосовом канале.
- **Распознавание речи:** Функция `recognizer` скачивает аудиофайл, конвертирует его в формат WAV и распознает речь с помощью Google Speech Recognition.
- **Преобразование текста в речь:** Функция `text_to_speech_and_play` преобразует текст в речь с помощью библиотеки `gTTS` и воспроизводит его в голосовом канале.

## Запуск бота

Бот запускается с использованием токена, хранящегося в переменной `gs.credentials.discord.bot_token`.

## Модули и библиотеки

- `discord.py`: Основная библиотека для создания Discord-ботов.
- `speech_recognition`: Для распознавания речи.
- `pydub`: Для конвертации аудиофайлов.
- `gtts`: Для преобразования текста в речь.
- `requests`: Для скачивания файлов.
- `pathlib`: Для работы с путями файлов.
- `tempfile`: Для создания временных файлов.
- `asyncio`: Для асинхронного выполнения задач.

## Классы

### `DiscordBot`

**Описание**: Класс, представляющий Discord-бота. 

**Наследует**: `discord.Client`

**Атрибуты**:

- `prefix` (str): Префикс команд бота (по умолчанию `!`).
- `intents` (discord.Intents): Разрешения бота на доступ к событиям Discord. 

**Методы**:

- `on_ready()`: Вызывается при готовности бота к работе.
- `on_message(message)`: Вызывается при получении нового сообщения.
- `on_voice_state_update(member, before, after)`: Вызывается при изменении состояния пользователя в голосовом канале.

**Примеры**:

```python
import discord
from src.endpoints.bots.discord.bot import DiscordBot

# Инициализация бота
bot = DiscordBot(prefix='!', intents=discord.Intents.all())

# Запуск бота
bot.run(gs.credentials.discord.bot_token)
```

## Функции

### `recognizer(url: str) -> str`

**Назначение**: Функция, которая скачивает аудиофайл, конвертирует его в формат WAV и распознает речь с помощью Google Speech Recognition.

**Параметры**:

- `url` (str): URL-адрес аудиофайла.

**Возвращает**:

- `str`: Распознанный текст.

**Пример**:

```python
audio_url = 'https://example.com/audio.mp3'
recognized_text = recognizer(audio_url)
print(f'Распознанный текст: {recognized_text}')
```

### `text_to_speech_and_play(text: str, voice_channel: discord.VoiceChannel)`

**Назначение**: Функция, которая преобразует текст в речь с помощью библиотеки `gTTS` и воспроизводит его в голосовом канале.

**Параметры**:

- `text` (str): Текст для преобразования.
- `voice_channel` (discord.VoiceChannel): Голосовой канал для воспроизведения.

**Пример**:

```python
text_to_speak = 'Привет, мир!'
voice_channel = bot.voice_clients[0].channel
text_to_speech_and_play(text_to_speak, voice_channel)
```

## Параметры

- `gs.credentials.discord.bot_token` (str): Токен доступа к Discord API.

## Примеры

```python
# Создание экземпляра DiscordBot
bot = DiscordBot(prefix='!', intents=discord.Intents.all())

# Обработчик события 'on_ready'
@bot.event
async def on_ready():
    print(f'Бот {bot.user} запущен.')

# Обработчик события 'on_message'
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!hi'):
        await message.channel.send('Привет!')

# Запуск бота
bot.run(gs.credentials.discord.bot_token)
```