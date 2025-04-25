# Модуль обработки ответов от gpt4free

## Обзор

Этот модуль содержит классы, которые используются для обработки ответов от API gpt4free. Он предоставляет механизмы для преобразования сырых ответов в различные типы данных, таких как Markdown, HTML,  JSON и др. 

## Подробнее

Модуль `response.py` предоставляет классы для обработки ответов от различных провайдеров, таких как gpt4free, OpenAI, Google Gemini. 
Он предоставляет механизм преобразования сырых ответов в различные типы данных, таких как Markdown, HTML,  JSON и др. 
В модуле используются абстрактные классы `ResponseType` и `JsonMixin`. 

## Классы

### `class ResponseType`

**Описание**: Абстрактный класс, определяющий базовую структуру для всех типов ответов.

**Методы**:

- `__str__(self) -> str`:  Преобразует ответ в строковое представление.

### `class JsonMixin`

**Описание**: Класс, реализующий методы для работы с JSON данными.

**Атрибуты**:

- `kwargs`:  Словары с  ключ-значение, используемые для инициализации. 

**Методы**:

- `__init__(self, **kwargs) -> None`:  Инициализирует класс с помощью ключевых аргументов.
- `get_dict(self) -> Dict`: Возвращает словарь с атрибутами класса.
- `reset(self) -> None`: Сбрасывает все атрибуты.

### `class RawResponse(ResponseType, JsonMixin)`

**Описание**: Класс, представляющий сырой ответ, который не требует дополнительной обработки.

### `class HiddenResponse(ResponseType)`

**Описание**: Класс, представляющий скрытые ответы, которые не отображаются пользователю.

**Методы**:

- `__str__(self) -> str`:  Возвращает пустую строку.

### `class FinishReason(JsonMixin, HiddenResponse)`

**Описание**: Класс, представляющий причину завершения запроса.

**Атрибуты**:

- `reason (str)`:  Причина завершения запроса.

### `class ToolCalls(HiddenResponse)`

**Описание**: Класс, представляющий список вызовов инструментов.

**Атрибуты**:

- `list (List)`:  Список вызовов инструментов.

**Методы**:

- `get_list(self) -> List`: Возвращает список вызовов инструментов.

### `class Usage(JsonMixin, HiddenResponse)`

**Описание**: Класс, представляющий информацию об использовании.

### `class AuthResult(JsonMixin, HiddenResponse)`

**Описание**: Класс, представляющий результат аутентификации.

### `class TitleGeneration(HiddenResponse)`

**Описание**: Класс, представляющий сгенерированный заголовок.

**Атрибуты**:

- `title (str)`:  Сгенерированный заголовок.

### `class DebugResponse(HiddenResponse)`

**Описание**: Класс, представляющий отладочную информацию.

**Атрибуты**:

- `log (str)`:  Сообщение отладки.

### `class Reasoning(ResponseType)`

**Описание**: Класс, представляющий результат рассуждения.

**Атрибуты**:

- `token (Optional[str])`:  Идентификатор токена.
- `label (Optional[str])`:  Метка.
- `status (Optional[str])`:  Статус.
- `is_thinking (Optional[str])`:  Признак того, что модель думает.

**Методы**:

- `__str__(self) -> str`:  Возвращает строковое представление результата рассуждения.
- `__eq__(self, other: Reasoning)`: Проверяет равенство двух объектов `Reasoning`.
- `get_dict(self) -> Dict`: Возвращает словарь с атрибутами результата рассуждения.

### `class Sources(ResponseType)`

**Описание**: Класс, представляющий список источников.

**Атрибуты**:

- `list (List[Dict[str, str]])`:  Список словарей с информацией об источниках.

**Методы**:

- `__init__(self, sources: List[Dict[str, str]]) -> None`: Инициализирует класс со списком словарей источников.
- `add_source(self, source: Union[Dict[str, str], str]) -> None`: Добавляет источник в список, очищая URL, если необходимо.
- `__str__(self) -> str`:  Возвращает отформатированные источники в виде строки.

### `class YouTube(HiddenResponse)`

**Описание**: Класс, представляющий список идентификаторов видео YouTube.

**Атрибуты**:

- `ids (List[str])`:  Список идентификаторов видео YouTube.

**Методы**:

- `to_string(self) -> str`: Возвращает встраивание видео YouTube в виде строки.

### `class AudioResponse(ResponseType)`

**Описание**: Класс, представляющий аудиоответ.

**Атрибуты**:

- `data (Union[bytes, str])`:  Аудиоданные в виде байтов.

**Методы**:

- `to_uri(self) -> str`:  Преобразует аудиоданные в URI base64.
- `__str__(self) -> str`:  Возвращает аудио в виде HTML-элемента.

