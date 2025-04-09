# Модуль для обработки ответов от GPT4Free

## Обзор

Этот модуль содержит классы и функции для обработки и форматирования различных типов ответов, полученных от GPT4Free. Он включает в себя функции для форматирования URL-адресов, заголовков, изображений и другие классы для представления различных типов ответов, таких как JSON, скрытые ответы, сообщения о завершении, вызовы инструментов, использование, результаты аутентификации, сгенерированные заголовки, отладочные ответы, рассуждения, источники, видео YouTube и аудио.

## Подробнее

Модуль предоставляет инструменты для преобразования и представления данных в различных форматах, включая Markdown и HTML, что позволяет легко интегрировать ответы GPT4Free в различные приложения и платформы. Он содержит классы для обработки различных типов ответов и обеспечивает единообразный способ доступа к данным ответа.

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
- `str`: Правильно экранированный URL.

**Как работает функция**:
1. Проверяет, содержит ли URL символ `%`. Если да, то декодирует URL, чтобы избежать двойного декодирования.
2. Разделяет URL на части, используя `//` в качестве разделителя, чтобы отделить протокол от остальной части URL.
3. Если в URL нет `//`, то считает его относительным URL и экранирует его целиком.
4. Если в URL есть `//`, то разделяет оставшуюся часть на домен и путь, используя `/` в качестве разделителя.
5. Если после домена нет `/`, то считает URL доменом и возвращает его.
6. Если после домена есть `/`, то экранирует путь и возвращает полный URL с экранированным путем.

```
URL -> Проверка на наличие '%' -> Декодирование URL (если нужно) -> Разделение на протокол и остальную часть ->
    Относительный URL? -> Экранирование URL -> Возврат
    ↓
    Нет -> Разделение на домен и путь -> После домена есть '/'? -> Экранирование пути -> Возврат полного URL
```

**Примеры**:

```python
>>> quote_url('https://example.com/path%20with%20spaces?query=value')
'https://example.com/path%20with%20spaces?query=value'

>>> quote_url('/relative/path?query=value')
'%2Frelative%2Fpath%3Fquery%3Dvalue'
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
1. Разделяет заголовок на слова, используя пробелы в качестве разделителя.
2. Объединяет слова обратно в строку, используя один пробел между словами.

```
Заголовок -> Разделение на слова -> Объединение слов с одним пробелом -> Возврат нормализованного заголовка
```

**Примеры**:

```python
>>> quote_title('  Example   Title  ')
'Example Title'

>>> quote_title('')
''
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

**Назначение**: Форматирует URL и заголовок как ссылку в Markdown.

**Параметры**:
- `url` (str): URL для ссылки.
- `title` (Optional[str], optional): Заголовок для отображения. Если `None`, извлекается из URL. По умолчанию `None`.

**Возвращает**:
- `str`: Отформатированная ссылка в Markdown.

**Как работает функция**:
1. Если заголовок не указан, пытается извлечь его из URL.
2. Экранирует URL и заголовок.
3. Форматирует URL и заголовок как ссылку в Markdown.

```
URL, Заголовок -> Заголовок указан? -> Извлечение заголовка из URL (если не указан) -> Экранирование URL и заголовка -> Форматирование как ссылка в Markdown -> Возврат
```

**Примеры**:

```python
>>> format_link('https://example.com', 'Example')
'[Example](https://example.com)'

>>> format_link('https://example.com')
'[example.com](https://example.com)'
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

**Назначение**: Форматирует данное изображение как строку в Markdown.

**Параметры**:
- `image` (str): Изображение для форматирования.
- `alt` (str): Альтернативный текст для изображения.
- `preview` (Optional[str], optional): URL превью. По умолчанию используется оригинальное изображение.

**Возвращает**:
- `str`: Отформатированная строка в Markdown.

**Как работает функция**:
1. Если URL превью указан, заменяет `{image}` в URL превью на URL изображения.
2. Экранирует URL превью и альтернативный текст.
3. Форматирует изображение как строку в Markdown.

```
Изображение, Альт. текст, URL превью -> URL превью указан? -> Замена '{image}' в URL превью на URL изображения -> Экранирование URL превью и альт. текста -> Форматирование как строка в Markdown -> Возврат
```

**Примеры**:

```python
>>> format_image('https://example.com/image.jpg', 'Example Image')
'[![Example Image](https://example.com/image.jpg)](https://example.com/image.jpg)'

