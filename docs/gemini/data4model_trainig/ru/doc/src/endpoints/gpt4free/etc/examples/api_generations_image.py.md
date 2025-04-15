# Модуль для генерации изображений через API

## Обзор

Этот модуль содержит пример кода для отправки запроса на генерацию изображения через API, используя библиотеку `requests`. Он демонстрирует, как задать параметры модели, текстовое описание и формат ответа.

## Подробнее

Этот код предназначен для отправки POST-запроса к API по адресу `http://localhost:1337/v1/images/generations` с целью генерации изображения на основе предоставленных параметров. Используется библиотека `requests` для отправки HTTP-запроса. Параметры запроса включают модель, текстовое описание и формат ответа.

## Функции

### Отправка запроса на генерацию изображения

```python
import requests
url = "http://localhost:1337/v1/images/generations"
body = {
    "model": "flux",
    "prompt": "hello world user",
    "response_format": None,
    #"response_format": "url",
    #"response_format": "b64_json",
}
data = requests.post(url, json=body, stream=True).json()
print(data)
```

**Назначение**: Отправляет запрос на генерацию изображения к API и выводит полученные данные.

**Параметры**:

- `url` (str): URL-адрес API для генерации изображений.
- `body` (dict): Словарь с параметрами запроса, включающий:
    - `model` (str): Название модели для генерации изображения (в данном случае "flux").
    - `prompt` (str): Текстовое описание для генерации изображения (в данном случае "hello world user").
    - `response_format` (Optional[str]): Формат ответа API (может быть `None`, `"url"` или `"b64_json"`).

**Возвращает**:

- `data` (dict): JSON-ответ от API с информацией о сгенерированном изображении.

**Как работает функция**:

1. Импортирует библиотеку `requests`.
2. Определяет URL-адрес API и тело запроса с необходимыми параметрами.
3. Отправляет POST-запрос к API с использованием `requests.post()`, указывая, что данные передаются в формате JSON, и включает потоковую передачу (`stream=True`).
4. Преобразует ответ от API в формат JSON с помощью `.json()`.
5. Выводит полученные данные в консоль.

**Примеры**:

```python
import requests
url = "http://localhost:1337/v1/images/generations"
body = {
    "model": "flux",
    "prompt": "a cat",
    "response_format": "url",
}
data = requests.post(url, json=body, stream=True).json()
print(data)
```

```python
import requests
url = "http://localhost:1337/v1/images/generations"
body = {
    "model": "flux",
    "prompt": "a dog",
    "response_format": "b64_json",
}
data = requests.post(url, json=body, stream=True).json()
print(data)
```