# Модуль обработки ответов от GPT4Free

## Обзор

Модуль `response.py` предназначен для обработки и форматирования ответов, полученных от различных провайдеров в рамках проекта `gpt4free`. Он включает в себя функции для работы с URL, текстом, изображениями, аудио и другими типами данных, а также содержит классы для представления различных типов ответов, таких как JSON, текст, изображения, видео и т.д.

## Подробней

Этот модуль предоставляет набор инструментов и классов, необходимых для стандартизации и представления данных, возвращаемых различными поставщиками услуг GPT4Free. Он содержит функции для форматирования URL-адресов и заголовков, а также классы, представляющие различные типы ответов, такие как JSON, скрытые ответы, причины завершения, вызовы инструментов, использование, результаты аутентификации, генерация заголовков, отладочные ответы, рассуждения, источники, YouTube-видео, аудио-ответы, базовые разговоры, данные синтеза, предлагаемые последующие действия, запросы на вход, медиа-ответы, ответы изображений, ответы видео, предварительный просмотр изображений, ответы предварительного просмотра, параметры и информацию о провайдере.

## Функции

### `quote_url`

```python
def quote_url(url: str) -> str:
    """
    Quote parts of a URL while preserving the domain structure.
    
    Args:
        url: The URL to quote
        
    Returns:
        str: The properly quoted URL
    """
    ...
```

**Назначение**: Экранирует части URL, сохраняя структуру домена.
**Параметры**:
- `url` (str): URL для экранирования.

**Возвращает**:
- `str`: Экранированный URL.

**Как работает функция**:
- Функция сначала проверяет, содержит ли URL символы `%`. Если да, то URL декодируется.
- Затем URL разделяется на части, чтобы отделить протокол от остальной части URL.
- Если в URL нет `//`, то он считается относительным и экранируется целиком.
- Если протокол есть, то остальная часть URL разделяется на домен и путь.
- Если после домена нет `/`, то URL считается URL домена и возвращается как есть.
- Наконец, путь экранируется и объединяется с протоколом и доменом.

**Примеры**:

```python
url = "https://example.com/path with spaces?param=value"
quoted_url = quote_url(url)
print(quoted_url)  # Вывод: https://example.com/path%20with%20spaces?param=value

url = "/relative/path with spaces"
quoted_url = quote_url(url)
print(quoted_url)  # Вывод: %2Frelative%2Fpath%20with%20spaces
```

### `quote_title`

```python
def quote_title(title: str) -> str:
    """
    Normalize whitespace in a title.
    
    Args:
        title: The title to normalize
        
    Returns:
        str: The title with normalized whitespace
    """
    ...
```

**Назначение**: Нормализует пробелы в заголовке.

**Параметры**:
- `title` (str): Заголовок для нормализации.

**Возвращает**:
- `str`: Заголовок с нормализованными пробелами.

**Как работает функция**:
- Функция разделяет заголовок на слова, используя пробелы в качестве разделителя.
- Затем она объединяет слова обратно в строку, используя один пробел между ними.
- Если заголовок пустой, возвращается пустая строка.

**Примеры**:

```python
title = "Title  with   multiple   spaces"
normalized_title = quote_title(title)
print(normalized_title)  # Вывод: Title with multiple spaces

title = ""
normalized_title = quote_title(title)
print(normalized_title)  # Вывод:
```

### `format_link`

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
    ...
```

**Назначение**: Форматирует URL и заголовок как ссылку в формате Markdown.

**Параметры**:
- `url` (str): URL для создания ссылки.
- `title` (Optional[str], optional): Заголовок для отображения. Если `None`, извлекается из URL. По умолчанию `None`.

**Возвращает**:
- `str`: Отформатированная ссылка в формате Markdown.

**Как работает функция**:
- Если заголовок не предоставлен, он пытается извлечь его из URL.
- URL и заголовок экранируются.
- Функция возвращает строку в формате `[title](url)`.

**Примеры**:

```python
url = "https://example.com/path?param=value"
markdown_link = format_link(url)
print(markdown_link)  # Вывод: [example.com/path](https://example.com/path?param=value)

url = "https://example.com/path?param=value"
title = "Example Title"
markdown_link = format_link(url, title)
print(markdown_link)  # Вывод: [Example Title](https://example.com/path?param=value)
```

### `format_image`

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
    ...
```

**Назначение**: Форматирует данное изображение как строку в формате Markdown.

**Параметры**:
- `image` (str): Изображение для форматирования.
- `alt` (str): Альтернативный текст для изображения.
- `preview` (Optional[str], optional): URL предварительного просмотра. По умолчанию используется исходное изображение.