>>> format_image('https://example.com/image.jpg', 'Example Image', 'https://example.com/preview/{image}')
'[![Example Image](https://example.com/preview/https%3A//example.com/image.jpg)](https://example.com/image.jpg)'
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

**Назначение**: Форматирует заданные изображения как строку Markdown.

**Параметры**:
- `images` (Union[str, List[str]]): Изображение или список изображений для форматирования.
- `alt` (str): Альтернативный текст для изображений.
- `preview` (Union[str, List[str]], optional): URL превью или список URL превью. Если не указан, используются оригинальные изображения.

**Возвращает**:
- `str`: Отформатированная строка Markdown.

**Как работает функция**:
1. Если `images` является списком и содержит только одно изображение, присваивает это изображение переменной `images`.
2. Если `images` является строкой, вызывает `format_image` для форматирования изображения.
3. Если `images` является списком, вызывает `format_image` для каждого изображения в списке и объединяет результаты с помощью `\n`.
4. Добавляет флаги начала и конца сгенерированных изображений.

```
Изображения, Альт. текст, URL превью -> images - список? -> images.length == 1? -> images = images[0]
↓
images - строка? -> result = format_image() -> Добавление флагов начала и конца -> Возврат
↓
Нет -> result = "\\n".join(format_image() для каждого изображения) -> Добавление флагов начала и конца -> Возврат
```

**Примеры**:

```python
>>> format_images_markdown('https://example.com/image.jpg', 'Example Image')
'\n<!-- generated images start -->\n[![Example Image](https://example.com/image.jpg)](https://example.com/image.jpg)\n<!-- generated images end -->\n'

>>> format_images_markdown(['https://example.com/image1.jpg', 'https://example.com/image2.jpg'], 'Example Image')
'\n<!-- generated images start -->\n[![#1 Example Image](https://example.com/image1.jpg)](https://example.com/image1.jpg)\\n[![#2 Example Image](https://example.com/image2.jpg)](https://example.com/image2.jpg)\n<!-- generated images end -->\n'
```

## Классы

### `ResponseType`

**Описание**: Абстрактный базовый класс для всех типов ответов.

**Методы**:
- `__str__(self) -> str`: Абстрактный метод для преобразования ответа в строковое представление. Должен быть реализован в подклассах. Вызывает исключение `NotImplementedError`, если не реализован.

### `JsonMixin`

**Описание**: Миксин для классов, которые могут быть представлены в формате JSON.

**Методы**:
- `__init__(self, **kwargs) -> None`: Инициализирует класс с атрибутами, переданными в виде именованных аргументов.
- `get_dict(self) -> Dict`: Возвращает словарь атрибутов класса, исключая приватные атрибуты (начинающиеся с `__`).
- `reset(self) -> None`: Сбрасывает все атрибуты класса.

### `RawResponse`

**Описание**: Класс для представления необработанного ответа.

**Наследует**:
- `ResponseType`
- `JsonMixin`

### `HiddenResponse`

**Описание**: Класс для представления скрытого ответа.

**Наследует**:
- `ResponseType`

**Методы**:
- `__str__(self) -> str`: Возвращает пустую строку.

### `FinishReason`

**Описание**: Класс для представления причины завершения.

**Наследует**:
- `JsonMixin`
- `HiddenResponse`

**Методы**:
- `__init__(self, reason: str) -> None`: Инициализирует класс с причиной завершения.

### `ToolCalls`

**Описание**: Класс для представления списка вызовов инструментов.

**Наследует**:
- `HiddenResponse`

**Методы**:
- `__init__(self, list: List) -> None`: Инициализирует класс со списком вызовов инструментов.
- `get_list(self) -> List`: Возвращает список вызовов инструментов.

