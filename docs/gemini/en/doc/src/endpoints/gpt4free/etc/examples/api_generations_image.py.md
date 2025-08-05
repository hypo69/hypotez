# Генерация изображения с помощью API gpt4free

## Обзор

Данный файл демонстрирует пример использования API gpt4free для генерации изображения по текстовому запросу. 

## Подробности

Файл содержит код, который отправляет POST-запрос на сервер gpt4free с JSON-объектом, содержащим текстовый запрос (prompt) для генерации изображения. В ответе от сервера  получаются данные о сгенерированном изображении. 

## Пример

### Параметры запроса

```python
url = "http://localhost:1337/v1/images/generations"
body = {
    "model": "flux",  # модель генерации изображений
    "prompt": "hello world user",  # текстовый запрос для генерации изображения
    "response_format": None  # формат ответа. Возможные варианты: None, "url", "b64_json".
}
```

### Отправка запроса и получение ответа

```python
data = requests.post(url, json=body, stream=True).json()
print(data)
```

**Важно:**

- API gpt4free предоставляет бесплатную версию, которая может иметь ограничение по количеству запросов и времени выполнения.
- В этом коде, используется модель `flux` для генерации изображения.
- В зависимости от модели и параметров запроса, формат ответа может отличаться.

## Код

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