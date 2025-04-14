# Модуль stubs.py

## Обзор

Модуль `stubs.py` содержит определения моделей данных, используемых для конфигурации и ответов API g4f (GPT4Free). Он включает в себя конфигурационные модели для чат-завершений и генерации изображений, а также модели ответов от провайдеров, моделей, загрузок файлов и ошибок.

## Подробнее

Этот модуль предоставляет структуры данных, необходимые для взаимодействия с API g4f. Он определяет, какие параметры можно передавать в запросах и какие данные можно ожидать в ответах. Использование `pydantic.BaseModel` обеспечивает валидацию данных и упрощает работу с API.

## Классы

### `ChatCompletionsConfig`

**Описание**: Конфигурационная модель для запросов чат-завершений. Определяет структуру данных для настройки запросов к API, включая сообщения, модель, провайдера и другие параметры.

**Атрибуты**:
- `messages` (Messages): Список сообщений для чат-завершения. Пример: `[[{"role": "system", "content": ""}, {"role": "user", "content": ""}]]`.
- `model` (str): Модель, используемая для завершения чата. По умолчанию "".
- `provider` (Optional[str]): Провайдер, используемый для завершения чата. По умолчанию `None`.
- `stream` (bool): Флаг, указывающий, следует ли использовать потоковую передачу. По умолчанию `False`.
- `image` (Optional[str]): Изображение, используемое в запросе. По умолчанию `None`.
- `image_name` (Optional[str]): Имя изображения, используемого в запросе. По умолчанию `None`.
- `images` (Optional[list[tuple[str, str]]]): Список изображений в формате (content_type, base64_encoded_data). По умолчанию `None`.
- `media` (Optional[list[tuple[str, str]]]): Список медиа-файлов в формате (content_type, base64_encoded_data). По умолчанию `None`.
- `modalities` (Optional[list[str]]): Список модальностей, используемых в запросе (например, "text", "audio"). По умолчанию `["text", "audio"]`.
- `temperature` (Optional[float]): Температура модели. По умолчанию `None`.
- `presence_penalty` (Optional[float]): Штраф за присутствие. По умолчанию `None`.
- `frequency_penalty` (Optional[float]): Штраф за частоту. По умолчанию `None`.
- `top_p` (Optional[float]): Top-p модели. По умолчанию `None`.
- `max_tokens` (Optional[int]): Максимальное количество токенов. По умолчанию `None`.
- `stop` (Union[list[str], str, None]): Список стоп-слов. По умолчанию `None`.
- `api_key` (Optional[str]): Ключ API. По умолчанию `None`.
- `api_base` (str): Базовый URL API. По умолчанию `None`.
- `web_search` (Optional[bool]): Флаг, указывающий, следует ли использовать веб-поиск. По умолчанию `None`.
- `proxy` (Optional[str]): Прокси-сервер. По умолчанию `None`.
- `conversation_id` (Optional[str]): Идентификатор разговора. По умолчанию `None`.
- `conversation` (Optional[dict]): Объект разговора. По умолчанию `None`.
- `return_conversation` (Optional[bool]): Флаг, указывающий, следует ли возвращать разговор. По умолчанию `None`.
- `history_disabled` (Optional[bool]): Флаг, указывающий, следует ли отключать историю. По умолчанию `None`.
- `timeout` (Optional[int]): Время ожидания. По умолчанию `None`.
- `tool_calls` (list): Список вызовов инструментов. Пример: `[[{"function": {"arguments": {"query":"search query", "max_results":5, "max_words": 2500, "backend": "auto", "add_text": True, "timeout": 5},"name": "search_tool"},"type": "function"}]]`. По умолчанию `[]`.
- `tools` (list): Список доступных инструментов. По умолчанию `None`.
- `parallel_tool_calls` (bool): Флаг, разрешающий параллельные вызовы инструментов. По умолчанию `None`.
- `tool_choice` (Optional[str]): Выбор инструмента. По умолчанию `None`.
- `reasoning_effort` (Optional[str]): Уровень усилий рассуждения. По умолчанию `None`.
- `logit_bias` (Optional[dict]): Смещение логитов. По умолчанию `None`.
- `modalities` (Optional[list[str]]): Список модальностей. По умолчанию `None`.
- `audio` (Optional[dict]): Аудио данные. По умолчанию `None`.
- `response_format` (Optional[dict]): Формат ответа. По умолчанию `None`.
- `extra_data` (Optional[dict]): Дополнительные данные. По умолчанию `None`.