### `Usage`

**Описание**: Класс для представления информации об использовании.

**Наследует**:
- `JsonMixin`
- `HiddenResponse`

### `AuthResult`

**Описание**: Класс для представления результата аутентификации.

**Наследует**:
- `JsonMixin`
- `HiddenResponse`

### `TitleGeneration`

**Описание**: Класс для представления сгенерированного заголовка.

**Наследует**:
- `HiddenResponse`

**Методы**:
- `__init__(self, title: str) -> None`: Инициализирует класс с заголовком.

### `DebugResponse`

**Описание**: Класс для представления отладочного ответа.

**Наследует**:
- `HiddenResponse`

**Методы**:
- `__init__(self, log: str) -> None`: Инициализирует класс с сообщением журнала.

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

**Описание**: Класс для представления рассуждений.

**Наследует**:
- `ResponseType`

**Параметры**:
- `token` (Optional[str], optional): Токен рассуждения. По умолчанию `None`.
- `label` (Optional[str], optional): Метка рассуждения. По умолчанию `None`.
- `status` (Optional[str], optional): Статус рассуждения. По умолчанию `None`.
- `is_thinking` (Optional[str], optional): Состояние размышления. По умолчанию `None`.

**Методы**:
- `__init__(self, token: Optional[str] = None, label: Optional[str] = None, status: Optional[str] = None, is_thinking: Optional[str] = None) -> None`: Инициализирует класс с токеном, статусом и состоянием размышления.
- `__str__(self) -> str`: Возвращает строковое представление на основе доступных атрибутов.
- `__eq__(self, other: Reasoning)`: Сравнивает два объекта `Reasoning` на равенство.
- `get_dict(self) -> Dict`: Возвращает словарное представление рассуждения.

**Как работает класс**:
Класс `Reasoning` предназначен для представления этапов логических рассуждений. Он может хранить токен (текстовый фрагмент), метку, статус и флаг, указывающий, находится ли процесс в стадии размышления. В зависимости от того, какие атрибуты заданы, метод `__str__` формирует различные строковые представления. Метод `get_dict` возвращает словарь, содержащий заполненные атрибуты.

**Примеры**:

```python
>>> reasoning = Reasoning(token='Thinking...')
>>> str(reasoning)
'Thinking...'

>>> reasoning = Reasoning(label='Step 1', status='Completed')
>>> str(reasoning)
'Step 1: Completed\n'
```

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
        return "\\n\\n\\n\\n" + ("\\n>\\n".join([\
            f"> [{idx}] {format_link(link['url'], link.get('title', None))}"
            for idx, link in enumerate(self.list)
        ]))