**Возвращает**:
- `str`: Отформатированная строка в формате Markdown.

**Как работает функция**:
- Если предоставлен URL предварительного просмотра, он используется вместо исходного URL изображения.
- URL изображения и альтернативный текст экранируются.
- Функция возвращает строку в формате `[![alt](preview_url)](image_url)`.

**Примеры**:

```python
image_url = "https://example.com/image.jpg"
alt_text = "Example Image"
markdown_image = format_image(image_url, alt_text)
print(markdown_image)  # Вывод: [![Example Image](https://example.com/image.jpg)](https://example.com/image.jpg)

image_url = "https://example.com/image.jpg"
alt_text = "Example Image"
preview_url = "https://example.com/preview.jpg"
markdown_image = format_image(image_url, alt_text, preview_url)
print(markdown_image)  # Вывод: [![Example Image](https://example.com/preview.jpg)](https://example.com/image.jpg)
```

### `format_images_markdown`

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
    ...
```

**Назначение**: Форматирует данное изображение или список изображений в виде строки Markdown.

**Параметры**:
- `images` (Union[str, List[str]]): Изображение или список изображений для форматирования.
- `alt` (str): Альтернативный текст для изображений.
- `preview` (Union[str, List[str]], optional): URL предварительного просмотра или список URL-адресов предварительного просмотра. Если не указано, используются исходные изображения.

**Возвращает**:
- `str`: Отформатированная строка Markdown.

**Как работает функция**:
- Если `images` - это список и содержит только один элемент, он извлекается.
- Если `images` - это строка, то вызывается `format_image` для форматирования одного изображения.
- Если `images` - это список, то `format_image` вызывается для каждого изображения в списке, и результаты объединяются с разделителем `\n`.
- Результат обрамляется флагами `<!-- generated images start -->` и `<!-- generated images end -->`.

**Примеры**:

```python
images = "https://example.com/image.jpg"
alt_text = "Example Image"
markdown_images = format_images_markdown(images, alt_text)
print(markdown_images)
# Вывод:
#
# <!-- generated images start -->
# [![Example Image](https://example.com/image.jpg)](https://example.com/image.jpg)
# <!-- generated images end -->
#

images = ["https://example.com/image1.jpg", "https://example.com/image2.jpg"]
alt_text = "Example Image"
markdown_images = format_images_markdown(images, alt_text)
print(markdown_images)
# Вывод:
#
# <!-- generated images start -->
# [![#1 Example Image](https://example.com/image1.jpg)](https://example.com/image1.jpg)
# \n
# [![#2 Example Image](https://example.com/image2.jpg)](https://example.com/image2.jpg)
# <!-- generated images end -->
#
```

## Классы

### `ResponseType`

```python
class ResponseType:
    @abstractmethod
    def __str__(self) -> str:
        """Convert the response to a string representation."""
        raise NotImplementedError
```

**Описание**: Базовый абстрактный класс для всех типов ответов.

**Методы**:
- `__str__`: Преобразует ответ в строковое представление. Должен быть реализован в подклассах.

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

**Описание**: Mixin класс для классов, которые могут быть представлены в виде JSON.

**Методы**:

- `__init__`:
    ```python
    def __init__(self, **kwargs) -> None:
        """Initialize with keyword arguments as attributes."""
        ...
    ```

    **Назначение**: Инициализирует экземпляр класса, устанавливая атрибуты на основе переданных ключевых слов.

    **Параметры**:
    - `**kwargs`: Ключевые слова, которые будут установлены как атрибуты класса.

    **Как работает функция**:
    - Проходит по всем переданным ключевым словам и их значениям.
    - Устанавливает каждый ключ как атрибут экземпляра класса и присваивает ему соответствующее значение.

- `get_dict`:
    ```python
    def get_dict(self) -> Dict:
        """Return a dictionary of non-private attributes."""
        ...
    ```

    **Назначение**: Возвращает словарь, содержащий все не приватные атрибуты экземпляра класса.

    **Возвращает**:
    - `Dict`: Словарь, где ключи - имена атрибутов, а значения - их соответствующие значения.

    **Как работает функция**:
    - Проходит по всем атрибутам экземпляра класса.
    - Проверяет, начинается ли имя атрибута с двух подчеркиваний (`__`), чтобы исключить приватные атрибуты.
    - Добавляет атрибут и его значение в словарь, если атрибут не является приватным.

- `reset`:
    ```python
    def reset(self) -> None:
        """Reset all attributes."""
        ...
    ```

    **Назначение**: Сбрасывает все атрибуты экземпляра класса, удаляя их.

    **Как работает функция**:
    - Присваивает атрибуту `__dict__` пустой словарь, что приводит к удалению всех атрибутов экземпляра класса.

### `RawResponse`

```python
class RawResponse(ResponseType, JsonMixin):
    pass
