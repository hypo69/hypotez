# Модуль API для взаимодействия с g4f

## Обзор

Модуль `api.py` предоставляет API для взаимодействия с различными моделями и провайдерами в проекте `g4f`. Он включает в себя методы для получения списка моделей, провайдеров, версий, а также для обработки запросов на генерацию текста и изображений.

## Подробнее

Этот модуль является ключевым компонентом серверной части GUI для g4f, обеспечивая взаимодействие между пользовательским интерфейсом и различными провайдерами моделей. Он содержит функции для обработки запросов, управления беседами и формирования ответов в формате JSON.

## Классы

### `Api`

**Описание**: Класс, содержащий статические методы для предоставления API.

**Принцип работы**:
Класс `Api` предоставляет набор статических методов для получения информации о моделях, провайдерах и версиях, а также методы для обработки запросов и формирования ответов. Он использует другие модули проекта `g4f`, такие как `ProviderUtils`, `version`, `models`, `ChatCompletion` и `debug`.

**Методы**:
- `get_models()`: Возвращает список доступных моделей.
- `get_provider_models(provider: str, api_key: str = None, api_base: str = None)`: Возвращает список моделей, поддерживаемых указанным провайдером.
- `get_providers()`: Возвращает список доступных провайдеров.
- `get_version()`: Возвращает информацию о текущей и последней версиях.
- `serve_images(name)`: Отправляет запрошенное изображение из директории с изображениями.
- `_prepare_conversation_kwargs(json_data: dict)`: Подготавливает аргументы для начала или продолжения беседы на основе входных данных в формате JSON.
- `_create_response_stream(kwargs: dict, conversation_id: str, provider: str, download_media: bool = True)`: Создает поток ответов на основе переданных аргументов.
- `_yield_logs()`: Генерирует логи отладки.
- `_format_json(response_type: str, content = None, **kwargs)`: Форматирует ответ в формате JSON.
- `handle_provider(provider_handler, model)`: Форматирует информацию о провайдере в формате JSON.

### `Api.get_models`

```python
    @staticmethod
    def get_models():
        return [{
            "name": model.name,
            "image": isinstance(model, models.ImageModel),
            "vision": isinstance(model, models.VisionModel),
            "providers": [
                getattr(provider, "parent", provider.__name__)
                for provider in providers
                if provider.working
            ]
        }
        for model, providers in models.__models__.values()]
```

**Назначение**: Возвращает список доступных моделей с информацией об их поддержке изображений, vision и провайдерах.

**Параметры**:
- Нет параметров.

**Возвращает**:
- `list[dict]`: Список словарей, где каждый словарь содержит информацию о модели.

**Как работает функция**:
1. Функция перебирает все модели и их провайдеров из `models.__models__.values()`.
2. Для каждой модели создается словарь, содержащий её имя, флаги поддержки изображений и vision, а также список провайдеров, поддерживающих эту модель.
3. Если у провайдера есть атрибут `parent`, используется его значение, иначе используется имя провайдера.
4. В итоговый список включаются только те провайдеры, у которых атрибут `working` имеет значение `True`.

**Примеры**:
```python
models_info = Api.get_models()
print(models_info)
```

### `Api.get_provider_models`

```python
    @staticmethod
    def get_provider_models(provider: str, api_key: str = None, api_base: str = None):
        if provider in ProviderUtils.convert:
            provider = ProviderUtils.convert[provider]
            if issubclass(provider, ProviderModelMixin):
                if "api_key" in signature(provider.get_models).parameters:
                    models = provider.get_models(api_key=api_key, api_base=api_base)
                else:
                    models = provider.get_models()
                return [
                    {
                        "model": model,
                        "default": model == provider.default_model,
                        "vision": getattr(provider, "default_vision_model", None) == model or model in getattr(provider, "vision_models", []),
                        "image": False if provider.image_models is None else model in provider.image_models,
                        "task": None if not hasattr(provider, "task_mapping") else provider.task_mapping[model] if model in provider.task_mapping else None
                    }
                    for model in models
                ]
        return []
```

**Назначение**: Возвращает список моделей, поддерживаемых указанным провайдером.