```

**Описание**: Класс для представления списка источников.

**Наследует**:
- `ResponseType`

**Параметры**:
- `sources` (List[Dict[str, str]]): Список словарей, представляющих источники.

**Методы**:
- `__init__(self, sources: List[Dict[str, str]]) -> None`: Инициализирует класс со списком словарей, представляющих источники.
- `add_source(self, source: Union[Dict[str, str], str]) -> None`: Добавляет источник в список, очищая URL при необходимости.
- `__str__(self) -> str`: Возвращает отформатированные источники в виде строки.

**Как работает класс**:
Класс `Sources` предназначен для хранения и форматирования списка источников информации. В конструкторе он принимает список словарей, каждый из которых представляет источник. Метод `add_source` добавляет источник в список, предварительно очищая URL от параметров `utm_source`. Метод `__str__` возвращает отформатированную строку со списком источников, каждый из которых представлен в виде ссылки Markdown.

**Примеры**:

```python
>>> sources = Sources([{'url': 'https://example.com', 'title': 'Example'}])
>>> str(sources)
'\n\n\n\n> \n> [0] [Example](https://example.com)'
```

### `YouTube`

**Описание**: Класс для представления списка идентификаторов YouTube.

**Наследует**:
- `HiddenResponse`

**Методы**:
- `__init__(self, ids: List[str]) -> None`: Инициализирует класс со списком идентификаторов YouTube.
- `to_string(self) -> str`: Возвращает встроенные видео YouTube в виде строки.

### `AudioResponse`

**Описание**: Класс для представления аудиоданных.

**Наследует**:
- `ResponseType`

**Методы**:
- `__init__(self, data: Union[bytes, str]) -> None`: Инициализирует класс с аудиоданными в виде байтов.
- `to_uri(self) -> str`: Возвращает аудиоданные в виде URI данных в кодировке Base64.
- `__str__(self) -> str`: Возвращает аудио как HTML-элемент.

### `BaseConversation`

**Описание**: Базовый класс для представления разговора.

**Наследует**:
- `ResponseType`

**Методы**:
- `__str__(self) -> str`: Возвращает пустую строку по умолчанию.

### `JsonConversation`

**Описание**: Класс для представления разговора в формате JSON.

**Наследует**:
- `BaseConversation`
- `JsonMixin`

### `SynthesizeData`

**Описание**: Класс для представления синтезированных данных.

**Наследует**:
- `HiddenResponse`
- `JsonMixin`

**Методы**:
- `__init__(self, provider: str, data: Dict) -> None`: Инициализирует класс с поставщиком и данными.

### `SuggestedFollowups`

**Описание**: Класс для представления предложенных продолжений.

**Наследует**:
- `HiddenResponse`

**Методы**:
- `__init__(self, suggestions: list[str])`: инициализирует класс со списком предложений.

### `RequestLogin`

**Описание**: Класс для представления запроса на вход.

**Наследует**:
- `HiddenResponse`

**Методы**:
- `__init__(self, label: str, login_url: str) -> None`: Инициализирует класс с меткой и URL для входа.
- `to_string(self) -> str`: Возвращает отформатированную ссылку для входа в виде строки.

### `MediaResponse`

**Описание**: Базовый класс для ответа, содержащего медиафайлы (изображения, видео и т.д.).

**Методы**:
    - `__init__(self, urls: Union[str, List[str]], alt: str, options: Dict = {}, **kwargs) -> None`:
        Инициализирует объект MediaResponse.
        **Параметры**:
            - `urls` (Union[str, List[str]]): URL или список URL медиафайлов.
            - `alt` (str): Альтернативный текст для медиафайлов.
            - `options` (Dict, optional): Дополнительные параметры. По умолчанию {}.
            - `**kwargs`: Дополнительные именованные аргументы.
    - `get(self, key: str) -> any`: Возвращает значение параметра по ключу.
    - `get_list(self) -> List[str]`: Возвращает список URL медиафайлов.

### `ImageResponse`

**Описание**: Класс для представления ответа с изображениями.

**Наследует**:
- `MediaResponse`

**Методы**:
- `__str__(self) -> str`: Возвращает изображения в виде Markdown.

### `VideoResponse`

**Описание**: Класс для представления ответа с видео.

**Наследует**:
- `MediaResponse`

**Методы**:
- `__str__(self) -> str`: Возвращает видео в виде HTML-элементов.

### `ImagePreview`

**Описание**: Класс для представления предварительного просмотра изображения.

**Наследует**:
- `ImageResponse`

**Методы**:
- `__str__(self) -> str`: Возвращает пустую строку для предварительного просмотра.
- `to_string(self) -> str`: Возвращает изображения в виде Markdown.

### `PreviewResponse`

**Описание**: Класс для представления предварительного просмотра.

**Наследует**:
- `HiddenResponse`

**Методы**:
- `__init__(self, data: str) -> None`: Инициализирует класс с данными.
- `to_string(self) -> str`: Возвращает данные в виде строки.

### `Parameters`

**Описание**: Класс для представления параметров.

**Наследует**:
- `ResponseType`
- `JsonMixin`

**Методы**:
- `__str__(self) -> str`: Возвращает пустую строку.

### `ProviderInfo`

**Описание**: Класс для представления информации о провайдере.

**Наследует**:
- `JsonMixin`
- `HiddenResponse`