### `class BaseConversation(ResponseType)`

**Описание**: Класс, представляющий базовую структуру для конверсаций.

**Методы**:

- `__str__(self) -> str`:  Возвращает пустую строку по умолчанию.

### `class JsonConversation(BaseConversation, JsonMixin)`

**Описание**: Класс, представляющий конверсацию в формате JSON.

### `class SynthesizeData(HiddenResponse, JsonMixin)`

**Описание**: Класс, представляющий синтезированные данные.

**Атрибуты**:

- `provider (str)`:  Провайдер синтезированных данных.
- `data (Dict)`:  Синтезированные данные.

### `class SuggestedFollowups(HiddenResponse)`

**Описание**: Класс, представляющий список предложений продолжения.

**Атрибуты**:

- `suggestions (list[str])`:  Список предложений продолжения.

### `class RequestLogin(HiddenResponse)`

**Описание**: Класс, представляющий запрос на вход.

**Атрибуты**:

- `label (str)`:  Метка запроса на вход.
- `login_url (str)`:  URL для входа.

**Методы**:

- `to_string(self) -> str`:  Возвращает отформатированную ссылку на вход в виде строки.

### `class MediaResponse(ResponseType)`

**Описание**: Класс, представляющий ответ с медиаданными.

**Атрибуты**:

- `urls (Union[str, List[str]])`:  URL медиафайла (изображения, видео) или список URL.
- `alt (str)`:  Альтернативный текст для медиафайла.
- `options (Dict)`:  Дополнительноие параметры для медиафайла. 

**Методы**:

- `get(self, key: str) -> any`:  Возвращает значение опции по ключу.
- `get_list(self) -> List[str]`:  Возвращает медиафайлы в виде списка.

### `class ImageResponse(MediaResponse)`

**Описание**: Класс, представляющий ответ с изображением.

**Методы**:

- `__str__(self) -> str`:  Возвращает изображение в виде Markdown.

### `class VideoResponse(MediaResponse)`

**Описание**: Класс, представляющий ответ с видео.

**Методы**:

- `__str__(self) -> str`:  Возвращает видео в виде HTML-элемента.

### `class ImagePreview(ImageResponse)`

**Описание**: Класс, представляющий предварительный просмотр изображения.

**Методы**:

- `__str__(self) -> str`:  Возвращает пустую строку для предварительного просмотра.
- `to_string(self) -> str`:  Возвращает изображение в виде Markdown.

### `class PreviewResponse(HiddenResponse)`

**Описание**: Класс, представляющий предварительный просмотр.

**Атрибуты**:

- `data (str)`:  Данные предварительного просмотра.

**Методы**:

- `to_string(self) -> str`:  Возвращает данные предварительного просмотра в виде строки.

### `class Parameters(ResponseType, JsonMixin)`

**Описание**: Класс, представляющий параметры.

**Методы**:

- `__str__(self) -> str`:  Возвращает пустую строку.

### `class ProviderInfo(JsonMixin, HiddenResponse)`

**Описание**: Класс, представляющий информацию о провайдере.

## Функции

### `quote_url(url: str) -> str`

**Назначение**:  Преобразует URL в закодированный вид, сохраняя структуру домена.

**Параметры**:

- `url (str)`: URL для кодирования.

**Возвращает**:

- `str`: Закодированный URL.

**Как работает функция**:

- Сначала функция декодирует URL, если в нем есть символы `%`, чтобы избежать двойного декодирования.
- Затем она разделяет URL по символу `//`, чтобы получить протокол и оставшуюся часть URL.
- Если в URL нет символа `//`, то это относительный URL, который кодируется без изменений.
- Если в URL есть символ `//`, то функция разделяет оставшуюся часть URL по символу `/`, чтобы получить домен и путь.
- Домен кодируется без изменений, а путь кодируется с помощью `quote_plus`, чтобы сохранить структуру пути.
- В конце функция формирует финальный URL, объединяя закодированные части.

**Примеры**:

```python
>>> quote_url("https://www.example.com/path/to/file")
'https://www.example.com/path/to/file'

>>> quote_url("http://example.com/path%20with%20spaces")
'http://example.com/path%20with%20spaces'

>>> quote_url("relative/path")
'relative/path'
```

### `quote_title(title: str) -> str`

**Назначение**: Нормализует пробелы в заголовке.

**Параметры**:

- `title (str)`:  Заголовок для нормализации.

**Возвращает**:

- `str`: Заголовок с нормализованными пробелами.

**Как работает функция**:

- Функция разделяет заголовок по пробелам и объединяет полученные части обратно, используя один пробел в качестве разделителя.

**Примеры**:

```python
>>> quote_title("  Example Title  ")
'Example Title'

>>> quote_title("Example   Title")
'Example Title'
```

