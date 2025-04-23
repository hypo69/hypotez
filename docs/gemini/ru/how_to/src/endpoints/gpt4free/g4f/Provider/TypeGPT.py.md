### **Как использовать блок кода TypeGPT**
=========================================================================================

Описание
-------------------------
Этот блок кода определяет класс `TypeGPT`, который является подклассом `OpenaiTemplate`. Он предназначен для взаимодействия с сервисом TypeGPT (chat.typegpt.net) через его API. Класс содержит настройки для подключения к API, включая URL, заголовки запросов, список поддерживаемых моделей, а также методы для получения списка доступных моделей.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируется `requests` для выполнения HTTP-запросов.
   - Импортируется `OpenaiTemplate` из `.template`, чтобы унаследовать базовый функционал.

2. **Определение класса `TypeGPT`**:
   - Устанавливаются атрибуты класса, такие как:
     - `label`: Имя провайдера ("TypeGpt").
     - `url`: URL сервиса TypeGPT.
     - `api_base`: Базовый URL для API запросов.
     - `working`: Флаг, указывающий на работоспособность провайдера (True).
     - `headers`: Заголовки HTTP-запросов, необходимые для взаимодействия с API.
     - `default_model`: Модель, используемая по умолчанию.
     - `default_vision_model`: Модель для работы с изображениями, используемая по умолчанию.
     - `vision_models`: Список моделей, поддерживающих обработку изображений.
     - `fallback_models`: Список моделей для переключения в случае проблем с основными моделями.
     - `image_models`: Список моделей, предназначенных для генерации изображений.
     - `model_aliases`: Словарь псевдонимов для моделей.

3. **Получение списка моделей**:
   - Определяется метод класса `get_models(cls, **kwargs)`, который извлекает список доступных моделей из API TypeGPT.
   - Если список моделей еще не был получен (`if not cls.models`):
     - Выполняется GET-запрос к `f"{cls.url}/api/config"` для получения конфигурации.
     - Извлекается строка со списком моделей из JSON-ответа (`.json()["customModels"]`).
     - Разделяется строка на список моделей, фильтруются модели, начинающиеся с "+" и не входящие в `image_models`.
   - Возвращается список доступных моделей.

Пример использования
-------------------------

```python
import requests
from .template import OpenaiTemplate

class TypeGPT(OpenaiTemplate):
    label = "TypeGpt"
    url = "https://chat.typegpt.net"
    api_base = "https://chat.typegpt.net/api/openai/v1"
    working = True
    headers = {
        "accept": "application/json, text/event-stream",
        "accept-language": "de,en-US;q=0.9,en;q=0.8",
        "content-type": "application/json",
        "priority": "u=1, i",
        "sec-ch-ua": "\\"Not(A:Brand\\";v=\\"99\\", \\"Google Chrome\\";v=\\"133\\", \\"Chromium\\";v=\\"133\\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\\"Linux\\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "referer": "https://chat.typegpt.net/",
    }
    
    default_model = 'gpt-4o-mini-2024-07-18'
    default_vision_model = default_model
    vision_models = ['gpt-3.5-turbo', 'gpt-3.5-turbo-202201', default_vision_model, "o3-mini"]
    fallback_models = vision_models + ["deepseek-r1", "deepseek-v3", "evil"]
    image_models = ["Image-Generator"]
    model_aliases = {
        "gpt-4o-mini": "gpt-4o-mini-2024-07-18",
        "evil": "uncensored-r1",
    }

    @classmethod
    def get_models(cls, **kwargs):
        if not cls.models:
            cls.models = requests.get(f"{cls.url}/api/config").json()["customModels"].split(",")
            cls.models = [model.split("@")[0][1:] for model in cls.models if model.startswith("+") and model not in cls.image_models]
        return cls.models

# Пример использования:
models = TypeGPT.get_models()
print(models)
```