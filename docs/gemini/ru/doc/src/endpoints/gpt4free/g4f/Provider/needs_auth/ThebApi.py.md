# Модуль ThebApi
## Обзор
Модуль `ThebApi` предоставляет класс `ThebApi`, который реализует взаимодействие с API платформы TheB.AI для получения ответов от языковых моделей. 

## Подробности
Модуль `ThebApi` является частью проекта `hypotez`, предназначенного для работы с различными AI-моделями. 
Класс `ThebApi` предоставляет механизм для отправки запросов к API TheB.AI и получения ответов от различных моделей, таких как `theb-ai`, `gpt-3.5-turbo`, `gpt-4`, `gpt-4-turbo`, `claude-3.5-sonnet`, `llama-2-7b-chat`, `llama-2-13b-chat`, `llama-2-70b-chat`, `code-llama-7b`, `code-llama-13b`, `code-llama-34b`, `qwen-2-72b`. 

## Классы

### `class ThebApi(OpenaiTemplate)`

**Описание**: Класс `ThebApi` наследует от `OpenaiTemplate` и реализует специфические особенности взаимодействия с API TheB.AI.

**Атрибуты**:

 - `label` (str): Метка для идентификации провайдера, в данном случае "TheB.AI API".
 - `url` (str): Базовый URL API TheB.AI.
 - `login_url` (str): URL для входа в TheB.AI.
 - `api_base` (str): Базовый URL API TheB.AI.
 - `working` (bool): Флаг, указывающий на работоспособность API TheB.AI.
 - `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации при взаимодействии с API TheB.AI.
 - `default_model` (str): Название модели по умолчанию, используемой TheB.AI.
 - `fallback_models` (list): Список доступных моделей в TheB.AI.

**Методы**:

 - `create_async_generator(model: str, messages: Messages, temperature: float = None, top_p: float = None, **kwargs) -> CreateResult`: 
    - **Назначение**: Метод для создания асинхронного генератора ответов от модели TheB.AI. 
    - **Параметры**: 
        - `model` (str): Название модели для использования.
        - `messages` (Messages): Список сообщений в контексте диалога.
        - `temperature` (float): Параметр, влияющий на случайность генерируемого текста (по умолчанию `None`).
        - `top_p` (float): Параметр, влияющий на выбор вариантов слов (по умолчанию `None`).
        - `**kwargs`: Дополнительные аргументы.
    - **Возвращает**: `CreateResult`: Объект, содержащий информацию о результате запроса к модели.
    - **Как работает**:
        - Извлекает системные сообщения из списка `messages` и объединяет их в одну строку.
        - Фильтрует сообщения из списка `messages`, удаляя системные сообщения.
        - Создает словарь `data` с параметрами для запроса к модели TheB.AI.
        - Вызывает метод `create_async_generator` базового класса `OpenaiTemplate` с указанными параметрами и дополнительными данными из `data`.
        - Возвращает результат от `create_async_generator` базового класса.


## Примеры
```python
# Создание экземпляра класса ThebApi
theb_api = ThebApi()

# Получение ответа от модели theb-ai
messages = [
    {"role": "user", "content": "Привет! Как дела?"},
]
response = theb_api.create_async_generator(model="theb-ai", messages=messages)
print(response) # Вывод: Объект CreateResult с информацией о ответе

# Использование метода create_async_generator с дополнительными параметрами
response = theb_api.create_async_generator(model="theb-ai", messages=messages, temperature=0.7, top_p=0.8)
print(response) # Вывод: Объект CreateResult с информацией о ответе с измененными параметрами

```
```python
                from __future__ import annotations\n\nfrom ...typing import CreateResult, Messages\nfrom ..helper import filter_none\nfrom ..template import OpenaiTemplate\n\nmodels = {\n    "theb-ai": "TheB.AI",\n    "gpt-3.5-turbo": "GPT-3.5",\n    "gpt-4-turbo": "GPT-4 Turbo",\n    "gpt-4": "GPT-4",\n    "claude-3.5-sonnet": "Claude",\n    "llama-2-7b-chat": "Llama 2 7B",\n    "llama-2-13b-chat": "Llama 2 13B",\n    "llama-2-70b-chat": "Llama 2 70B",\n    "code-llama-7b": "Code Llama 7B",\n    "code-llama-13b": "Code Llama 13B",\n    "code-llama-34b": "Code Llama 34B",\n    "qwen-2-72b": "Qwen"\n}\n\nclass ThebApi(OpenaiTemplate):\n    label = "TheB.AI API"\n    url = "https://theb.ai"\n    login_url = "https://beta.theb.ai/home"\n    api_base = "https://api.theb.ai/v1"\n    working = True\n    needs_auth = True\n\n    default_model = "theb-ai"\n    fallback_models = list(models)\n\n    @classmethod\n    def create_async_generator(\n        cls,\n        model: str,\n        messages: Messages,\n        temperature: float = None,\n        top_p: float = None,\n        **kwargs\n    ) -> CreateResult:\n        system_message = "\\n".join([message["content"] for message in messages if message["role"] == "system"])\n        messages = [message for message in messages if message["role"] != "system"]\n        data = {\n            "model_params": filter_none(\n                system_prompt=system_message,\n                temperature=temperature,\n                top_p=top_p,\n            )\n        }\n        return super().create_async_generator(model, messages, extra_data=data, **kwargs)\n\n                ```