```

**Описание**: Класс для представления необработанного ответа. Наследуется от `ResponseType` и `JsonMixin`.

### `HiddenResponse`

```python
class HiddenResponse(ResponseType):
    def __str__(self) -> str:
        """Hidden responses return an empty string."""
        return ""
```

**Описание**: Класс для представления скрытого ответа. Наследуется от `ResponseType`.

**Методы**:
- `__str__`: Возвращает пустую строку.

### `FinishReason`

```python
class FinishReason(JsonMixin, HiddenResponse):
    def __init__(self, reason: str) -> None:
        """Initialize with a reason."""
        self.reason = reason
```

**Описание**: Класс для представления причины завершения. Наследуется от `JsonMixin` и `HiddenResponse`.

**Методы**:
- `__init__`:
    ```python
    def __init__(self, reason: str) -> None:
        """Initialize with a reason."""
        self.reason = reason
    ```

    **Назначение**: Инициализирует экземпляр класса с указанной причиной завершения.

    **Параметры**:
    - `reason` (str): Причина завершения.

    **Как работает функция**:
    - Устанавливает значение атрибута `reason` экземпляра класса равным переданной причине завершения.

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

**Описание**: Класс для представления вызовов инструментов. Наследуется от `HiddenResponse`.

**Методы**:
- `__init__`: Инициализирует класс списком вызовов инструментов.
- `get_list`: Возвращает список вызовов инструментов.

### `Usage`

```python
class Usage(JsonMixin, HiddenResponse):
    pass
```

**Описание**: Класс для представления информации об использовании. Наследуется от `JsonMixin` и `HiddenResponse`.

### `AuthResult`

```python
class AuthResult(JsonMixin, HiddenResponse):
    pass
```

**Описание**: Класс для представления результата аутентификации. Наследуется от `JsonMixin` и `HiddenResponse`.

### `TitleGeneration`

```python
class TitleGeneration(HiddenResponse):
    def __init__(self, title: str) -> None:
        """Initialize with a title."""
        self.title = title
```

**Описание**: Класс для представления сгенерированного заголовка. Наследуется от `HiddenResponse`.

**Методы**:
- `__init__`: Инициализирует класс заголовком.

### `DebugResponse`

```python
class DebugResponse(HiddenResponse):
    def __init__(self, log: str) -> None:
        """Initialize with a log message."""
        self.log = log
```

**Описание**: Класс для представления отладочного ответа. Наследуется от `HiddenResponse`.

**Методы**:
- `__init__`: Инициализирует класс сообщением журнала.

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
                return f"{self.label}: {self.status}\\n"
            return f"{self.status}\\n"
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

**Описание**: Класс для представления рассуждений. Наследуется от `ResponseType`.

**Методы**:

- `__init__`:
    ```python
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
    ```

    **Назначение**: Инициализирует экземпляр класса с указанными параметрами.

    **Параметры**:
    - `token` (Optional[str], optional): Токен рассуждения. По умолчанию `None`.
    - `label` (Optional[str], optional): Метка рассуждения. По умолчанию `None`.
    - `status` (Optional[str], optional): Статус рассуждения. По умолчанию `None`.
    - `is_thinking` (Optional[str], optional): Состояние "размышления". По умолчанию `None`.

    **Как работает функция**:
    - Устанавливает значения атрибутов `token`, `label`, `status` и `is_thinking` экземпляра класса равными переданным параметрам.

- `__str__`:
    ```python
    def __str__(self) -> str:
        """Return string representation based on available attributes."""
        ...
    ```

    **Назначение**: Возвращает строковое представление объекта `Reasoning` на основе доступных атрибутов.

    **Возвращает**:
    - `str`: Строковое представление объекта.

    **Как работает функция**:
    - Проверяет, установлен ли атрибут `is_thinking`. Если да, возвращает его значение.
    - Если `is_thinking` не установлен, проверяет, установлен ли атрибут `token`. Если да, возвращает его значение.
    - Если `token` не установлен, проверяет, установлен ли атрибут `status`.
        - Если `status` установлен и `label` также установлен, возвращает строку в формате "{label}: {status}\n".
        - Если `status` установлен, но `label` не установлен, возвращает строку в формате "{status}\n".
    - Если ни один из атрибутов `is_thinking`, `token` и `status` не установлен, возвращает пустую строку.

- `__eq__`:
    ```python
    def __eq__(self, other: Reasoning):
        return (self.token == other.token and
                self.status == other.status and
                self.is_thinking == other.is_thinking)
    ```

    **Назначение**: Сравнивает два объекта `Reasoning` на равенство.

    **Параметры**:
    - `other` (Reasoning): Другой объект `Reasoning` для сравнения.

    **Возвращает**:
    - `bool`: `True`, если объекты равны, `False` в противном случае.

    **Как работает функция**:
    - Сравнивает атрибуты `token`, `status` и `is_thinking` текущего объекта с соответствующими атрибутами другого объекта.
    - Возвращает `True`, если все атрибуты равны, и `False` в противном случае.

- `get_dict`:
    ```python
    def get_dict(self) -> Dict:
        """Return a dictionary representation of the reasoning."""
        ...
    ```

    **Назначение**: Возвращает словарь, представляющий рассуждение.

    **Возвращает**:
    - `Dict`: Словарь, содержащий атрибуты рассуждения.

    **Как работает функция**:
    - Если установлен атрибут `label`, возвращает словарь с ключами "label" и "status".
    - Если атрибут `is_thinking` не установлен:
        - Если атрибут `status` не установлен, возвращает словарь с ключом "token".
        - Если атрибут `status` установлен, возвращает словарь с ключами "token" и "status".
    - В противном случае возвращает словарь с ключами "token", "status" и "is_thinking".

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
        return "\\n\\n\\n\\n" + ("\\n>\\n".join([
            f"> [{idx}] {format_link(link['url'], link.get('title', None))}"
            for idx, link in enumerate(self.list)
        ]))
```