**Параметры**:
- `provider` (str): Имя провайдера.
- `api_key` (str, optional): API ключ для провайдера. По умолчанию `None`.
- `api_base` (str, optional): Базовый URL для API провайдера. По умолчанию `None`.

**Возвращает**:
- `list[dict]`: Список словарей, где каждый словарь содержит информацию о модели, поддерживаемой провайдером.

**Как работает функция**:

```
     Провайдер выбран
     │
     │ да
     │
     Проверка: есть ли провайдер в ProviderUtils.convert?
     │
     │ нет
     │
     Возврат: []
     │
     Провайдер конвертирован
     │
     Проверка: Является ли провайдер подклассом ProviderModelMixin?
     │
     │ нет
     │
     Возврат: []
     │
     Проверка: Есть ли параметр api_key в provider.get_models?
     │
     │ да
     │
     Получение моделей с api_key и api_base
     │
     Получение моделей
     │
     Формирование списка моделей с информацией (model, default, vision, image, task)
     │
     Возврат: список моделей
```

1. Функция проверяет, есть ли указанный провайдер в `ProviderUtils.convert`.
2. Если провайдер найден, он конвертируется с использованием `ProviderUtils.convert`.
3. Проверяется, является ли провайдер подклассом `ProviderModelMixin`.
4. Если провайдер является подклассом `ProviderModelMixin`, вызывается метод `get_models` провайдера. Если метод `get_models` принимает параметры `api_key` и `api_base`, они передаются при вызове.
5. Для каждой модели, возвращенной методом `get_models`, создается словарь, содержащий информацию о модели, является ли она моделью по умолчанию, поддерживает ли она vision и изображения, а также информацию о задаче (task), которую она выполняет.
6. Возвращается список словарей с информацией о моделях.

**Примеры**:
```python
provider_models = Api.get_provider_models("Gemini", api_key="YOUR_API_KEY")
print(provider_models)
```

### `Api.get_providers`

```python
    @staticmethod
    def get_providers() -> dict[str, str]:
        return [{
            "name": provider.__name__,
            "label": provider.label if hasattr(provider, "label") else provider.__name__,
            "parent": getattr(provider, "parent", None),
            "image": bool(getattr(provider, "image_models", False)),
            "vision": getattr(provider, "default_vision_model", None) is not None,
            "nodriver": getattr(provider, "use_nodriver", False),
            "hf_space": getattr(provider, "hf_space", False),
            "auth": provider.needs_auth,
            "login_url": getattr(provider, "login_url", None),
        } for provider in __providers__ if provider.working]
```

**Назначение**: Возвращает список доступных провайдеров с информацией об их возможностях и требованиях к аутентификации.

**Параметры**:
- Нет параметров.

**Возвращает**:
- `list[dict[str, str]]`: Список словарей, где каждый словарь содержит информацию о провайдере.

**Как работает функция**:
1. Функция перебирает все провайдеры из `__providers__`.
2. Для каждого провайдера создается словарь, содержащий его имя, метку (label), родительский провайдер (parent), флаги поддержки изображений и vision, флаг использования без драйвера (nodriver), флаг использования HF Space (hf_space), флаг необходимости аутентификации (auth) и URL для входа (login_url).
3. В итоговый список включаются только те провайдеры, у которых атрибут `working` имеет значение `True`.

**Примеры**:
```python
providers_info = Api.get_providers()
print(providers_info)
```

### `Api.get_version`

```python
    @staticmethod
    def get_version() -> dict:
        current_version = None
        latest_version = None
        try:
            current_version = version.utils.current_version
            latest_version = version.utils.latest_version
        except VersionNotFoundError:
            pass
        return {
            "version": current_version,
            "latest_version": latest_version,
        }
```

**Назначение**: Возвращает информацию о текущей и последней версиях.

**Параметры**:
- Нет параметров.

**Возвращает**:
- `dict`: Словарь, содержащий информацию о текущей и последней версиях.

**Как работает функция**:
1. Функция пытается получить текущую и последнюю версии из `version.utils`.
2. Если возникает исключение `VersionNotFoundError`, оно игнорируется.
3. Возвращается словарь, содержащий информацию о текущей и последней версиях.

