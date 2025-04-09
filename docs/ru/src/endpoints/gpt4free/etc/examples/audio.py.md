# Модуль для работы с аудио через API g4f

## Обзор

Этот модуль демонстрирует, как использовать библиотеку `g4f` для генерации и транскрибации аудио с использованием различных провайдеров. Он включает в себя примеры генерации аудио с использованием PollinationsAI и транскрибации аудиофайла с использованием Microsoft Phi-4.

## Подробней

Модуль предоставляет асинхронные функции для взаимодействия с API g4f. Он показывает, как генерировать аудио из текста и как транскрибировать аудиофайл в текст. Это может быть полезно для приложений, требующих преобразования текста в речь и наоборот.

## Функции

### `main`

```python
async def main():
    """
    Асинхронная функция, демонстрирующая генерацию и транскрибацию аудио.

    Returns:
        None

    Raises:
        Exception: Если возникает ошибка при выполнении асинхронных операций.

    Example:
        >>> asyncio.run(main())
    """
```

**Назначение**: Основная асинхронная функция, которая демонстрирует процесс генерации аудио из текста и транскрибации аудиофайла в текст с использованием различных провайдеров g4f.

**Как работает функция**:

1.  **Инициализация асинхронного клиента**: Создается экземпляр `AsyncClient` с провайдером `g4f.Provider.PollinationsAI`.
2.  **Генерация аудио**: Используется метод `client.chat.completions.create` для генерации аудио из текста "Say good day to the world". Указывается модель "openai-audio", голос "alloy" и формат "mp3". Сгенерированное аудио сохраняется в файл "alloy.mp3".
3.  **Транскрибация аудиофайла**: Открывается аудиофайл "audio.wav" в бинарном режиме. Используется метод `client.chat.completions.create` для транскрибации аудиофайла с использованием провайдера `g4f.Provider.Microsoft_Phi_4`. Результат транскрибации выводится на экран.

**ASCII flowchart**:

```
Инициализация AsyncClient (PollinationsAI)
↓
Генерация аудио из текста (openai-audio, alloy, mp3)
↓
Сохранение аудио в файл (alloy.mp3)
↓
Открытие аудиофайла (audio.wav)
↓
Транскрибация аудиофайла (Microsoft_Phi_4)
↓
Вывод результата транскрибации
```

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
            media=[[audio_file, "audio.wav"]],
            modalities=["text"],
        )
        print(response.choices[0].message.content)

if __name__ == "__main__":
    asyncio.run(main())
```