**Описание**: Класс для представления источников. Наследуется от `ResponseType`.

**Методы**:

- `__init__`:
    ```python
    def __init__(self, sources: List[Dict[str, str]]) -> None:
        """Initialize with a list of source dictionaries."""
        self.list = []
        for source in sources:
            self.add_source(source)
    ```

    **Назначение**: Инициализирует экземпляр класса списком словарей источников.

    **Параметры**:
    - `sources` (List[Dict[str, str]]): Список словарей, где каждый словарь представляет источник.

    **Как работает функция**:
    - Инициализирует пустой список `self.list`.
    - Перебирает каждый источник в списке `sources` и вызывает метод `add_source` для добавления источника в список.

- `add_source`:
    ```python
    def add_source(self, source: Union[Dict[str, str], str]) -> None:
        """Add a source to the list, cleaning the URL if necessary."""
        source = source if isinstance(source, dict) else {"url": source}
        url = source.get("url", source.get("link", None))
        if url is not None:
            url = re.sub(r"[&?]utm_source=.+", "", url)
            source["url"] = url
            self.list.append(source)
    ```

    **Назначение**: Добавляет источник в список, очищая URL при необходимости.

    **Параметры**:
    - `source` (Union[Dict[str, str], str]): Источник для добавления. Может быть словарем или строкой.

    **Как работает функция**:
    - Если `source` является строкой, преобразует ее в словарь с ключом `"url"`.
    - Извлекает URL из источника, сначала пытаясь получить его из ключа `"url"`, затем из ключа `"link"`.
    - Если URL найден, удаляет из него параметры `utm_source`.
    - Добавляет очищенный URL в список `self.list`.

- `__str__`:
    ```python
    def __str__(self) -> str:
        """Return formatted sources as a string."""
        if not self.list:
            return ""
        return "\\n\\n\\n\\n" + ("\\n>\\n".join([
            f"> [{idx}] {format_link(link['url'], link.get('title', None))}"
            for idx, link in enumerate(self.list)
        ]))
    ```

    **Назначение**: Возвращает отформатированные источники в виде строки.

    **Возвращает**:
    - `str`: Строка, содержащая отформатированные источники.

    **Как работает функция**:
    - Если список `self.list` пуст, возвращает пустую строку.
    - Иначе, перебирает каждый источник в списке `self.list`, форматирует его с помощью функции `format_link` и объединяет результаты в строку, разделенную символами `\n>\n`.

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
        return "\\n\\n" + ("\\n".join([
            f'<iframe type="text/html" src="https://www.youtube.com/embed/{id}"></iframe>'
            for id in self.ids
        ]))