**Примеры**:
```python
version_info = Api.get_version()
print(version_info)
```

### `Api.serve_images`

```python
    def serve_images(self, name):
        ensure_images_dir()
        return send_from_directory(os.path.abspath(images_dir), name)
```

**Назначение**: Отправляет запрошенное изображение из директории с изображениями.

**Параметры**:
- `name` (str): Имя файла изображения.

**Возвращает**:
- `Response`: Ответ Flask, содержащий файл изображения.

**Как работает функция**:
1. Функция вызывает `ensure_images_dir()` для обеспечения существования директории с изображениями.
2. Функция вызывает `send_from_directory` для отправки файла изображения из директории с изображениями.

**Примеры**:
```python
from flask import Flask

app = Flask(__name__)
api = Api()

@app.route("/images/<name>")
def serve_image(name):
    return api.serve_images(name)

if __name__ == "__main__":
    app.run(debug=True)
```

### `Api._prepare_conversation_kwargs`

```python
    def _prepare_conversation_kwargs(self, json_data: dict):
        kwargs = {**json_data}
        model = json_data.get('model')
        provider = json_data.get('provider')
        messages = json_data.get('messages')
        kwargs["tool_calls"] = [{
            "function": {
                "name": "bucket_tool"
            },
            "type": "function"
        }]
        action = json_data.get('action')
        if action == "continue":
            kwargs["tool_calls"].append({
                "function": {
                    "name": "continue_tool"
                },
                "type": "function"
            })
        conversation = json_data.get("conversation")
        if isinstance(conversation, dict):
            kwargs["conversation"] = JsonConversation(**conversation)
        else:
            conversation_id = json_data.get("conversation_id")
            if conversation_id and provider:
                if provider in conversations and conversation_id in conversations[provider]:
                    kwargs["conversation"] = conversations[provider][conversation_id]
        return {
            "model": model,
            "provider": provider,
            "messages": messages,
            "stream": True,
            "ignore_stream": True,
            "return_conversation": True,
            **kwargs
        }
```

**Назначение**: Подготавливает аргументы для создания или продолжения беседы на основе входных данных в формате JSON.

**Параметры**:
- `json_data` (dict): Словарь с данными запроса в формате JSON.

**Возвращает**:
- `dict`: Словарь с подготовленными аргументами для создания или продолжения беседы.

**Как работает функция**:

```
     Получение данных из json_data
     │
     Подготовка аргументов (kwargs)
     │
     Добавление tool_calls (bucket_tool)
     │
     Проверка: action == "continue"?
     │
     │ да
     │
     Добавление tool_calls (continue_tool)
     │
     Обработка conversation
     │
     Проверка: conversation - словарь?
     │
     │ да
     │
     Создание JsonConversation из conversation
     │
     Обработка conversation_id
     │
     Проверка: conversation_id и provider существуют?
     │
     │ да
     │
     Поиск conversation в conversations
     │
     Обновление kwargs["conversation"]
     │
     Возврат: kwargs
```

1. Функция получает данные из `json_data`, такие как `model`, `provider`, `messages` и `action`.
2. Подготавливаются аргументы `kwargs` на основе полученных данных.
3. Добавляется информация о `tool_calls`, включающая `bucket_tool`.
4. Если `action` равно `"continue"`, добавляется информация о `tool_calls`, включающая `continue_tool`.
5. Если `conversation` является словарем, создается экземпляр `JsonConversation` на основе этого словаря.
6. Если `conversation_id` и `provider` существуют, функция пытается найти существующую беседу в словаре `conversations`.
7. Если беседа найдена, она добавляется в `kwargs`.
8. Возвращается словарь `kwargs` с подготовленными аргументами.

**Примеры**:
```python
json_data = {
    "model": "gemini",
    "provider": "google",
    "messages": [{"role": "user", "content": "Hello"}],
    "action": "continue",
    "conversation_id": "123"
}
kwargs = Api()._prepare_conversation_kwargs(json_data)
print(kwargs)
```

### `Api._create_response_stream`

