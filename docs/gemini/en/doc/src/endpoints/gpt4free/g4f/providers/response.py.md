# Модуль `response`
## Обзор

Модуль `response` в рамках проекта `hypotez` предназначен для обработки и форматирования различных типов ответов от моделей искусственного интеллекта, используемых в проекте. В нем реализованы классы, которые представляют собой различные типы ответов, включая:

- **`RawResponse`**:  Сырой ответ в формате JSON.
- **`HiddenResponse`**:  Скрытые ответы, не предназначенные для отображения пользователю.
- **`FinishReason`**:  Причина завершения работы модели.
- **`ToolCalls`**:  Список вызовов инструментов, использованных моделью.
- **`Usage`**:  Статистика использования модели.
- **`AuthResult`**:  Результат аутентификации.
- **`TitleGeneration`**:  Сгенерированный заголовок.
- **`DebugResponse`**:  Отладочные сообщения.
- **`Reasoning`**:  Ответ модели, который содержит токен, статус и состояние размышлений.
- **`Sources`**:  Список использованных источников.
- **`YouTube`**:  Список YouTube-видео, вставленных в ответ.
- **`AudioResponse`**:  Аудио-ответ в виде data URI.
- **`BaseConversation`**:  Базовый класс для ответов в виде чата.
- **`JsonConversation`**:  Ответ в формате JSON для чата.
- **`SynthesizeData`**:  Данные для синтеза речи.
- **`SuggestedFollowups`**:  Список предложенных продолжений.
- **`RequestLogin`**:  Запрос на авторизацию.
- **`MediaResponse`**:  Базовый класс для медиа-ответов (изображений, видео).
- **`ImageResponse`**:  Ответ с изображениями.
- **`VideoResponse`**:  Ответ с видео.
- **`ImagePreview`**:  Предварительный просмотр изображения.
- **`PreviewResponse`**:  Предварительный просмотр ответа.
- **`Parameters`**:  Дополнительные параметры.
- **`ProviderInfo`**:  Информация о провайдере.