### `ImageGenerationConfig`

**Описание**: Конфигурационная модель для запросов генерации изображений.

**Атрибуты**:
- `prompt` (str): Текст запроса для генерации изображения.
- `model` (Optional[str]): Модель, используемая для генерации изображения. По умолчанию `None`.
- `provider` (Optional[str]): Провайдер, используемый для генерации изображения. По умолчанию `None`.
- `response_format` (Optional[str]): Формат ответа. По умолчанию `None`.
- `api_key` (Optional[str]): Ключ API. По умолчанию `None`.
- `proxy` (Optional[str]): Прокси-сервер. По умолчанию `None`.
- `width` (Optional[int]): Ширина изображения. По умолчанию `None`.
- `height` (Optional[int]): Высота изображения. По умолчанию `None`.
- `num_inference_steps` (Optional[int]): Количество шагов вывода. По умолчанию `None`.
- `seed` (Optional[int]): Зерно для генерации случайных чисел. По умолчанию `None`.
- `guidance_scale` (Optional[int]): Масштаб направления. По умолчанию `None`.
- `aspect_ratio` (Optional[str]): Соотношение сторон изображения. По умолчанию `None`.
- `n` (Optional[int]): Количество сгенерированных изображений. По умолчанию `None`.
- `negative_prompt` (Optional[str]): Негативный запрос. По умолчанию `None`.
- `resolution` (Optional[str]): Разрешение изображения. По умолчанию `None`.

### `ProviderResponseModel`

**Описание**: Модель ответа от провайдера.

**Атрибуты**:
- `id` (str): Идентификатор провайдера.
- `object` (str): Тип объекта. Всегда "provider".
- `created` (int): Время создания.
- `url` (Optional[str]): URL. По умолчанию `None`.
- `label` (Optional[str]): Метка. По умолчанию `None`.

### `ProviderResponseDetailModel`

**Описание**: Модель детального ответа от провайдера, наследуется от `ProviderResponseModel`.

**Наследует**: `ProviderResponseModel`

**Атрибуты**:
- `models` (list[str]): Список моделей.
- `image_models` (list[str]): Список моделей изображений.
- `vision_models` (list[str]): Список моделей машинного зрения.
- `params` (list[str]): Список параметров.

### `ModelResponseModel`

**Описание**: Модель ответа от модели.

**Атрибуты**:
- `id` (str): Идентификатор модели.
- `object` (str): Тип объекта. Всегда "model".
- `created` (int): Время создания.
- `owned_by` (Optional[str]): Владелец. По умолчанию `None`.

### `UploadResponseModel`

**Описание**: Модель ответа на загрузку файла.

**Атрибуты**:
- `bucket_id` (str): Идентификатор бакета.
- `url` (str): URL.

### `ErrorResponseModel`

**Описание**: Модель ответа об ошибке.

**Атрибуты**:
- `error` (ErrorResponseMessageModel): Сообщение об ошибке.
- `model` (Optional[str]): Модель. По умолчанию `None`.
- `provider` (Optional[str]): Провайдер. По умолчанию `None`.

### `ErrorResponseMessageModel`

**Описание**: Модель сообщения об ошибке.

**Атрибуты**:
- `message` (str): Сообщение.

### `FileResponseModel`

**Описание**: Модель ответа файла.

**Атрибуты**:
- `filename` (str): Имя файла.