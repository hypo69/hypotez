# Gravityengine Provider

## Overview

Этот модуль содержит код провайдера `Gravityengine`, который используется для взаимодействия с API Gravity Engine для генерации текста с помощью модели GPT-3.5.

## Details

Модуль реализует функцию `_create_completion`, которая отправляет запрос на API Gravity Engine, используя модель GPT-3.5, и получает ответ в формате JSON. 

## Classes

### `class _create_completion`

**Description:** 
   Функция `_create_completion` отправляет запрос на API Gravity Engine, используя модель GPT-3.5, и получает ответ в формате JSON.

**Purpose**:  Отправка запроса на API Gravity Engine и получение ответа.

**Parameters**:
- `model` (str): Имя модели GPT-3.5, которую нужно использовать.
- `messages` (list): Список сообщений, которые необходимо передать модели.
- `stream` (bool): Указывает, необходимо ли использовать потоковую передачу для получения ответа.

**Returns**:
- `yield response.json()['choices'][0]['message']['content']`:  Возвращает строку с текстом ответа от модели.

**Raises Exceptions**:
- `ExecutionError`:  Возникает при ошибке выполнения запроса.

**How the Function Works**:
- Функция принимает имя модели, список сообщений и флаг потоковой передачи.
- Она формирует заголовок запроса и данные для отправки на API Gravity Engine.
- Затем она отправляет POST-запрос на API Gravity Engine и получает ответ в формате JSON.
- Она обрабатывает ответ, извлекая текст ответа от модели.
- Функция возвращает текст ответа.

**Examples**:
```python
messages = [
    {"role": "user", "content": "Привет! Напиши мне стихотворение про любовь."}
]
response = _create_completion(model='gpt-3.5-turbo-16k', messages=messages, stream=True)
print(response) # Вывод:  стихотворение про любовь
```

## Parameter Details

- `model` (str):  Имя модели GPT-3.5.
- `messages` (list): Список сообщений, которые необходимо передать модели.
- `stream` (bool):  Указывает, необходимо ли использовать потоковую передачу для получения ответа.

## Examples

```python
# Пример использования функции _create_completion
messages = [
    {"role": "user", "content": "Привет! Напиши мне стихотворение про любовь."}
]
response = _create_completion(model='gpt-3.5-turbo-16k', messages=messages, stream=True)
print(response)
```