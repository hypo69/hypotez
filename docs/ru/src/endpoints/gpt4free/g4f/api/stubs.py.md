# Модуль stubs.py

## Обзор

Модуль `stubs.py` содержит определения моделей данных, используемых для конфигурации и обмена данными с API g4f (gpt4free). Включает модели для конфигурации чат-запросов, генерации изображений, а также модели ответов от провайдеров, моделей и ошибок.
Все модели определены с использованием `pydantic.BaseModel` для валидации и управления данными.

## Подробней

Этот модуль предоставляет структуры данных, необходимые для взаимодействия с различными API, предоставляемыми g4f. Он определяет, как должны быть структурированы запросы к API и как ожидать ответы от них.

## Классы

### `ChatCompletionsConfig`

**Описание**: Класс конфигурации для запросов чат-завершений. Определяет структуру данных, необходимую для отправки запросов на генерацию текста.

**Аттрибуты**:

- `messages` (Messages): Список сообщений для чата. Содержит историю разговора. Пример: `[{"role": "system", "content": ""}, {"role": "user", "content": ""}]`.
- `model` (str): Идентификатор используемой модели. По умолчанию "".
- `provider` (Optional[str]): Провайдер модели. По умолчанию `None`.
- `stream` (bool): Флаг потоковой передачи данных. По умолчанию `False`.
- `image` (Optional[str]): URL изображения. По умолчанию `None`.
- `image_name` (Optional[str]): Имя изображения. По умолчанию `None`.
- `images` (Optional[list[tuple[str, str]]]): Список кортежей (URL, имя) изображений. По умолчанию `None`.
- `media` (Optional[list[tuple[str, str]]]): Список кортежей (URL, имя) медиафайлов. По умолчанию `None`.
- `modalities` (Optional[list[str]]): Список поддерживаемых модальностей (например, "text", "audio"). По умолчанию `["text", "audio"]`.
- `temperature` (Optional[float]): Температура модели. По умолчанию `None`.
- `presence_penalty` (Optional[float]): Штраф за присутствие. По умолчанию `None`.
- `frequency_penalty` (Optional[float]): Штраф за частоту. По умолчанию `None`.
- `top_p` (Optional[float]): Top-p значение. По умолчанию `None`.
- `max_tokens` (Optional[int]): Максимальное количество токенов в ответе. По умолчанию `None`.
- `stop` (Union[list[str], str, None]): Условие остановки генерации. Может быть списком строк, строкой или `None`. По умолчанию `None`.
- `api_key` (Optional[str]): Ключ API. По умолчанию `None`.
- `api_base` (str): Базовый URL API. По умолчанию `None`.
- `web_search` (Optional[bool]): Флаг использования веб-поиска. По умолчанию `None`.
- `proxy` (Optional[str]): URL прокси-сервера. По умолчанию `None`.
- `conversation_id` (Optional[str]): Идентификатор разговора. По умолчанию `None`.
- `conversation` (Optional[dict]): Словарь с данными разговора. По умолчанию `None`.
- `return_conversation` (Optional[bool]): Флаг возврата данных разговора. По умолчанию `None`.
- `history_disabled` (Optional[bool]): Флаг отключения истории. По умолчанию `None`.
- `timeout` (Optional[int]): Время ожидания ответа. По умолчанию `None`.
- `tool_calls` (list): Список вызовов инструментов. Пример: `[{ "function": { "arguments": {"query":"search query", "max_results":5, "max_words": 2500, "backend": "auto", "add_text": True, "timeout": 5}, "name": "search_tool" }, "type": "function" }]`.
- `tools` (list): Список доступных инструментов. По умолчанию `None`.
- `parallel_tool_calls` (bool): Флаг параллельных вызовов инструментов. По умолчанию `None`.
- `tool_choice` (Optional[str]): Выбор инструмента. По умолчанию `None`.
- `reasoning_effort` (Optional[str]): Уровень усилий при рассуждении. По умолчанию `None`.
- `logit_bias` (Optional[dict]): Смещение логитов. По умолчанию `None`.
- `modalities` (Optional[list[str]]): Список модальностей. По умолчанию `None`.
- `audio` (Optional[dict]): Конфигурация аудио. По умолчанию `None`.
- `response_format` (Optional[dict]): Формат ответа. По умолчанию `None`.
- `extra_data` (Optional[dict]): Дополнительные данные. По умолчанию `None`.