```python
    def _create_response_stream(self, kwargs: dict, conversation_id: str, provider: str, download_media: bool = True) -> Iterator:
        def decorated_log(text: str, file = None):
            debug.logs.append(text)
            if debug.logging:
                debug.log_handler(text, file=file)
        debug.log = decorated_log
        proxy = os.environ.get("G4F_PROXY")
        provider = kwargs.get("provider")
        try:
            model, provider_handler = get_model_and_provider(\
                kwargs.get("model"), provider,\
                stream=True,\
                ignore_stream=True,\
                logging=False,\
                has_images="media" in kwargs,\
            )
        except Exception as e:
            debug.error(e)
            yield self._format_json(\'error\', type(e).__name__, message=get_error_message(e))
            return
        if not isinstance(provider_handler, BaseRetryProvider):\
            if not provider:\
                provider = provider_handler.__name__
            yield self.handle_provider(provider_handler, model)\
            if hasattr(provider_handler, "get_parameters"):\
                yield self._format_json("parameters", provider_handler.get_parameters(as_json=True))\
        try:\
            result = iter_run_tools(ChatCompletion.create, **{**kwargs, "model": model, "provider": provider_handler, "download_media": download_media})\
            for chunk in result:\
                if isinstance(chunk, ProviderInfo):\
                    yield self.handle_provider(chunk, model)\
                    provider = chunk.name\
                elif isinstance(chunk, BaseConversation):\
                    if provider is not None:\
                        if hasattr(provider, "__name__"):\
                            provider = provider.__name__\
                        if provider not in conversations:\
                            conversations[provider] = {}\
                        conversations[provider][conversation_id] = chunk\
                        if isinstance(chunk, JsonConversation):\
                            yield self._format_json("conversation", {\
                                provider: chunk.get_dict()\
                            })\
                        else:\
                            yield self._format_json("conversation_id", conversation_id)\
                elif isinstance(chunk, Exception):\
                    logger.exception(chunk)\
                    debug.error(chunk)\
                    yield self._format_json(\'message\', get_error_message(chunk), error=type(chunk).__name__)\
                elif isinstance(chunk, RequestLogin):\
                    yield self._format_json("preview", chunk.to_string())\
                elif isinstance(chunk, PreviewResponse):\
                    yield self._format_json("preview", chunk.to_string())\
                elif isinstance(chunk, ImagePreview):\
                    yield self._format_json("preview", chunk.to_string(), urls=chunk.urls, alt=chunk.alt)\
                elif isinstance(chunk, MediaResponse):\
                    media = chunk\
                    if download_media or chunk.get("cookies"):\
                        chunk.alt = format_image_prompt(kwargs.get("messages"), chunk.alt)\
                        tags = [model, kwargs.get("aspect_ratio"), kwargs.get("resolution"), kwargs.get("width"), kwargs.get("height")]\
                        media = asyncio.run(copy_media(chunk.get_list(), chunk.get("cookies"), chunk.get("headers"), proxy=proxy, alt=chunk.alt, tags=tags))\
                        media = ImageResponse(media, chunk.alt) if isinstance(chunk, ImageResponse) else VideoResponse(media, chunk.alt)\
                    yield self._format_json("content", str(media), urls=chunk.urls, alt=chunk.alt)\
                elif isinstance(chunk, SynthesizeData):\
                    yield self._format_json("synthesize", chunk.get_dict())\
                elif isinstance(chunk, TitleGeneration):\
                    yield self._format_json("title", chunk.title)\
                elif isinstance(chunk, RequestLogin):\
                    yield self._format_json("login", str(chunk))\
                elif isinstance(chunk, Parameters):\
                    yield self._format_json("parameters", chunk.get_dict())\
                elif isinstance(chunk, FinishReason):\
                    yield self._format_json("finish", chunk.get_dict())\
                elif isinstance(chunk, Usage):\
                    yield self._format_json("usage", chunk.get_dict())\
                elif isinstance(chunk, Reasoning):\
                    yield self._format_json("reasoning", **chunk.get_dict())\
                elif isinstance(chunk, YouTube):\
                    yield self._format_json("content", chunk.to_string())\
                elif isinstance(chunk, AudioResponse):\
                    yield self._format_json("content", str(chunk))\
                elif isinstance(chunk, DebugResponse):\
                    yield self._format_json("log", chunk.log)\
                elif isinstance(chunk, RawResponse):\
                    yield self._format_json(chunk.type, **chunk.get_dict())\
                else:\
                    yield self._format_json("content", str(chunk))\
        except MissingAuthError as e:\
            yield self._format_json(\'auth\', type(e).__name__, message=get_error_message(e))\
        except Exception as e:\
            logger.exception(e)\
            debug.error(e)\
            yield self._format_json(\'error\', type(e).__name__, message=get_error_message(e))\
        finally:\
            yield from self._yield_logs()
```

