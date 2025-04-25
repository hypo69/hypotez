# Модуль PerplexityApi 

## Обзор

Модуль `PerplexityApi` предоставляет класс `PerplexityApi`, который реализует доступ к API сервиса Perplexity.ai. Класс наследует от класса `OpenaiTemplate`, предоставляющего общие методы для работы с различными API.

## Подробней

Модуль `PerplexityApi`  предназначен для использования в проекте `hypotez` для  обработки запросов к API сервиса Perplexity.ai.  Данный код обеспечивает взаимодействие с API сервиса Perplexity.ai для получения ответов от модели.  

## Классы

### `PerplexityApi`

**Описание**: Класс `PerplexityApi` реализует доступ к API сервиса Perplexity.ai. 
**Наследует**:  `OpenaiTemplate` 

**Атрибуты**:

 - `label` (str): Имя API -  "Perplexity API"
 - `url` (str): Основной URL сервиса - "https://www.perplexity.ai"
 - `login_url` (str): URL страницы авторизации - "https://www.perplexity.ai/settings/api"
 - `working` (bool):  Флаг, указывающий на доступность API - `True`
 - `needs_auth` (bool):  Флаг, указывающий на необходимость авторизации - `True`
 - `api_base` (str): Базовый URL для API -  "https://api.perplexity.ai"
 - `default_model` (str): Имя модели по умолчанию - "llama-3-sonar-large-32k-online"
 - `models` (list): Список доступных моделей 
 
 
 
 ## Примеры

```python
# Создание объекта класса PerplexityApi
api = PerplexityApi()

# Получение списка доступных моделей
print(api.models)

# Выполнение запроса к API с использованием модели по умолчанию
response = api.make_request(prompt="Какой сегодня день?")

# Вывод ответа
print(response.text)