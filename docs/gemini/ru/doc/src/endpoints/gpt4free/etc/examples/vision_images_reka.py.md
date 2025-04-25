# Модуль для обработки изображений с помощью Reca

## Обзор

Этот модуль предоставляет пример использования API Reca для анализа изображений с помощью чат-бота. 

## Подробней

Модуль использует библиотеку `g4f` для взаимодействия с API Reca. Он демонстрирует, как загрузить изображение и задать вопрос чат-боту об изображении. 

## Функции

### `completions.create()`

**Назначение**: 
Функция `completions.create()` из библиотеки `g4f` отправляет запрос к API Reca для получения ответа на основе предоставленного текста и изображения.

**Параметры**:

- `model` (str):  Название модели, в данном случае "reka-core" - это название модели чат-бота от Reca. 
- `messages` (list): Список сообщений, представляющий собой диалог с чат-ботом. Каждый элемент списка должен быть словарем с ключами `role` и `content`. В данном случае используется сообщение от пользователя, которое задает вопрос о содержимом изображения.
- `stream` (bool): Флаг, указывающий, нужно ли получать ответ чат-бота потоково (True), или ждать, пока он не будет готов полностью (False).
- `image` (file): Файловый объект изображения, который нужно анализировать. 

**Возвращает**:
- `completion` (Generator): Итератор, который выдает части ответа чат-бота.

**Как работает функция**:
- Функция `completions.create()` отправляет запрос к API Reca, который включает текст сообщения и изображение.
- Reca анализирует изображение и отвечает на вопрос пользователя.
- Ответ чат-бота поступает частями через генератор `completion`.

**Примеры**:

```python
from g4f.client import Client
from g4f.Provider import Reka

client = Client(
    provider=Reka  # Optional if you set model name to reka-core
)

completion = client.chat.completions.create(
    model="reka-core",
    messages=[
        {
            "role": "user",
            "content": "What can you see in the image ?"
        }
    ],
    stream=True,
    image=open("docs/images/cat.jpeg", "rb")  # open("path", "rb"), do not use .read(), etc. it must be a file object
)

for message in completion:
    print(message.choices[0].delta.content or "")