**Назначение**: Создает поток ответов на основе переданных аргументов.

**Параметры**:
- `kwargs` (dict): Словарь с аргументами для создания ответа.
- `conversation_id` (str): Идентификатор беседы.
- `provider` (str): Имя провайдера.
- `download_media` (bool, optional): Флаг, указывающий, нужно ли загружать медиафайлы. По умолчанию `True`.

**Возвращает**:
- `Iterator`: Итератор, генерирующий ответы в формате JSON.

**Как работает функция**:

```
     Установка обработчика логирования
     │
     Получение G4F_PROXY из окружения
     │
     Получение model и provider_handler через get_model_and_provider
     │
     Обработка ошибок получения model и provider_handler
     │
     Проверка: provider_handler - экземпляр BaseRetryProvider?
     │
     │ нет
     │
     Обработка provider_handler
     │
     Получение параметров провайдера
     │
     Получение результата через iter_run_tools(ChatCompletion.create)
     │
     Обработка чанков результата
     │
     Проверка типа чанка: ProviderInfo, BaseConversation, Exception, RequestLogin, PreviewResponse, ImagePreview, MediaResponse, SynthesizeData, TitleGeneration, Parameters, FinishReason, Usage, Reasoning, YouTube, AudioResponse, DebugResponse, RawResponse
     │
     Форматирование и отправка JSON ответа в зависимости от типа чанка
     │
     Обработка MissingAuthError
     │
     Обработка общих исключений
     │
     Завершение: yield from self._yield_logs()
```

1. Устанавливается обработчик логирования для отладки.
2. Получается значение переменной окружения `G4F_PROXY`.
3. С помощью функции `get_model_and_provider` извлекаются модель и обработчик провайдера на основе предоставленных аргументов.
4. В случае возникновения исключения при получении модели или провайдера, формируется JSON-ответ с информацией об ошибке.
5. Проверяется, является ли `provider_handler` экземпляром `BaseRetryProvider`. Если нет, вызывается метод `handle_provider` для форматирования информации о провайдере.
6. Вызывается функция `iter_run_tools` для получения результата генерации текста или изображений.
7. Результат итерируется по чанкам, и в зависимости от типа чанка формируется соответствующий JSON-ответ:
   - `ProviderInfo`: информация о провайдере.
   - `BaseConversation`: информация о беседе.
   - `Exception`: сообщение об ошибке.
   - `RequestLogin`, `PreviewResponse`, `ImagePreview`: информация для предварительного просмотра.
   - `MediaResponse`: информация о медиафайлах (изображениях, видео).
   - `SynthesizeData`, `TitleGeneration`, `Parameters`, `FinishReason`, `Usage`, `Reasoning`, `YouTube`, `AudioResponse`, `DebugResponse`, `RawResponse`: различные типы данных для форматирования ответа.
8. В случае возникновения исключения `MissingAuthError`, формируется JSON-ответ с информацией об ошибке аутентификации.
9. В случае возникновения других исключений, они логируются и формируется JSON-ответ с информацией об ошибке.
10. В завершение вызывается метод `_yield_logs` для отправки логов отладки.

**Внутренние функции**:
### `Api._create_response_stream.decorated_log`
```python
        def decorated_log(text: str, file = None):
            debug.logs.append(text)
            if debug.logging:
                debug.log_handler(text, file=file)
```

**Назначение**: Добавляет текст в логи отладки и, если включено логирование, обрабатывает его.

**Параметры**:
- `text` (str): Текст для логирования.
- `file`: Файл для логирования.