```

**Описание**: Класс для представления YouTube видео. Наследуется от `HiddenResponse`.

**Методы**:
- `__init__`: Инициализирует класс списком идентификаторов YouTube видео.
- `to_string`: Возвращает HTML-код для встраивания видео YouTube.

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

**Описание**: Класс для представления аудио-ответа. Наследуется от `ResponseType`.

**Методы**:
- `__init__`: Инициализирует класс байтами аудиоданных.
- `to_uri`: Возвращает аудиоданные в виде URI данных, закодированного в base64.
- `__str__`: Возвращает аудио как HTML-элемент.

### `BaseConversation`

```python
class BaseConversation(ResponseType):
    def __str__(self) -> str:
        """Return an empty string by default."""
        return ""
```

**Описание**: Базовый класс для представления разговора. Наследуется от `ResponseType`.

**Методы**:
- `__str__`: По умолчанию возвращает пустую строку.

### `JsonConversation`

```python
class JsonConversation(BaseConversation, JsonMixin):
    pass
```

**Описание**: Класс для представления разговора в формате JSON. Наследуется от `BaseConversation` и `JsonMixin`.

### `SynthesizeData`

```python
class SynthesizeData(HiddenResponse, JsonMixin):
    def __init__(self, provider: str, data: Dict) -> None:
        """Initialize with provider and data."""
        self.provider = provider
        self.data = data
```

**Описание**: Класс для представления данных синтеза. Наследуется от `HiddenResponse` и `JsonMixin`.

**Методы**:
- `__init__`: Инициализирует класс провайдером и данными.

### `SuggestedFollowups`

```python
class SuggestedFollowups(HiddenResponse):
    def __init__(self, suggestions: list[str]):
        self.suggestions = suggestions
```

**Описание**: Класс для представления предлагаемых последующих действий. Наследуется от `HiddenResponse`.

**Методы**:
 - `__init__`: Инициализирует класс списком предложений.

### `RequestLogin`

```python
class RequestLogin(HiddenResponse):
    def __init__(self, label: str, login_url: str) -> None:
        """Initialize with label and login URL."""
        self.label = label
        self.login_url = login_url

    def to_string(self) -> str:
        """Return formatted login link as a string."""
        return format_link(self.login_url, f"[Login to {self.label}]") + "\\n\\n"
```

**Описание**: Класс для представления запроса на вход. Наследуется от `HiddenResponse`.

**Методы**:
- `__init__`: Инициализирует класс меткой и URL-адресом для входа.
- `to_string`: Возвращает отформатированную ссылку для входа в виде строки.

### `MediaResponse`

```python
class MediaResponse(ResponseType):
    def __init__(
        self,
        urls: Union[str, List[str]],
        alt: str,
        options: Dict = {},\
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

**Описание**: Базовый класс для представления медиа-ответа (изображения, видео и т.д.). Наследуется от `ResponseType`.

**Методы**:
- `__init__`: Инициализирует класс URL-адресами, альтернативным текстом и параметрами.
- `get`: Возвращает значение параметра по ключу.
- `get_list`: Возвращает список URL-адресов.

### `ImageResponse`

```python
class ImageResponse(MediaResponse):
    def __str__(self) -> str:
        """Return images as markdown."""
        return format_images_markdown(self.urls, self.alt, self.get("preview"))
```

**Описание**: Класс для представления ответа с изображением. Наследуется от `MediaResponse`.

**Методы**:
- `__str__`: Возвращает изображения в формате Markdown.

### `VideoResponse`

```python
class VideoResponse(MediaResponse):
    def __str__(self) -> str:
        """Return videos as html elements."""
        return "\\n".join([f'<video controls src="{video}"></video>\' for video in self.get_list()])
```

**Описание**: Класс для представления видео-ответа. Наследуется от `MediaResponse`.

**Методы**:
- `__str__`: Возвращает видео в виде HTML-элементов.

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

**Описание**: Класс для предварительного просмотра изображений. Наследуется от `ImageResponse`.

**Методы**:
- `__str__`: Возвращает пустую строку для предварительного просмотра.
- `to_string`: Возвращает изображения в формате Markdown, используя метод родительского класса.

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

**Описание**: Класс для представления ответа предварительного просмотра. Наследуется от `HiddenResponse`.

**Методы**:
- `__init__`: Инициализирует класс данными.
- `to_string`: Возвращает данные в виде строки.

### `Parameters`

```python
class Parameters(ResponseType, JsonMixin):
    def __str__(self) -> str:
        """Return an empty string."""
        return ""
```

**Описание**: Класс для представления параметров. Наследуется от `ResponseType` и `JsonMixin`.

**Методы**:
- `__str__`: Возвращает пустую строку.

### `ProviderInfo`

```python
class ProviderInfo(JsonMixin, HiddenResponse):
    pass
```

**Описание**: Класс для представления информации о провайдере. Наследуется от `JsonMixin` и `HiddenResponse`.