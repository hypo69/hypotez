# Модуль `MiniMax`

## Обзор

Модуль `MiniMax` предоставляет класс `MiniMax`, который представляет собой реализацию API для доступа к модели `MiniMax`.

## Подробней

Класс `MiniMax` наследует класс `OpenaiTemplate` и предоставляет ряд атрибутов и методов для работы с API `MiniMax`. 

- `label`: `MiniMax API`
- `url`: Базовый URL для общения с API.
- `login_url`: URL для получения ключа API.
- `api_base`: Базовый URL для вызовов API.
- `working`: `True`, указывает на то, что API работает.
- `needs_auth`: `True`, указывает на то, что API требует авторизации.
- `default_model`: Имя модели по умолчанию.
- `default_vision_model`: Имя модели по умолчанию для обработки изображений.
- `models`: Список доступных моделей.
- `model_aliases`: Словарь с псевдонимами моделей.

## Классы

### `class MiniMax(OpenaiTemplate)`

**Описание**: Класс `MiniMax` представляет собой реализацию API для доступа к модели `MiniMax`. 

**Наследует**: 
    - `OpenaiTemplate` 

**Атрибуты**: 

- `label` (str): "MiniMax API"
- `url` (str): `https://www.hailuo.ai/chat`
- `login_url` (str): `https://intl.minimaxi.com/user-center/basic-information/interface-key`
- `api_base` (str): `https://api.minimaxi.chat/v1`
- `working` (bool): `True`
- `needs_auth` (bool): `True`
- `default_model` (str): `MiniMax-Text-01`
- `default_vision_model` (str): `MiniMax-Text-01`
- `models` (list): `[default_model, "abab6.5s-chat"]`
- `model_aliases` (dict): `{"MiniMax": default_model}`

**Принцип работы**: 

Класс `MiniMax` реализует методы для взаимодействия с API `MiniMax`, такие как аутентификация, получение ключа API, отправка запросов и обработка ответов. 

## Примеры

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.mini_max.MiniMax import MiniMax

# Создание экземпляра класса MiniMax
mini_max = MiniMax()

# Получение ключа API
mini_max.get_api_key()

# Отправка запроса к модели
response = mini_max.send_request(prompt="Привет, как дела?")

# Обработка ответа
print(response)
```