**Как работает функция**:
1. Добавляет текст в список логов отладки (`debug.logs`).
2. Если включено логирование (`debug.logging`), вызывает функцию `debug.log_handler` для обработки текста.

**Примеры**:
```python
decorated_log("Some debug text")
```

**Примеры**:
```python
kwargs = {
    "model": "gemini",
    "provider": "google",
    "messages": [{"role": "user", "content": "Hello"}]
}
conversation_id = "123"
provider = "google"
response_stream = Api()._create_response_stream(kwargs, conversation_id, provider)
for response in response_stream:
    print(response)
```

### `Api._yield_logs`

```python
    def _yield_logs(self):\
        if debug.logs:\
            for log in debug.logs:\
                yield self._format_json("log", log)\
            debug.logs = []
```

**Назначение**: Генерирует логи отладки.

**Параметры**:
- Нет параметров.

**Возвращает**:
- `Iterator`: Итератор, генерирующий логи отладки в формате JSON.

**Как работает функция**:
1. Функция проверяет, есть ли логи в списке `debug.logs`.
2. Если логи есть, функция перебирает их и генерирует JSON-ответ для каждого лога.
3. После отправки всех логов, список `debug.logs` очищается.

**Примеры**:
```python
logs_stream = Api()._yield_logs()
for log in logs_stream:
    print(log)
```

### `Api._format_json`

```python
    def _format_json(self, response_type: str, content = None, **kwargs):\
        if content is not None and isinstance(response_type, str):\
            return {\
                \'type\': response_type,\
                response_type: content,\
                **kwargs\
            }\
        return {\
            \'type\': response_type,\
            **kwargs\
        }
```

**Назначение**: Форматирует ответ в формате JSON.

**Параметры**:
- `response_type` (str): Тип ответа.
- `content`: Содержимое ответа.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `dict`: Словарь с отформатированным ответом в формате JSON.

**Как работает функция**:
1. Функция проверяет, есть ли содержимое ответа и является ли тип ответа строкой.
2. Если условия выполняются, функция создает словарь, содержащий тип ответа, содержимое ответа и дополнительные аргументы.
3. Если условия не выполняются, функция создает словарь, содержащий только тип ответа и дополнительные аргументы.

**Примеры**:
```python
json_response = Api()._format_json("message", "Hello", error="SomeError")
print(json_response)
```

### `Api.handle_provider`

```python
    def handle_provider(self, provider_handler, model):\
        if isinstance(provider_handler, BaseRetryProvider) and provider_handler.last_provider is not None:\
            provider_handler = provider_handler.last_provider\
        if model:\
            return self._format_json("provider", {**provider_handler.get_dict(), "model": model})\
        return self._format_json("provider", provider_handler.get_dict())
```

**Назначение**: Форматирует информацию о провайдере в формате JSON.

**Параметры**:
- `provider_handler`: Обработчик провайдера.
- `model`: Модель.

**Возвращает**:
- `dict`: Словарь с информацией о провайдере в формате JSON.

**Как работает функция**:
1. Если `provider_handler` является экземпляром `BaseRetryProvider` и у него есть атрибут `last_provider`, используется значение `last_provider`.
2. Если модель указана, функция создает словарь, содержащий информацию о провайдере и модели.
3. Если модель не указана, функция создает словарь, содержащий только информацию о провайдере.

**Примеры**:
```python
from ...Provider import Gemini

provider_info = Api().handle_provider(Gemini, "gemini-1.5-pro")
print(provider_info)
```

## Функции

### `get_error_message`

```python
def get_error_message(exception: Exception) -> str:\
    return f"{type(exception).__name__}: {exception}"
```

**Назначение**: Форматирует сообщение об ошибке на основе переданного исключения.

**Параметры**:
- `exception` (Exception): Исключение, для которого нужно сформировать сообщение.

**Возвращает**:
- `str`: Отформатированное сообщение об ошибке.

**Как работает функция**:
1. Функция извлекает имя типа исключения и само исключение.
2. Формирует строку с именем типа исключения и сообщением исключения.

**Примеры**:
```python
try:
    raise ValueError("Invalid value")
except ValueError as ex:
    error_message = get_error_message(ex)
    print(error_message)
```
```
ValueError: Invalid value
```
```