### `format_link(url: str, title: Optional[str] = None) -> str`

**Назначение**: Форматирует URL и заголовок как ссылку в формате Markdown.

**Параметры**:

- `url (str)`: URL для ссылки.
- `title (Optional[str])`: Заголовок для ссылки. Если `None`, извлекается из URL.

**Возвращает**:

- `str`: Отформатированная ссылка в формате Markdown.

**Как работает функция**:

- Если `title` не задан, функция извлекает заголовок из URL, удаляя протокол, домен и параметры запроса.
- Затем функция кодирует URL и заголовок с помощью функций `quote_url` и `quote_title` соответственно.
- В конце функция формирует финальную ссылку в формате Markdown, используя квадратные скобки для заголовка и круглые скобки для URL.

**Примеры**:

```python
>>> format_link("https://www.example.com/path/to/file", "Example File")
'[Example File](https://www.example.com/path/to/file)'

>>> format_link("https://www.example.com/path/to/file")
'[Example.com/path/to/file](https://www.example.com/path/to/file)'
```

### `format_image(image: str, alt: str, preview: Optional[str] = None) -> str`

**Назначение**: Форматирует изображение как строку в формате Markdown.

**Параметры**:

- `image (str)`: URL изображения.
- `alt (str)`: Альтернативный текст для изображения.
- `preview (Optional[str])`: URL для предварительного просмотра. По умолчанию используется URL изображения.

**Возвращает**:

- `str`: Отформатированная строка в формате Markdown.

**Как работает функция**:

- Функция кодирует URL изображения и URL предварительного просмотра с помощью функции `quote_url`.
- Затем она формирует строку в формате Markdown, используя синтаксис для изображения: `![alt text](image url)`.
- Если задан `preview`, то строка Markdown дополнительно содержит ссылку на `preview`: `[![alt text](preview url)](image url)`.

**Примеры**:

```python
>>> format_image("https://www.example.com/image.jpg", "Example Image")
'![Example Image](https://www.example.com/image.jpg)'

>>> format_image("https://www.example.com/image.jpg", "Example Image", "https://www.example.com/preview.jpg")
'[![Example Image](https://www.example.com/preview.jpg)](https://www.example.com/image.jpg)'
```

### `format_images_markdown(images: Union[str, List[str]], alt: str, preview: Union[str, List[str]] = None) -> str`

**Назначение**: Форматирует изображение или список изображений как строку в формате Markdown.

**Параметры**:

- `images (Union[str, List[str]])`: URL изображения или список URL изображений.
- `alt (str)`: Альтернативный текст для изображения.
- `preview (Union[str, List[str]])`: URL для предварительного просмотра или список URL для предварительного просмотра. Если не задан, используется URL изображения.

**Возвращает**:

- `str`: Отформатированная строка в формате Markdown.

**Как работает функция**:

- Если `images` является списком, а его длина равна 1, то функция преобразует его в строку.
- Если `images` является строкой, то функция использует функцию `format_image` для форматирования изображения.
- Если `images` является списком, то функция использует цикл `for` для форматирования каждого изображения в списке.
- В цикле функция форматирует каждое изображение, используя функцию `format_image`. 
- Для `alt` используется строка, которая включает номер изображения в списке.
- Если `preview` является списком, то функция использует соответствующий элемент из списка `preview` для каждого изображения. 
- В конце функция добавляет флаги `<!-- generated images start -->` и `<!-- generated images end -->` в начало и конец отформатированного текста.

**Примеры**:

```python
>>> format_images_markdown("https://www.example.com/image.jpg", "Example Image")
'\n<!-- generated images start -->\n[![Example Image](https://www.example.com/image.jpg)](https://www.example.com/image.jpg)\n<!-- generated images end -->\n'

>>> format_images_markdown(["https://www.example.com/image1.jpg", "https://www.example.com/image2.jpg"], "Example Image")
'\n<!-- generated images start -->\n[![#1 Example Image](https://www.example.com/image1.jpg)](https://www.example.com/image1.jpg)\n[![#2 Example Image](https://www.example.com/image2.jpg)](https://www.example.com/image2.jpg)\n<!-- generated images end -->\n'

>>> format_images_markdown(["https://www.example.com/image1.jpg", "https://www.example.com/image2.jpg"], "Example Image", ["https://www.example.com/preview1.jpg", "https://www.example.com/preview2.jpg"])
'\n<!-- generated images start -->\n[![#1 Example Image](https://www.example.com/preview1.jpg)](https://www.example.com/image1.jpg)\n[![#2 Example Image](https://www.example.com/preview2.jpg)](https://www.example.com/image2.jpg)\n<!-- generated images end -->\n'