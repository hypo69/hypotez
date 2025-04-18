# Модуль запроса к API генерации изображений

## Обзор

Этот модуль демонстрирует пример запроса к API для генерации изображений. Он отправляет POST-запрос к локальному серверу и выводит полученные данные в формате JSON.

## Подробней

Модуль содержит пример кода, который отправляет запрос на генерацию изображения, используя модель "flux" с запросом "hello world user". Код демонстрирует, как настроить параметры запроса, такие как модель и текстовый запрос, и как обрабатывать ответ от API. Этот код может быть использован как отправная точка для интеграции с API генерации изображений в проекте `hypotez`.

## Функции

### Отправка запроса к API генерации изображений

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

**Назначение**: Отправляет POST-запрос к API для генерации изображений и выводит полученные данные в формате JSON.

**Параметры**:

-   `url` (str): URL-адрес API для генерации изображений.
-   `body` (dict): Тело запроса в формате JSON, содержащее параметры для генерации изображения, такие как модель и текстовый запрос.

**Возвращает**:

-   `data` (dict): Ответ от API в формате JSON.

**Как работает функция**:

1.  Определяется URL-адрес API и тело запроса в формате JSON.

2.  Отправляется POST-запрос к API с использованием библиотеки `requests`.
3.  Ответ от API преобразуется в формат JSON.
4.  Полученные данные выводятся в консоль.

```
Начало
  ↓
Определение URL и тела запроса (URL, тело_запроса)
  ↓
Отправка POST-запроса к API (POST-запрос)
  ↓
Преобразование ответа в JSON (JSON-ответ)
  ↓
Вывод данных (Вывод)
  ↓
Конец
```

**Примеры**:

```python
import requests
url = "http://localhost:1337/v1/images/generations"
body = {
    "model": "flux",
    "prompt": "hello world user",
    "response_format": None,
}
data = requests.post(url, json=body, stream=True).json()
print(data)