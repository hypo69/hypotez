## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет класс `OpenaiAPI`, который представляет собой провайдера для доступа к API OpenAI. Он наследует класс `OpenaiTemplate` и предоставляет конфигурационные данные для использования API OpenAI.

Шаги выполнения
-------------------------
1. Определяется класс `OpenaiAPI`, который наследует класс `OpenaiTemplate`.
2. Устанавливаются атрибуты класса:
    - `label`: "OpenAI API" - имя провайдера.
    - `url`: "https://platform.openai.com" - базовый URL-адрес.
    - `login_url`: "https://platform.openai.com/settings/organization/api-keys" - URL-адрес для входа в API.
    - `api_base`: "https://api.openai.com/v1" - базовый URL-адрес для API.
    - `working`: True - флаг, указывающий, что API работает.
    - `needs_auth`: True - флаг, указывающий, что для использования API требуется авторизация.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.needs_auth.OpenaiAPI import OpenaiAPI

# Создание экземпляра класса OpenaiAPI
openai_api = OpenaiAPI()

# Получение имени провайдера
print(openai_api.label)  # Вывод: "OpenAI API"

# Получение базового URL-адреса
print(openai_api.url)  # Вывод: "https://platform.openai.com"
```