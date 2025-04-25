## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода демонстрирует использование библиотеки `g4f` для работы с аудио с помощью модели GPT-4. Он содержит два примера:  генерацию аудио с помощью `PollinationsAI` и транскрипцию аудиофайла с помощью `Microsoft_Phi_4`.

Шаги выполнения
-------------------------
1. **Импорт необходимых библиотек:**
    - `asyncio`: для работы с асинхронным кодом.
    - `g4f.client`: для создания объекта клиента GPT-4.
    - `g4f.Provider`: для выбора провайдера модели GPT-4.
    - `g4f.models`: для работы с моделями GPT-4.
2. **Создание объекта клиента:**
    -  Инициализируется объект `AsyncClient` с помощью `g4f.Provider.PollinationsAI`.
3. **Генерация аудио:**
    - Вызывается метод `client.chat.completions.create` с параметрами:
        - `model="openai-audio"`: выбор модели для генерации аудио.
        - `messages=[{"role": "user", "content": "Say good day to the world"}]`: текст, который будет озвучен.
        - `audio={ "voice": "alloy", "format": "mp3" }`: параметры аудио, такие как голос и формат.
    - Результат сохраняется в файл `alloy.mp3`.
4. **Транскрипция аудио:**
    - Открывается аудиофайл `audio.wav` в бинарном режиме.
    - Вызывается метод `client.chat.completions.create` с параметрами:
        - `messages="Transcribe this audio"`:  запрос на транскрипцию.
        - `provider=g4f.Provider.Microsoft_Phi_4`: выбор модели для транскрипции.
        - `media=[[audio_file, "audio.wav"]]:`  загрузка аудиофайла.
        - `modalities=["text"]`:  указание желаемого типа выходных данных (текст).
    - Результат транскрипции выводится на консоль.

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