### `ImageGenerationConfig`

**Описание**: Класс конфигурации для запросов генерации изображений. Определяет структуру данных, необходимую для отправки запросов на создание изображений.

**Аттрибуты**:

- `prompt` (str): Текст запроса для генерации изображения.
- `model` (Optional[str]): Идентификатор используемой модели. По умолчанию `None`.
- `provider` (Optional[str]): Провайдер модели. По умолчанию `None`.
- `response_format` (Optional[str]): Формат ответа. По умолчанию `None`.
- `api_key` (Optional[str]): Ключ API. По умолчанию `None`.
- `proxy` (Optional[str]): URL прокси-сервера. По умолчанию `None`.
- `width` (Optional[int]): Ширина изображения. По умолчанию `None`.
- `height` (Optional[int]): Высота изображения. По умолчанию `None`.
- `num_inference_steps` (Optional[int]): Количество шагов инференса. По умолчанию `None`.
- `seed` (Optional[int]): Зерно для генерации. По умолчанию `None`.
- `guidance_scale` (Optional[int]): Масштаб соответствия запросу. По умолчанию `None`.
- `aspect_ratio` (Optional[str]): Соотношение сторон изображения. По умолчанию `None`.
- `n` (Optional[int]): Количество генерируемых изображений. По умолчанию `None`.
- `negative_prompt` (Optional[str]): Негативный запрос. По умолчанию `None`.
- `resolution` (Optional[str]): Разрешение изображения. По умолчанию `None`.

### `ProviderResponseModel`

**Описание**: Базовая модель ответа от провайдера. Содержит общую информацию об ответе.

**Аттрибуты**:

- `id` (str): Идентификатор ответа.
- `object` (str): Тип объекта. Всегда "provider".
- `created` (int): Время создания.
- `url` (Optional[str]): URL ресурса. По умолчанию `None`.
- `label` (Optional[str]): Метка. По умолчанию `None`.

### `ProviderResponseDetailModel`

**Описание**: Модель подробного ответа от провайдера. Наследует `ProviderResponseModel` и добавляет информацию о моделях и параметрах.

**Наследует**:

- `ProviderResponseModel`

**Аттрибуты**:

- `models` (list[str]): Список идентификаторов моделей.
- `image_models` (list[str]): Список идентификаторов моделей изображений.
- `vision_models` (list[str]): Список идентификаторов моделей vision.
- `params` (list[str]): Список параметров.

### `ModelResponseModel`

**Описание**: Модель ответа о модели. Содержит информацию о конкретной модели.

**Аттрибуты**:

- `id` (str): Идентификатор модели.
- `object` (str): Тип объекта. Всегда "model".
- `created` (int): Время создания.
- `owned_by` (Optional[str]): Владелец модели. По умолчанию `None`.

### `UploadResponseModel`

**Описание**: Модель ответа на загрузку файла. Содержит информацию о загруженном файле.

**Аттрибуты**:

- `bucket_id` (str): Идентификатор бакета.
- `url` (str): URL загруженного файла.

### `ErrorResponseModel`

**Описание**: Модель ответа об ошибке. Содержит информацию об ошибке.

**Аттрибуты**:

- `error` (ErrorResponseMessageModel): Сообщение об ошибке.
- `model` (Optional[str]): Идентификатор модели, вызвавшей ошибку. По умолчанию `None`.
- `provider` (Optional[str]): Провайдер, вызвавший ошибку. По умолчанию `None`.

### `ErrorResponseMessageModel`

**Описание**: Модель сообщения об ошибке. Содержит текст сообщения об ошибке.

**Аттрибуты**:

- `message` (str): Текст сообщения об ошибке.

### `FileResponseModel`

**Описание**: Модель ответа о файле.

**Аттрибуты**:

- `filename` (str): Имя файла.