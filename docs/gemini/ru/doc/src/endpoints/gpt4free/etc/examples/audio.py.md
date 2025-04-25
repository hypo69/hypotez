# Модуль для работы с аудио с использованием GPT-4Free

## Обзор

Этот модуль предоставляет примеры использования GPT-4Free для генерации и транскрипции аудио. Он демонстрирует использование API GPT-4Free с помощью библиотеки `g4f` для работы с различными поставщиками, такими как PollinationsAI и Microsoft Phi-4.

## Пример использования

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

## Функции

### `main`

**Назначение**: 
Асинхронная функция, которая демонстрирует использование GPT-4Free для генерации и транскрипции аудио.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Вызывает исключения**:
- Возможны ошибки сети или ошибки API при работе с GPT-4Free.

**Как работает функция**:
- Создает объект `AsyncClient` с использованием провайдера PollinationsAI.
- Использует функцию `client.chat.completions.create` для генерации аудио с помощью модели "openai-audio" и сохранения полученного аудио в файл "alloy.mp3".
- Использует функцию `client.chat.completions.create` для транскрипции аудиофайла "audio.wav" с помощью провайдера Microsoft Phi-4.
- Печатает текст транскрипции в консоль.

**Примеры**:
```python
# Запуск функции main
asyncio.run(main())
```


## Параметры

- `client` (`AsyncClient`): Объект клиента GPT-4Free, используемый для взаимодействия с API.
- `model` (`str`): Название модели GPT-4Free, используемой для генерации аудио.
- `messages` (`List[dict]`): Список сообщений, передаваемых модели для генерации аудио.
- `audio` (`dict`): Словарь с параметрами аудио, например, "voice" и "format".
- `media` (`List[List]`): Список файлов, передаваемых в качестве медиа для транскрипции.
- `modalities` (`List[str]`): Список модальностей, которые должны быть возвращены моделью.

## Примечания

- Модуль использует асинхронный стиль программирования с использованием `asyncio` для улучшения производительности при обработке запросов к API.
- Для работы с GPT-4Free необходим API-ключ от выбранного провайдера.
- Доступные модели и функции могут отличаться в зависимости от выбранного провайдера.

## Дополнительная информация

- Документация GPT-4Free: [https://gpt4free.com/](https://gpt4free.com/)
- Библиотека `g4f`: [https://github.com/g4f-org/g4f](https://github.com/g4f-org/g4f)