## Содержание
  - [Классы](#Классы)
    - [`ResponseType`](#ResponseType)
    - [`JsonMixin`](#JsonMixin)
    - [`RawResponse`](#RawResponse)
    - [`HiddenResponse`](#HiddenResponse)
    - [`FinishReason`](#FinishReason)
    - [`ToolCalls`](#ToolCalls)
    - [`Usage`](#Usage)
    - [`AuthResult`](#AuthResult)
    - [`TitleGeneration`](#TitleGeneration)
    - [`DebugResponse`](#DebugResponse)
    - [`Reasoning`](#Reasoning)
    - [`Sources`](#Sources)
    - [`YouTube`](#YouTube)
    - [`AudioResponse`](#AudioResponse)
    - [`BaseConversation`](#BaseConversation)
    - [`JsonConversation`](#JsonConversation)
    - [`SynthesizeData`](#SynthesizeData)
    - [`SuggestedFollowups`](#SuggestedFollowups)
    - [`RequestLogin`](#RequestLogin)
    - [`MediaResponse`](#MediaResponse)
    - [`ImageResponse`](#ImageResponse)
    - [`VideoResponse`](#VideoResponse)
    - [`ImagePreview`](#ImagePreview)
    - [`PreviewResponse`](#PreviewResponse)
    - [`Parameters`](#Parameters)
    - [`ProviderInfo`](#ProviderInfo)
  - [Функции](#Функции)
    - [`quote_url(url: str) -> str`](#quote_urlurl-str--str)
    - [`quote_title(title: str) -> str`](#quote_titletitle-str--str)
    - [`format_link(url: str, title: Optional[str] = None) -> str`](#format_linkurl-str-title-optionalstr--none--str)
    - [`format_image(image: str, alt: str, preview: Optional[str] = None) -> str`](#format_imageimage-str-alt-str-preview-optionalstr--none--str)
    - [`format_images_markdown(images: Union[str, List[str]], alt: str, preview: Union[str, List[str]] = None) -> str`](#format_images_markdownimages-unionstr-liststr-alt-str-preview-unionstr-liststr--none--str)


## Классы

### `ResponseType`

```python
class ResponseType:
    @abstractmethod
    def __str__(self) -> str:
        """Convert the response to a string representation."""
        raise NotImplementedError
```

**Описание**: Базовый класс для всех типов ответов. Предоставляет абстрактный метод `__str__`, который должен быть переопределен в дочерних классах для преобразования ответа в строковое представление.

### `JsonMixin`

```python
class JsonMixin:
    def __init__(self, **kwargs) -> None:
        """Initialize with keyword arguments as attributes."""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_dict(self) -> Dict:
        """Return a dictionary of non-private attributes."""
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("__")
        }

    def reset(self) -> None:
        """Reset all attributes."""
        self.__dict__ = {}
```

**Описание**:  Класс, который предоставляет методы для работы с атрибутами объекта в формате JSON.

- **`__init__(self, **kwargs) -> None`**: Инициализирует объект с помощью аргументов ключевых слов, которые становятся атрибутами объекта.
- **`get_dict(self) -> Dict`**: Возвращает словарь, содержащий все не-приватные атрибуты объекта.
- **`reset(self) -> None`**: Сбрасывает все атрибуты объекта, очищая его состояние.


### `RawResponse`

```python
class RawResponse(ResponseType, JsonMixin):
    pass
```

**Описание**:  Класс, представляющий собой сырой ответ от модели. Наследует от `ResponseType` и `JsonMixin`. Используется для хранения ответа в первоначальном виде.

### `HiddenResponse`

```python
class HiddenResponse(ResponseType):
    def __str__(self) -> str:
        """Hidden responses return an empty string."""
        return ""
```

**Описание**:  Класс, представляющий собой скрытый ответ от модели. Наследует от `ResponseType` и возвращает пустую строку при преобразовании в строку. Используется для ответов, которые не должны отображаться пользователю.

### `FinishReason`

```python
class FinishReason(JsonMixin, HiddenResponse):
    def __init__(self, reason: str) -> None:
        """Initialize with a reason."""
        self.reason = reason
```

**Описание**:  Класс, представляющий собой причину завершения работы модели. Наследует от `JsonMixin` и `HiddenResponse`. Хранит причину завершения в атрибуте `reason`.

### `ToolCalls`

```python
class ToolCalls(HiddenResponse):
    def __init__(self, list: List) -> None:
        """Initialize with a list of tool calls."""
        self.list = list

    def get_list(self) -> List:
        """Return the list of tool calls."""
        return self.list
```

**Описание**:  Класс, представляющий собой список вызовов инструментов, использованных моделью. Наследует от `HiddenResponse`. Хранит список вызовов в атрибуте `list`.

### `Usage`

```python
class Usage(JsonMixin, HiddenResponse):
    pass
```

**Описание**:  Класс, представляющий собой статистику использования модели. Наследует от `JsonMixin` и `HiddenResponse`.

### `AuthResult`

```python
class AuthResult(JsonMixin, HiddenResponse):
    pass
```

**Описание**:  Класс, представляющий собой результат аутентификации. Наследует от `JsonMixin` и `HiddenResponse`.

### `TitleGeneration`

```python
class TitleGeneration(HiddenResponse):
    def __init__(self, title: str) -> None:
        """Initialize with a title."""
        self.title = title
```

**Описание**:  Класс, представляющий собой сгенерированный заголовок. Наследует от `HiddenResponse`. Хранит сгенерированный заголовок в атрибуте `title`.

### `DebugResponse`

```python
class DebugResponse(HiddenResponse):
    def __init__(self, log: str) -> None:
        """Initialize with a log message."""
        self.log = log
```

**Описание**:  Класс, представляющий собой отладочные сообщения. Наследует от `HiddenResponse`. Хранит сообщение в атрибуте `log`.

### `Reasoning`

```python
class Reasoning(ResponseType):
    def __init__(
            self,
            token: Optional[str] = None,
            label: Optional[str] = None,
            status: Optional[str] = None,
            is_thinking: Optional[str] = None
        ) -> None:
        """Initialize with token, status, and thinking state."""
        self.token = token
        self.label = label
        self.status = status
        self.is_thinking = is_thinking

    def __str__(self) -> str:
        """Return string representation based on available attributes."""
        if self.is_thinking is not None:
            return self.is_thinking
        if self.token is not None:
            return self.token
        if self.status is not None:
            if self.label is not None:
                return f"{self.label}: {self.status}\n"
            return f"{self.status}\n"
        return ""

    def __eq__(self, other: Reasoning):
        return (self.token == other.token and
                self.status == other.status and
                self.is_thinking == other.is_thinking)

    def get_dict(self) -> Dict:
        """Return a dictionary representation of the reasoning."""
        if self.label is not None:
            return {"label": self.label, "status": self.status}
        if self.is_thinking is None:
            if self.status is None:
                return {"token": self.token}
            return {"token": self.token, "status": self.status}
        return {"token": self.token, "status": self.status, "is_thinking": self.is_thinking}
```

**Описание**:  Класс, представляющий собой ответ модели, который содержит токен, статус и состояние размышлений. Наследует от `ResponseType`.

- **`__init__(self, token: Optional[str] = None, label: Optional[str] = None, status: Optional[str] = None, is_thinking: Optional[str] = None) -> None`**: Инициализирует объект с помощью токена, статуса, состояния размышлений и метки.
- **`__str__(self) -> str`**: Преобразует объект в строковое представление.
- **`__eq__(self, other: Reasoning)`**: Определяет равенство двух объектов `Reasoning`.
- **`get_dict(self) -> Dict`**: Возвращает словарь, содержащий атрибуты объекта.

### `Sources`

```python
class Sources(ResponseType):
    def __init__(self, sources: List[Dict[str, str]]) -> None:
        """Initialize with a list of source dictionaries."""
        self.list = []
        for source in sources:
            self.add_source(source)

    def add_source(self, source: Union[Dict[str, str], str]) -> None:
        """Add a source to the list, cleaning the URL if necessary."""
        source = source if isinstance(source, dict) else {"url": source}
        url = source.get("url", source.get("link", None))
        if url is not None:
            url = re.sub(r"[&?]utm_source=.+", "", url)
            source["url"] = url
            self.list.append(source)

    def __str__(self) -> str:
        """Return formatted sources as a string."""
        if not self.list:
            return ""
        return "\n\n\n\n" + ("\n>\n".join([
            f"> [{idx}] {format_link(link['url'], link.get('title', None))}"
            for idx, link in enumerate(self.list)
        ]))
```

**Описание**:  Класс, представляющий собой список использованных источников. Наследует от `ResponseType`.

- **`__init__(self, sources: List[Dict[str, str]]) -> None`**: Инициализирует объект с помощью списка словарей, содержащих информацию об источниках.
- **`add_source(self, source: Union[Dict[str, str], str]) -> None`**: Добавляет источник в список, очищая URL, если необходимо.
- **`__str__(self) -> str`**: Преобразует объект в строковое представление, форматируя список источников.

### `YouTube`

```python
class YouTube(HiddenResponse):
    def __init__(self, ids: List[str]) -> None:
        """Initialize with a list of YouTube IDs."""
        self.ids = ids

    def to_string(self) -> str:
        """Return YouTube embeds as a string."""
        if not self.ids:
            return ""
        return "\n\n" + ("\n".join([
            f'<iframe type="text/html" src="https://www.youtube.com/embed/{id}"></iframe>'
            for id in self.ids
        ]))
```

**Описание**:  Класс, представляющий собой список YouTube-видео, вставленных в ответ. Наследует от `HiddenResponse`.

- **`__init__(self, ids: List[str]) -> None`**: Инициализирует объект с помощью списка YouTube-ID.
- **`to_string(self) -> str`**: Преобразует объект в строковое представление, генерируя HTML-код для вставки YouTube-видео.

### `AudioResponse`

```python
class AudioResponse(ResponseType):
    def __init__(self, data: Union[bytes, str]) -> None:
        """Initialize with audio data bytes."""
        self.data = data

    def to_uri(self) -> str:
        if isinstance(self.data, str):
            return self.data
        """Return audio data as a base64-encoded data URI."""
        data_base64 = base64.b64encode(self.data).decode()
        return f"data:audio/mpeg;base64,{data_base64}"

    def __str__(self) -> str:
        """Return audio as html element."""
        return f'<audio controls src="{self.to_uri()}"></audio>'
```

**Описание**:  Класс, представляющий собой аудио-ответ в виде data URI. Наследует от `ResponseType`.

- **`__init__(self, data: Union[bytes, str]) -> None`**: Инициализирует объект с помощью аудио-данных в виде байтов или строки.
- **`to_uri(self) -> str`**: Преобразует аудио-данные в data URI.
- **`__str__(self) -> str`**: Преобразует объект в строковое представление, генерируя HTML-код для аудио-плеера.

### `BaseConversation`

```python
class BaseConversation(ResponseType):
    def __str__(self) -> str:
        """Return an empty string by default."""
        return ""
```

**Описание**:  Базовый класс для ответов в виде чата. Наследует от `ResponseType`.

### `JsonConversation`

```python
class JsonConversation(BaseConversation, JsonMixin):
    pass
```

**Описание**:  Класс, представляющий собой ответ в формате JSON для чата. Наследует от `BaseConversation` и `JsonMixin`.

### `SynthesizeData`

```python
class SynthesizeData(HiddenResponse, JsonMixin):
    def __init__(self, provider: str, data: Dict) -> None:
        """Initialize with provider and data."""
        self.provider = provider
        self.data = data
```

**Описание**:  Класс, представляющий собой данные для синтеза речи. Наследует от `HiddenResponse` и `JsonMixin`.

### `SuggestedFollowups`

```python
class SuggestedFollowups(HiddenResponse):
    def __init__(self, suggestions: list[str]):
        self.suggestions = suggestions
```

**Описание**:  Класс, представляющий собой список предложенных продолжений. Наследует от `HiddenResponse`.

### `RequestLogin`

```python
class RequestLogin(HiddenResponse):
    def __init__(self, label: str, login_url: str) -> None:
        """Initialize with label and login URL."""
        self.label = label
        self.login_url = login_url

    def to_string(self) -> str:
        """Return formatted login link as a string."""
        return format_link(self.login_url, f"[Login to {self.label}]") + "\n\n"
```

**Описание**:  Класс, представляющий собой запрос на авторизацию. Наследует от `HiddenResponse`.

### `MediaResponse`

```python
class MediaResponse(ResponseType):
    def __init__(
        self,
        urls: Union[str, List[str]],
        alt: str,
        options: Dict = {},
        **kwargs
    ) -> None:
        """Initialize with images, alt text, and options."""
        self.urls = kwargs.get("images", urls)
        self.alt = alt
        self.options = options

    def get(self, key: str) -> any:
        """Get an option value by key."""
        return self.options.get(key)

    def get_list(self) -> List[str]:
        """Return images as a list."""
        return [self.urls] if isinstance(self.urls, str) else self.urls
```

**Описание**:  Базовый класс для медиа-ответов (изображений, видео). Наследует от `ResponseType`.

### `ImageResponse`

```python
class ImageResponse(MediaResponse):
    def __str__(self) -> str:
        """Return images as markdown."""
        return format_images_markdown(self.urls, self.alt, self.get("preview"))
```

**Описание**:  Класс, представляющий собой ответ с изображениями. Наследует от `MediaResponse`.

### `VideoResponse`

```python
class VideoResponse(MediaResponse):
    def __str__(self) -> str:
        """Return videos as html elements."""
        return "\n".join([f'<video controls src="{video}"></video>' for video in self.get_list()])
```

**Описание**:  Класс, представляющий собой ответ с видео. Наследует от `MediaResponse`.

### `ImagePreview`

```python
class ImagePreview(ImageResponse):
    def __str__(self) -> str:
        """Return an empty string for preview."""
        return ""

    def to_string(self) -> str:
        """Return images as markdown."""
        return super().__str__()
```

**Описание**:  Класс, представляющий собой предварительный просмотр изображения. Наследует от `ImageResponse`.

### `PreviewResponse`

```python
class PreviewResponse(HiddenResponse):
    def __init__(self, data: str) -> None:
        """Initialize with data."""
        self.data = data

    def to_string(self) -> str:
        """Return data as a string."""
        return self.data
```

**Описание**:  Класс, представляющий собой предварительный просмотр ответа. Наследует от `HiddenResponse`.

### `Parameters`

```python
class Parameters(ResponseType, JsonMixin):
    def __str__(self) -> str:
        """Return an empty string."""
        return ""
```

**Описание**:  Класс, представляющий собой дополнительные параметры. Наследует от `ResponseType` и `JsonMixin`.

### `ProviderInfo`

```python
class ProviderInfo(JsonMixin, HiddenResponse):
    pass
```

**Описание**:  Класс, представляющий собой информацию о провайдере. Наследует от `JsonMixin` и `HiddenResponse`.

## Функции

### `quote_url(url: str) -> str`

```python
def quote_url(url: str) -> str:
    """
    Quote parts of a URL while preserving the domain structure.

    Args:
        url: The URL to quote

    Returns:
        str: The properly quoted URL
    """
    # Only unquote if needed to avoid double-unquoting
    if '%' in url:
        url = unquote_plus(url)

    url_parts = url.split("//", maxsplit=1)
    # If there is no "//" in the URL, then it is a relative URL
    if len(url_parts) == 1:
        return quote_plus(url_parts[0], '/?&=#')

    protocol, rest = url_parts
    domain_parts = rest.split("/", maxsplit=1)
    # If there is no "/" after the domain, then it is a domain URL
    if len(domain_parts) == 1:
        return f"{protocol}//{domain_parts[0]}"

    domain, path = domain_parts
    return f"{protocol}//{domain}/{quote_plus(path, '/?&=#')}"
```

**Описание**:  Функция кодирует URL, сохраняя структуру домена.

**Параметры**:

- `url` (str):  URL для кодирования.

**Возвращаемое значение**:

- `str`:  Закодированный URL.

**Как работает**:

- Функция сначала проверяет, содержит ли URL символ `%`. Если да, то она декодирует URL, чтобы избежать двойного декодирования.
- Затем функция разделяет URL на протокол и остальную часть, используя `//` как разделитель.
- Если в URL нет `//`, то это относительный URL, и функция кодирует его, используя `quote_plus`.
- Если есть `//`, то функция разделяет остальную часть URL на домен и путь, используя `/` как разделитель.
- Если после домена нет `/`, то это URL домена, и функция возвращает его без кодирования.
- Если после домена есть `/`, то функция кодирует путь, используя `quote_plus`, и возвращает полный URL.

### `quote_title(title: str) -> str`

```python
def quote_title(title: str) -> str:
    """
    Normalize whitespace in a title.

    Args:
        title: The title to normalize

    Returns:
        str: The title with normalized whitespace
    """
    return " ".join(title.split()) if title else ""
```

**Описание**:  Функция нормализует пробелы в заголовке.

**Параметры**:

- `title` (str):  Заголовок для нормализации.

**Возвращаемое значение**:

- `str`:  Заголовок с нормализованными пробелами.

**Как работает**:

- Функция разделяет заголовок на слова по пробелам, а затем снова объединяет их, используя один пробел в качестве разделителя.

### `format_link(url: str, title: Optional[str] = None) -> str`

```python
def format_link(url: str, title: Optional[str] = None) -> str:
    """
    Format a URL and title as a markdown link.

    Args:
        url: The URL to link to
        title: The title to display. If None, extracts from URL

    Returns:
        str: The formatted markdown link
    """
    if title is None:
        try:
            title = unquote_plus(url.split("//", maxsplit=1)[1].split("?")[0].replace("www.", ""))
        except IndexError:
            title = url
    return f"[{quote_title(title)}]({quote_url(url)})"
```

**Описание**:  Функция форматирует URL и заголовок как ссылку в Markdown.

**Параметры**:

- `url` (str):  URL для ссылки.
- `title` (Optional[str]):  Текст, который будет отображаться в ссылке. Если не задано, извлекается из URL.

**Возвращаемое значение**:

- `str`:  Сформированная ссылка в Markdown.

**Как работает**:

- Если `title` не задан, функция извлекает его из URL.
- Затем функция кодирует `title` и `url`, используя функции `quote_title` и `quote_url`.
- В результате формируется строка Markdown-ссылки.

### `format_image(image: str, alt: str, preview: Optional[str] = None) -> str`

```python
def format_image(image: str, alt: str, preview: Optional[str] = None) -> str:
    """
    Formats the given image as a markdown string.

    Args:
        image: The image to format.
        alt: The alt text for the image.
        preview: The preview URL format. Defaults to the original image.

    Returns:
        str: The formatted markdown string.
    """
    preview_url = preview.replace('{image}', image) if preview else image
    return f"[![{quote_title(alt)}]({quote_url(preview_url)})]({quote_url(image)})"
```

**Описание**:  Функция форматирует изображение в виде строки Markdown.

**Параметры**:

- `image` (str):  URL изображения.
- `alt` (str):  Альтернативный текст для изображения.
- `preview` (Optional[str]):  URL для предварительного просмотра изображения. По умолчанию используется исходный URL изображения.

**Возвращаемое значение**:

- `str`:  Сформированная строка Markdown с изображением.

**Как работает**:

- Функция сначала форматирует URL для предварительного просмотра, заменяя `{image}` на `image`.
- Затем функция кодирует URL изображения и URL предварительного просмотра, используя функцию `quote_url`.
- В результате формируется строка Markdown с изображением.

### `format_images_markdown(images: Union[str, List[str]], alt: str, preview: Union[str, List[str]] = None) -> str`

```python
def format_images_markdown(images: Union[str, List[str]], alt: str,
                           preview: Union[str, List[str]] = None) -> str:
    """
    Formats the given images as a markdown string.

    Args:
        images: The image or list of images to format.
        alt: The alt text for the images.
        preview: The preview URL format or list of preview URLs.
            If not provided, original images are used.

    Returns:
        str: The formatted markdown string.
    """
    if isinstance(images, list) and len(images) == 1:
        images = images[0]

    if isinstance(images, str):
        result = format_image(images, alt, preview)
    else:
        result = "\n".join(
            format_image(
                image,
                f"#{idx+1} {alt}",
                preview[idx] if isinstance(preview, list) and idx < len(preview) else preview
            )
            for idx, image in enumerate(images)
        )

    start_flag = "<!-- generated images start -->\n"
    end_flag = "<!-- generated images end -->\n"
    return f"\n{start_flag}{result}\n{end_flag}\n"
```

**Описание**:  Функция форматирует изображения в виде строки Markdown.

**Параметры**:

- `images` (Union[str, List[str]]):  URL изображения или список URL изображений.
- `alt` (str):  Альтернативный текст для изображений.
- `preview` (Union[str, List[str]]):  URL для предварительного просмотра изображения или список URL для предварительного просмотра изображений. По умолчанию используются исходные URL изображений.

**Возвращаемое значение**:

- `str`:  Сформированная строка Markdown с изображениями.

**Как работает**:

- Функция сначала проверяет, является ли `images` строкой или списком.
- Если это строка, функция вызывает `format_image` для форматирования изображения.
- Если это список, функция перебирает список изображений, форматируя каждое изображение с помощью `format_image` и объединяя результаты в одну строку с помощью `\n`.
- В результате формируется строка Markdown с изображениями, заключенная в комментарии `<!-- generated images start -->` и `<!-- generated images end -->`.