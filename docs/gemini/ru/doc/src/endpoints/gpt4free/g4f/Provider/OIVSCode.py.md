# Модуль `OIVSCode`

## Обзор

Этот модуль определяет класс `OIVSCode`, представляющий собой провайдера для OpenAI GPT-4 API. Он предоставляет доступ к различным моделям, включая:

- `gpt-4o-mini-2024-07-18`
- `gpt-4o-mini`
- `deepseek-ai/DeepSeek-V3`

## Подробней

Класс `OIVSCode` наследует от класса `OpenaiTemplate`, который определяет базовый интерфейс для взаимодействия с GPT-4 API. 
Он реализует следующие особенности:

- Поддержка потоковой передачи ответов (supports_stream = True)
- Поддержка системных сообщений (supports_system_message = True)
- Поддержка истории сообщений (supports_message_history = True)

## Классы

### `class OIVSCode`

**Описание**:  Класс, представляющий собой провайдера для OpenAI GPT-4 API. 
**Наследует**: `OpenaiTemplate`

**Атрибуты**:

- `label (str)`:  Название провайдера.
- `url (str)`: Базовый URL API.
- `api_base (str)`: Базовый URL для API-запросов.
- `working (bool)`:  Индикатор доступности провайдера.
- `needs_auth (bool)`:  Флаг, указывающий на необходимость авторизации.
- `supports_stream (bool)`:  Флаг, указывающий на поддержку потоковой передачи ответов.
- `supports_system_message (bool)`: Флаг, указывающий на поддержку системных сообщений.
- `supports_message_history (bool)`: Флаг, указывающий на поддержку истории сообщений.
- `default_model (str)`:  Модель по умолчанию.
- `default_vision_model (str)`:  Модель по умолчанию для задач, связанных с компьютерным зрением.
- `vision_models (list)`: Список моделей, поддерживающих задачи, связанные с компьютерным зрением.
- `models (list)`: Список всех поддерживаемых моделей.
- `model_aliases (dict)`: Словарь с псевдонимами моделей.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.OIVSCode import OIVSCode

# Создание экземпляра провайдера
provider = OIVSCode()

# Получение списка поддерживаемых моделей
print(provider.models)

# Использование модели по умолчанию
response = provider.generate_text(prompt="Привет, мир!", model=provider.default_model)

# Использование модели с псевдонимом
response = provider.generate_text(prompt="Привет, мир!", model="gpt-4o-mini")

# Использование модели "deepseek-ai/DeepSeek-V3"
response = provider.generate_text(prompt="Привет, мир!", model="deepseek-v3")

```

## Методы класса 

### `generate_text`

```python
def generate_text(
        self,
        prompt: str,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        top_p: float = 1.0,
        top_k: int = 0,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        stream: bool = False,
        system_message: str | None = None,
        message_history: list | None = None,
        **kwargs
    ) -> str | Generator[str, None, None]:
        """
        Генерирует текст с помощью выбранной модели.

        Args:
            prompt (str): Текстовый запрос для генерации.
            model (str | None, optional):  Модель для генерации. По умолчанию использует `self.default_model`.
            temperature (float, optional): Параметр "температуры" для генерации. По умолчанию 0.7.
            max_tokens (int, optional): Максимальное количество токенов в ответе. По умолчанию 1024.
            top_p (float, optional): Параметр "top_p" для генерации. По умолчанию 1.0.
            top_k (int, optional): Параметр "top_k" для генерации. По умолчанию 0.
            presence_penalty (float, optional):  Штраф за присутствие токенов. По умолчанию 0.0.
            frequency_penalty (float, optional):  Штраф за частоту токенов. По умолчанию 0.0.
            stream (bool, optional): Флаг, указывающий на использование потоковой передачи. По умолчанию False.
            system_message (str | None, optional):  Системное сообщение. По умолчанию None.
            message_history (list | None, optional):  История сообщений. По умолчанию None.

        Returns:
            str | Generator[str, None, None]:  Генерированный текст или генератор текстовых фрагментов.
        """
        ...
```

### `get_model_alias`

```python
    def get_model_alias(self, model: str) -> str:
        """
        Возвращает алиас для модели.

        Args:
            model (str): Название модели.

        Returns:
            str: Алиас для модели.
        """
        ...
```

### `get_available_models`

```python
    def get_available_models(self) -> list[str]:
        """
        Возвращает список доступных моделей.

        Returns:
            list[str]: Список доступных моделей.
        """
        ...
```

### `get_model_description`

```python
    def get_model_description(self, model: str) -> str | None:
        """
        Возвращает описание модели.

        Args:
            model (str): Название модели.

        Returns:
            str | None: Описание модели или None, если модель не найдена.
        """
        ...
```

### `get_model_parameters`

```python
    def get_model_parameters(self, model: str) -> dict:
        """
        Возвращает параметры модели.

        Args:
            model (str): Название модели.

        Returns:
            dict: Параметры модели.
        """
        ...
```

### `get_model_capabilities`

```python
    def get_model_capabilities(self, model: str) -> dict:
        """
        Возвращает список возможностей модели.

        Args:
            model (str): Название модели.

        Returns:
            dict:  Список возможностей модели.
        """
        ...
```

### `get_model_usage`

```python
    def get_model_usage(self, model: str) -> dict | None:
        """
        Возвращает информацию об использовании модели.

        Args:
            model (str): Название модели.

        Returns:
            dict | None:  Информация об использовании модели.
        """
        ...
```