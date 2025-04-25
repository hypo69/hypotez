# Модуль stubs

## Обзор

Этот модуль содержит определения типов для различных конфигурационных параметров, используемых в проекте `hypotez`. Он определяет классы `BaseModel` (pydantic) для представления различных конфигурационных параметров, таких как:

- Параметры для генерации текста с помощью API `ChatCompletionsConfig` 
- Параметры для генерации изображений с помощью API `ImageGenerationConfig`
- Параметры для работы с различными провайдерами (`ProviderResponseModel`, `ProviderResponseDetailModel`, `ModelResponseModel`)
- Модели ответа на запросы `UploadResponseModel`, `ErrorResponseModel`, `ErrorResponseMessageModel`, `FileResponseModel`

## Подробнее

Этот модуль обеспечивает типизированные модели для представления различных конфигурационных параметров, используемых в проекте. Типизированные модели предоставляют структурированный способ определения параметров и их типов.

## Классы

### `ChatCompletionsConfig`

**Описание**:  Модель, которая определяет конфигурационные параметры для генерации текста с помощью API. 

**Атрибуты**:

- `messages` (Messages): Список сообщений в чате. Пример: `[{"role": "system", "content": ""}, {"role": "user", "content": ""}]`
- `model` (str): Имя модели, которая будет использоваться для генерации текста.
- `provider` (Optional[str]): Провайдер AI-модели. 
- `stream` (bool): Флаг, указывающий, следует ли использовать потоковую передачу текста. 
- `image` (Optional[str]): URL изображения для обработки. 
- `image_name` (Optional[str]): Имя изображения для обработки.
- `images` (Optional[list[tuple[str, str]]]): Список изображений для обработки. 
- `media` (Optional[list[tuple[str, str]]]): Список медиа-файлов для обработки.
- `modalities` (Optional[list[str]]): Список режимов обработки, например, "text", "audio". 
- `temperature` (Optional[float]): Температура, влияющая на креативность ответа.
- `presence_penalty` (Optional[float]): Штраф за присутствие токена в ответе.
- `frequency_penalty` (Optional[float]): Штраф за частоту появления токена в ответе.
- `top_p` (Optional[float]): Вероятность выбора токена для генерации.
- `max_tokens` (Optional[int]): Максимальное количество токенов в ответе. 
- `stop` (Union[list[str], str, None]): Список стоп-слов для генерации. 
- `api_key` (Optional[str]): Ключ API для доступа к AI-модели.
- `api_base` (str): Базовый URL для API.
- `web_search` (Optional[bool]): Флаг, указывающий, следует ли использовать веб-поиск.
- `proxy` (Optional[str]): Прокси-сервер для доступа к API.
- `conversation_id` (Optional[str]): ID текущей беседы.
- `conversation` (Optional[dict]): Данные о текущей беседе.
- `return_conversation` (Optional[bool]): Флаг, указывающий, следует ли вернуть данные о беседе.
- `history_disabled` (Optional[bool]): Флаг, указывающий, следует ли отключить историю.
- `timeout` (Optional[int]): Тайм-аут для запроса.
- `tool_calls` (list): Список вызовов инструментов.
- `tools` (list): Список доступных инструментов.
- `parallel_tool_calls` (bool): Флаг, указывающий, следует ли выполнять вызовы инструментов параллельно.
- `tool_choice` (Optional[str]): Выбранный инструмент.
- `reasoning_effort` (Optional[str]): Уровень усилий для рассуждений.
- `logit_bias` (Optional[dict]): Смещение для логгирования вероятностей токенов.
- `modalities` (Optional[list[str]]): Список режимов обработки.
- `audio` (Optional[dict]): Конфигурация для обработки аудио.
- `response_format` (Optional[dict]): Формат ответа. 
- `extra_data` (Optional[dict]): Дополнительные данные.

### `ImageGenerationConfig`

**Описание**: Модель, которая определяет конфигурационные параметры для генерации изображений с помощью API.

**Атрибуты**:

- `prompt` (str): Текстовый запрос для генерации изображения.
- `model` (Optional[str]): Имя модели, которая будет использоваться для генерации изображения.
- `provider` (Optional[str]): Провайдер AI-модели. 
- `response_format` (Optional[str]): Формат ответа. 
- `api_key` (Optional[str]): Ключ API для доступа к AI-модели.
- `proxy` (Optional[str]): Прокси-сервер для доступа к API.
- `width` (Optional[int]): Ширина генерируемого изображения.
- `height` (Optional[int]): Высота генерируемого изображения.
- `num_inference_steps` (Optional[int]): Количество шагов инференса. 
- `seed` (Optional[int]): Случайное число для генерации.
- `guidance_scale` (Optional[int]): Шкала направляющего сигнала. 
- `aspect_ratio` (Optional[str]): Соотношение сторон изображения.
- `n` (Optional[int]): Количество генерируемых изображений.
- `negative_prompt` (Optional[str]): Текстовый запрос для генерации изображения, но с обратным значением. 
- `resolution` (Optional[str]): Разрешение изображения. 

### `ProviderResponseModel`

**Описание**:  Модель, которая представляет информацию о провайдере AI-модели.

**Атрибуты**:

- `id` (str): Идентификатор провайдера.
- `object` (str): Тип объекта - "provider".
- `created` (int): Время создания провайдера.
- `url` (Optional[str]): URL провайдера.
- `label` (Optional[str]): Название провайдера.

### `ProviderResponseDetailModel`

**Описание**: Модель, которая представляет более подробную информацию о провайдере AI-модели.

**Атрибуты**:

- `id` (str): Идентификатор провайдера.
- `object` (str): Тип объекта - "provider".
- `created` (int): Время создания провайдера.
- `url` (Optional[str]): URL провайдера.
- `label` (Optional[str]): Название провайдера.
- `models` (list[str]): Список доступных моделей.
- `image_models` (list[str]): Список доступных моделей для генерации изображений.
- `vision_models` (list[str]): Список доступных моделей для обработки изображений.
- `params` (list[str]): Список доступных параметров.

### `ModelResponseModel`

**Описание**: Модель, которая представляет информацию о модели AI-модели.

**Атрибуты**:

- `id` (str): Идентификатор модели.
- `object` (str): Тип объекта - "model".
- `created` (int): Время создания модели.
- `owned_by` (Optional[str]): Идентификатор владельца модели.

### `UploadResponseModel`

**Описание**: Модель, которая представляет результат загрузки файла.

**Атрибуты**:

- `bucket_id` (str): Идентификатор хранилища.
- `url` (str): URL загруженного файла.

### `ErrorResponseModel`

**Описание**: Модель, которая представляет ошибку, возникшую при работе с API.

**Атрибуты**:

- `error` (ErrorResponseMessageModel): Сообщение об ошибке.
- `model` (Optional[str]): Имя модели, которая вызвала ошибку.
- `provider` (Optional[str]): Провайдер AI-модели, который вызвал ошибку.

### `ErrorResponseMessageModel`

**Описание**:  Модель, которая представляет сообщение об ошибке.

**Атрибуты**:

- `message` (str): Текст сообщения об ошибке.

### `FileResponseModel`

**Описание**: Модель, которая представляет информацию о файле.

**Атрибуты**:

- `filename` (str): Имя файла.