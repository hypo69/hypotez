### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода демонстрирует, как генерировать аудио и транскрибировать аудиофайлы с использованием асинхронного клиента `g4f` (GPT4Free). Он использует провайдера `PollinationsAI` для генерации аудио и `Microsoft_Phi_4` для транскрибирования аудиофайлов.

Шаги выполнения
-------------------------
1. **Импорт библиотек**:
   - Импортируются необходимые библиотеки: `asyncio`, `AsyncClient` из `g4f.client`, `g4f.Provider` и `g4f.models`.
2. **Создание асинхронного клиента**:
   - Создается экземпляр `AsyncClient` с указанием провайдера `g4f.Provider.PollinationsAI`.
3. **Генерация аудио**:
   - Вызывается метод `client.chat.completions.create` для генерации аудио с использованием модели `"openai-audio"`.
   - В параметре `messages` передается сообщение с ролью "user" и содержанием "Say good day to the world".
   - Параметр `audio` указывает, что нужно сгенерировать аудио в формате "mp3" с голосом "alloy".
   - Сгенерированное аудио сохраняется в файл "alloy.mp3" с помощью метода `response.choices[0].message.save`.
4. **Транскрибирование аудиофайла**:
   - Открывается аудиофайл "audio.wav" в режиме чтения бинарных данных.
   - Вызывается метод `client.chat.completions.create` для транскрибирования аудио с использованием провайдера `g4f.Provider.Microsoft_Phi_4`.
   - В параметре `messages` передается сообщение "Transcribe this audio".
   - Параметр `media` содержит список, в котором указан файл "audio.wav" и его имя.
   - Параметр `modalities` указывает, что требуется получить текст.
   - Результат транскрибирования выводится на экран.
5. **Запуск асинхронной функции**:
   - Функция `main` запускается с помощью `asyncio.run(main())`.

Пример использования
-------------------------

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