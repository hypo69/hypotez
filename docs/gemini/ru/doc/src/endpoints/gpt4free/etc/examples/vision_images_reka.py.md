# Документация для модуля vision_images_reka.py

## Обзор

Модуль демонстрирует пример использования API `gpt4free` для взаимодействия с моделью `Reka` и анализа изображений. Он показывает, как отправить изображение в модель и получить описание содержимого изображения.

## Подробнее

Этот модуль предоставляет пример кода для отправки изображения в чат-бота `Reka` и получения ответа с описанием содержимого изображения. Для работы с этим примером необходимо быть залогиненным в `chat.reka.ai` и иметь сохраненные cookies. Также требуется изображение `cat.jpeg` в директории `docs/images/`.

## Классы

В данном коде классы не используются.

## Функции

В данном коде функции не используются.

## Переменные

- `client`: Объект класса `Client` из модуля `g4f.client`, используемый для взаимодействия с API.
- `completion`: Объект, представляющий собой ответ от API после отправки запроса с изображением.
- `message`: Переменная, используемая в цикле для итерации по сообщениям, полученным от API.

## Примеры

Пример использования модуля:

```python
# Image Chat with Reca
# !! YOU NEED COOKIES / BE LOGGED IN TO chat.reka.ai
# download an image and save it as test.png in the same folder

from g4f.client import Client
from g4f.Provider import Reka

client = Client(
    provider = Reka # Optional if you set model name to reka-core
)

completion = client.chat.completions.create(
    model = "reka-core",
    messages = [
        {
            "role": "user",
            "content": "What can you see in the image ?"
        }
    ],
    stream = True,
    image = open("docs/images/cat.jpeg", "rb") # open("path", "rb"), do not use .read(), etc. it must be a file object
)

for message in completion:
    print(message.choices[0].delta.content or "")

    # >>> In the image there is ...
```
Этот код инициализирует клиент `Reka`, отправляет запрос с изображением и вопросом "Что ты видишь на изображении?" и печатает полученный ответ.