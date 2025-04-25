# Модуль `DeepSeek`

## Обзор

Модуль `DeepSeek` предоставляет реализацию API для взаимодействия с сервисом `DeepSeek`.

## Подробнее

Модуль `DeepSeek` является частью проекта `hypotez` и обеспечивает доступ к модели `deepseek-chat` через API сервиса `DeepSeek`.

## Классы

### `DeepSeek`

**Описание**: Класс `DeepSeek` представляет собой реализацию API для взаимодействия с сервисом `DeepSeek`. Наследует от класса `OpenaiAPI` и реализует специфические методы для `DeepSeek`.

**Наследует**: `OpenaiAPI`

**Атрибуты**:

- `label` (str): Метка для модели, в данном случае `DeepSeek`.
- `url` (str): Основной URL сервиса `DeepSeek`.
- `login_url` (str): URL для входа в аккаунт `DeepSeek`.
- `working` (bool): Флаг, указывающий на доступность API.
- `api_base` (str): Базовый URL для вызова API.
- `needs_auth` (bool): Флаг, указывающий на необходимость авторизации для использования API.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `default_model` (str): Название модели по умолчанию.
- `fallback_models` (list): Список резервных моделей.

**Принцип работы**:

Класс `DeepSeek` расширяет функциональность класса `OpenaiAPI`, обеспечивая специфические настройки и методы для `DeepSeek`. 

**Методы**:

- Методы, наследуемые от `OpenaiAPI`.

## Параметры класса

- `label` (str): Метка для модели, в данном случае `DeepSeek`.
- `url` (str): Основной URL сервиса `DeepSeek`.
- `login_url` (str): URL для входа в аккаунт `DeepSeek`.
- `working` (bool): Флаг, указывающий на доступность API.
- `api_base` (str): Базовый URL для вызова API.
- `needs_auth` (bool): Флаг, указывающий на необходимость авторизации для использования API.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `default_model` (str): Название модели по умолчанию.
- `fallback_models` (list): Список резервных моделей.

**Примеры**:

```python
# Создание экземпляра класса DeepSeek
deepseek = DeepSeek()

# Доступ к атрибутам
print(deepseek.label)  # Вывод: DeepSeek
print(deepseek.url)  # Вывод: https://platform.deepseek.com

# Вызов методов, унаследованных от OpenaiAPI
response = deepseek.send_request(method='POST', url='https://api.deepseek.com/v1/chat/completions', data={'prompt': 'Hello, world!'})

# Обработка ответа
print(response.json())
```