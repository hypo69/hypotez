# Модуль для работы с аудио

## Обзор

Модуль содержит примеры асинхронной работы с аудио, используя библиотеку `g4f` для генерации и транскрибирования аудиофайлов.
Он демонстрирует взаимодействие с провайдерами `PollinationsAI` и `Microsoft_Phi_4` для выполнения задач, связанных с аудио.

## Более подробно

Этот модуль показывает, как можно использовать асинхронный клиент `AsyncClient` из библиотеки `g4f` для генерации аудиофайлов и их транскрибирования.
Он содержит примеры создания аудио с использованием голоса `alloy` через провайдера `PollinationsAI`, а также транскрибирования аудиофайла с использованием провайдера `Microsoft_Phi_4`.
Этот код может быть полезен для автоматической генерации и обработки аудиоконтента в различных приложениях.

## Функции

### `main`

```python
async def main():
    """Асинхронная функция для демонстрации работы с аудио.

    Функция демонстрирует два основных сценария:
    1. Генерация аудио с использованием провайдера PollinationsAI и сохранение его в файл "alloy.mp3".
    2. Транскрибирование аудиофайла "audio.wav" с использованием провайдера Microsoft_Phi_4 и вывод результата в консоль.

    Пример:
        Запуск функции приводит к генерации и транскрибированию аудиофайлов с использованием указанных провайдеров.
    """
```

**Как работает функция**:

1.  Создается асинхронный клиент `AsyncClient` с указанием провайдера `PollinationsAI`.
2.  Выполняется запрос к модели `openai-audio` для генерации аудио с текстом "Say good day to the world", используя голос `alloy` и формат `mp3`.
3.  Полученный аудиофайл сохраняется под именем "alloy.mp3".
4.  Открывается аудиофайл "audio.wav" для транскрибирования.
5.  Выполняется запрос к провайдеру `Microsoft_Phi_4` для транскрибирования аудиофайла.
6.  Результат транскрибирования выводится в консоль.

**Примеры**:

```python
import asyncio
from g4f.client import AsyncClient
import g4f.Provider
import g4f.models

async def main():
    client = AsyncClient(provider=g4f.Provider.PollinationsAI)

    # Generate audio with PollinationsAI
    response = await client.chat.completions.create(
        model="openai-audio",
        messages=[{"role": "user", "content": "Say good day to the world"}],
        audio={ "voice": "alloy", "format": "mp3" },
    )
    response.choices[0].message.save("alloy.mp3")

    # Transcribe a audio file
    with open("audio.wav", "rb") as audio_file:
        response = await client.chat.completions.create(
            messages="Transcribe this audio",
            provider=g4f.Provider.Microsoft_Phi_4,
            media=[[audio_file, "audio.wav"]],\
            modalities=["text"],
        )
        print(response.choices[0].message.content)

if __name__ == "__main__":
    asyncio.run(main())