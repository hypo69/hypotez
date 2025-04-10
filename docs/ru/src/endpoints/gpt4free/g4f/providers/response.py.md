# Модуль для работы с ответами от GPT4Free

## Обзор

Модуль `response.py` содержит классы и функции для обработки и форматирования ответов, полученных от различных поставщиков GPT4Free. Он предоставляет инструменты для нормализации URL, форматирования текста, создания markdown-ссылок и изображений, а также для представления различных типов ответов, таких как JSON, аудио, видео и изображения.

## Подробней

Этот модуль предоставляет набор классов и функций, упрощающих работу с ответами от API GPT4Free, а также подготавливает эти ответы для удобного отображения и использования. Он содержит функции для обработки URL-адресов, текста и мультимедийных данных, а также классы для представления различных типов ответов, таких как текстовые, JSON, аудио и видео. Модуль также включает классы для работы с метаданными, такими как источники и параметры.

## Функции

### `quote_url`

```python
def quote_url(url: str) -> str:
    """
    Кодирует части URL, сохраняя структуру домена.

    Args:
        url (str): URL для кодирования.

    Returns:
        str: Правильно закодированный URL.
    """
```

**Назначение**: Кодирует части URL, сохраняя структуру домена. Это необходимо для правильной обработки URL с символами, которые могут быть интерпретированы неправильно.

**Параметры**:

-   `url` (str): URL для кодирования.

**Возвращает**:

-   `str`: Правильно закодированный URL.

**Как работает функция**:

1.  Проверяет, содержит ли URL символы `%`, чтобы избежать двойного декодирования.
2.  Разделяет URL на части, используя `//` в качестве разделителя, чтобы отделить протокол от остальной части URL.
3.  Если в URL нет `//`, то он считается относительным и кодируется целиком.
4.  Если в URL есть протокол, то разделяет остальную часть URL на домен и путь, используя `/` в качестве разделителя.
5.  Если после домена нет `/`, то URL считается URL домена и возвращается без изменений.
6.  Кодирует путь, используя `quote_plus`, чтобы закодировать символы, которые могут быть интерпретированы неправильно.
7.  Возвращает полный URL с закодированным путем.

**ASCII flowchart**:

```
A[Проверка наличия '%' в URL]
|
B[Декодирование URL, если необходимо]
|
C[Разделение URL на протокол и остальную часть]
|
D[Проверка наличия '//' в URL]
|
E[Если нет '//', кодирование URL целиком]
|
F[Разделение остальной части URL на домен и путь]
|
G[Проверка наличия '/' после домена]
|
H[Если нет '/', возврат URL домена]
|
I[Кодирование пути URL]
|
J[Возврат полного URL с закодированным путем]
```

**Примеры**:

```python
>>> quote_url('https://example.com/path with spaces?query=value')
'https://example.com/path%20with%20spaces?query=value'
>>> quote_url('example.com/path with spaces')
'example.com%2Fpath+with+spaces'
```

### `quote_title`

```python
def quote_title(title: str) -> str:
    """
    Нормализует пробелы в заголовке.

    Args:
        title (str): Заголовок для нормализации.

    Returns:
        str: Заголовок с нормализованными пробелами.
    """
```

**Назначение**: Нормализует пробелы в заголовке, заменяя множественные пробелы на один и удаляя пробелы в начале и конце строки.

**Параметры**:

-   `title` (str): Заголовок для нормализации.

**Возвращает**:

-   `str`: Заголовок с нормализованными пробелами.

**Как работает функция**:

1.  Разделяет заголовок на слова, используя пробелы в качестве разделителя.
2.  Объединяет слова обратно в строку, используя один пробел в качестве разделителя.
3.  Если заголовок пустой, то возвращает пустую строку.

**ASCII flowchart**:

```
A[Проверка, является ли заголовок пустым]
|
B[Разделение заголовка на слова]
|
C[Объединение слов обратно в строку с одним пробелом]
|
D[Возврат нормализованного заголовка]
```

**Примеры**:

```python
>>> quote_title('  Title   with   multiple   spaces  ')
'Title with multiple spaces'
>>> quote_title('')
''
```

### `format_link`

```python
def format_link(url: str, title: Optional[str] = None) -> str:
    """
    Форматирует URL и заголовок в виде markdown-ссылки.

    Args:
        url (str): URL для ссылки.
        title (Optional[str], optional): Заголовок для отображения. Если `None`, извлекается из URL.

    Returns:
        str: Отформатированная markdown-ссылка.
    """
```

**Назначение**: Форматирует URL и заголовок в виде markdown-ссылки. Если заголовок не указан, он извлекается из URL.

**Параметры**:

-   `url` (str): URL для ссылки.
-   `title` (Optional[str], optional): Заголовок для отображения. Если `None`, извлекается из URL.

**Возвращает**:

-   `str`: Отформатированная markdown-ссылка.

**Как работает функция**:

1.  Если заголовок не указан, пытается извлечь его из URL.
2.  Если заголовок не может быть извлечен из URL, то в качестве заголовка используется сам URL.
3.  Кодирует URL, используя функцию `quote_url`.
4.  Форматирует URL и заголовок в виде markdown-ссылки.

**ASCII flowchart**:

```
A[Проверка, указан ли заголовок]
|
B[Если заголовок не указан, извлечение его из URL]
|
C[Если заголовок не может быть извлечен, использование URL в качестве заголовка]
|
D[Кодирование URL]
|
E[Форматирование URL и заголовка в виде markdown-ссылки]
|
F[Возврат отформатированной markdown-ссылки]
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
    Форматирует заданное изображение в виде markdown-строки.

    Args:
        image (str): Изображение для форматирования.
        alt (str): Альтернативный текст для изображения.
        preview (Optional[str], optional): URL для предварительного просмотра. По умолчанию используется оригинальное изображение.

    Returns:
        str: Отформатированная markdown-строка.
    """
```

**Назначение**: Форматирует изображение в виде markdown-строки с возможностью указания URL предварительного просмотра.

**Параметры**:

-   `image` (str): URL изображения.
-   `alt` (str): Альтернативный текст для изображения.
-   `preview` (Optional[str], optional): URL для предварительного просмотра. Если не указан, используется оригинальное изображение.

**Возвращает**:

-   `str`: Отформатированная markdown-строка.

**Как работает функция**:

1.  Если указан URL предварительного просмотра, заменяет `{image}` в URL предварительного просмотра на URL изображения.
2.  Кодирует URL изображения и URL предварительного просмотра, используя функцию `quote_url`.
3.  Форматирует изображение в виде markdown-строки.

**ASCII flowchart**:

```
A[Проверка, указан ли URL предварительного просмотра]
|
B[Замена '{image}' в URL предварительного просмотра на URL изображения]
|
C[Кодирование URL предварительного просмотра]
|
D[Кодирование URL изображения]
|
E[Форматирование изображения в виде markdown-строки]
|
F[Возврат отформатированной markdown-строки]
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
    Форматирует заданные изображения в виде markdown-строки.

    Args:
        images (Union[str, List[str]]): Изображение или список изображений для форматирования.
        alt (str): Альтернативный текст для изображений.
        preview (Union[str, List[str]], optional): URL формат или список URL для предварительного просмотра.
            Если не указан, используются оригинальные изображения.

    Returns:
        str: Отформатированная markdown-строка.
    """
```

**Назначение**: Форматирует одно или несколько изображений в виде markdown-строки.

**Параметры**:

-   `images` (Union[str, List[str]]): Изображение или список изображений для форматирования.
-   `alt` (str): Альтернативный текст для изображений.
-   `preview` (Union[str, List[str]], optional): URL предварительного просмотра или список URL. Если не указан, используются оригинальные изображения.

**Возвращает**:

-   `str`: Отформатированная markdown-строка.

**Как работает функция**:

1.  Если `images` - список и содержит только один элемент, то `images` присваивается этот элемент.
2.  Если `images` - строка, то форматирует изображение, используя функцию `format_image`.
3.  Если `images` - список, то форматирует каждое изображение в списке, используя функцию `format_image`, и объединяет их в одну строку, разделяя символом новой строки `\n`.
4.  Добавляет флаги начала и конца (`<!-- generated images start -->` и `<!-- generated images end -->`) для обозначения сгенерированных изображений.

**ASCII flowchart**:

```
A[Проверка, является ли images списком и содержит ли один элемент]
|
B[Если да, присваивание images единственного элемента списка]
|
C[Проверка, является ли images строкой]
|
D[Если да, форматирование изображения с помощью format_image]
|
E[Если нет, форматирование каждого изображения в списке с помощью format_image и объединение их в строку]
|
F[Добавление флагов начала и конца для обозначения сгенерированных изображений]
|
G[Возврат отформатированной markdown-строки]
```

**Примеры**:

```python
>>> format_images_markdown('https://example.com/image.jpg', 'Example Image')
'\n<!-- generated images start -->\n[![Example Image](https://example.com/image.jpg)](https://example.com/image.jpg)\n<!-- generated images end -->\n'
>>> format_images_markdown(['https://example.com/image1.jpg', 'https://example.com/image2.jpg'], 'Example Image', ['https://example.com/preview1', 'https://example.com/preview2'])
'\n<!-- generated images start -->\n[![#1 Example Image](https://example.com/preview1)](https://example.com/image1.jpg)\n[![#2 Example Image](https://example.com/preview2)](https://example.com/image2.jpg)\n<!-- generated images end -->\n'
```

## Классы

### `ResponseType`

```python
class ResponseType:
    """
    Абстрактный базовый класс для всех типов ответов.
    """
```

**Описание**: Абстрактный базовый класс для всех типов ответов.

**Методы**:

-   `__str__`: Абстрактный метод для преобразования ответа в строковое представление.

#### `__str__`

```python
    @abstractmethod
    def __str__(self) -> str:
        """Convert the response to a string representation."""
        raise NotImplementedError
```

**Назначение**: Преобразует ответ в строковое представление. Этот метод должен быть реализован в подклассах.

**Параметры**:

-   Нет

**Возвращает**:

-   `str`: Строковое представление ответа.

**Вызывает исключения**:

-   `NotImplementedError`: Если метод не реализован в подклассе.

### `JsonMixin`

```python
class JsonMixin:
    """
    Миксин для классов, которые могут быть представлены в виде JSON.
    """
```

**Описание**: Миксин для классов, которые могут быть представлены в виде JSON.

**Методы**:

-   `__init__`: Инициализирует объект с атрибутами, переданными в виде ключевых слов.
-   `get_dict`: Возвращает словарь атрибутов объекта, исключая приватные атрибуты (начинающиеся с `__`).
-   `reset`: Сбрасывает все атрибуты объекта.

#### `__init__`

```python
    def __init__(self, **kwargs) -> None:
        """Initialize with keyword arguments as attributes."""
        for key, value in kwargs.items():
            setattr(self, key, value)
```

**Назначение**: Инициализирует объект атрибутами, переданными в виде ключевых слов.

**Параметры**:

-   `**kwargs`: Ключевые слова и значения для инициализации атрибутов объекта.

**Как работает функция**:

Перебирает все переданные ключевые слова и устанавливает их как атрибуты объекта с соответствующими значениями.

#### `get_dict`

```python
    def get_dict(self) -> Dict:
        """Return a dictionary of non-private attributes."""
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("__")
        }
```

**Назначение**: Возвращает словарь атрибутов объекта, исключая приватные атрибуты (начинающиеся с `__`).

**Параметры**:

-   Нет

**Возвращает**:

-   `Dict`: Словарь атрибутов объекта.

**Как работает функция**:

Создает словарь, перебирая все атрибуты объекта и добавляя только те, которые не начинаются с `__`.

#### `reset`

```python
    def reset(self) -> None:
        """Reset all attributes."""
        self.__dict__ = {}
```

**Назначение**: Сбрасывает все атрибуты объекта.

**Параметры**:

-   Нет

**Как работает функция**:

Устанавливает `__dict__` объекта в пустой словарь, удаляя все атрибуты.

### `RawResponse`

```python
class RawResponse(ResponseType, JsonMixin):
    pass
```

**Описание**: Класс для представления "сырого" ответа, наследуется от `ResponseType` и `JsonMixin`.

### `HiddenResponse`

```python
class HiddenResponse(ResponseType):
    """
    Базовый класс для скрытых ответов.
    """
```

**Описание**: Базовый класс для скрытых ответов, наследуется от `ResponseType`.

**Методы**:

-   `__str__`: Возвращает пустую строку.

#### `__str__`

```python
    def __str__(self) -> str:
        """Hidden responses return an empty string."""
        return ""
```

**Назначение**: Возвращает пустую строку.

**Параметры**:

-   Нет

**Возвращает**:

-   `str`: Пустая строка.

**Как работает функция**:

Всегда возвращает пустую строку, что делает ответ невидимым.

### `FinishReason`

```python
class FinishReason(JsonMixin, HiddenResponse):
    """
    Класс для представления причины завершения.
    """
```

**Описание**: Класс для представления причины завершения, наследуется от `JsonMixin` и `HiddenResponse`.

**Атрибуты**:

-   `reason` (str): Причина завершения.

**Методы**:

-   `__init__`: Инициализирует объект с причиной завершения.

#### `__init__`

```python
    def __init__(self, reason: str) -> None:
        """Initialize with a reason."""
        self.reason = reason
```

**Назначение**: Инициализирует объект с причиной завершения.

**Параметры**:

-   `reason` (str): Причина завершения.

**Как работает функция**:

Устанавливает атрибут `reason` объекта в переданное значение.

### `ToolCalls`

```python
class ToolCalls(HiddenResponse):
    """
    Класс для представления списка вызовов инструментов.
    """
```

**Описание**: Класс для представления списка вызовов инструментов, наследуется от `HiddenResponse`.

**Атрибуты**:

-   `list` (List): Список вызовов инструментов.

**Методы**:

-   `__init__`: Инициализирует объект списком вызовов инструментов.
-   `get_list`: Возвращает список вызовов инструментов.

#### `__init__`

```python
    def __init__(self, list: List) -> None:
        """Initialize with a list of tool calls."""
        self.list = list
```

**Назначение**: Инициализирует объект списком вызовов инструментов.

**Параметры**:

-   `list` (List): Список вызовов инструментов.

**Как работает функция**:

Устанавливает атрибут `list` объекта в переданное значение.

#### `get_list`

```python
    def get_list(self) -> List:
        """Return the list of tool calls."""
        return self.list
```

**Назначение**: Возвращает список вызовов инструментов.

**Параметры**:

-   Нет

**Возвращает**:

-   `List`: Список вызовов инструментов.

**Как работает функция**:

Возвращает значение атрибута `list` объекта.

### `Usage`

```python
class Usage(JsonMixin, HiddenResponse):
    pass
```

**Описание**: Класс для представления информации об использовании, наследуется от `JsonMixin` и `HiddenResponse`.

### `AuthResult`

```python
class AuthResult(JsonMixin, HiddenResponse):
    pass
```

**Описание**: Класс для представления результата аутентификации, наследуется от `JsonMixin` и `HiddenResponse`.

### `TitleGeneration`

```python
class TitleGeneration(HiddenResponse):
    """
    Класс для представления сгенерированного заголовка.
    """
```

**Описание**: Класс для представления сгенерированного заголовка, наследуется от `HiddenResponse`.

**Атрибуты**:

-   `title` (str): Сгенерированный заголовок.

**Методы**:

-   `__init__`: Инициализирует объект с заголовком.

#### `__init__`

```python
    def __init__(self, title: str) -> None:
        """Initialize with a title."""
        self.title = title
```

**Назначение**: Инициализирует объект с заголовком.

**Параметры**:

-   `title` (str): Сгенерированный заголовок.

**Как работает функция**:

Устанавливает атрибут `title` объекта в переданное значение.

### `DebugResponse`

```python
class DebugResponse(HiddenResponse):
    """
    Класс для представления отладочного сообщения.
    """
```

**Описание**: Класс для представления отладочного сообщения, наследуется от `HiddenResponse`.

**Атрибуты**:

-   `log` (str): Отладочное сообщение.

**Методы**:

-   `__init__`: Инициализирует объект с отладочным сообщением.

#### `__init__`

```python
    def __init__(self, log: str) -> None:
        """Initialize with a log message."""
        self.log = log
```

**Назначение**: Инициализирует объект с отладочным сообщением.

**Параметры**:

-   `log` (str): Отладочное сообщение.

**Как работает функция**:

Устанавливает атрибут `log` объекта в переданное значение.

### `Reasoning`

```python
class Reasoning(ResponseType):
    """
    Класс для представления рассуждений.
    """
```

**Описание**: Класс для представления рассуждений, наследуется от `ResponseType`.

**Атрибуты**:

-   `token` (Optional[str], optional): Токен рассуждения.
-   `label` (Optional[str], optional): Метка рассуждения.
-   `status` (Optional[str], optional): Статус рассуждения.
-   `is_thinking` (Optional[str], optional): Состояние "размышления".

**Методы**:

-   `__init__`: Инициализирует объект с токеном, статусом и состоянием "размышления".
-   `__str__`: Возвращает строковое представление на основе доступных атрибутов.
-   `__eq__`: Сравнивает два объекта `Reasoning` на равенство.
-   `get_dict`: Возвращает словарное представление рассуждения.

#### `__init__`

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

**Назначение**: Инициализирует объект с токеном, статусом и состоянием "размышления".

**Параметры**:

-   `token` (Optional[str], optional): Токен рассуждения.
-   `label` (Optional[str], optional): Метка рассуждения.
-   `status` (Optional[str], optional): Статус рассуждения.
-   `is_thinking` (Optional[str], optional): Состояние "размышления".

**Как работает функция**:

Устанавливает атрибуты объекта в переданные значения.

#### `__str__`

```python
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
```

**Назначение**: Возвращает строковое представление на основе доступных атрибутов.

**Параметры**:

-   Нет

**Возвращает**:

-   `str`: Строковое представление рассуждения.

**Как работает функция**:

Возвращает строковое представление рассуждения на основе следующих правил:

1.  Если атрибут `is_thinking` не `None`, возвращает его значение.
2.  Если атрибут `token` не `None`, возвращает его значение.
3.  Если атрибут `status` не `None`, то:
    *   Если атрибут `label` не `None`, возвращает строку в формате `"{self.label}: {self.status}\n"`.
    *   Иначе возвращает строку в формате `"{self.status}\n"`.
4.  Иначе возвращает пустую строку.

#### `__eq__`

```python
    def __eq__(self, other: Reasoning):
        return (self.token == other.token and
                self.status == other.status and
                self.is_thinking == other.is_thinking)
```

**Назначение**: Сравнивает два объекта `Reasoning` на равенство.

**Параметры**:

-   `other` (Reasoning): Объект `Reasoning` для сравнения.

**Возвращает**:

-   `bool`: `True`, если объекты равны, `False` в противном случае.

**Как работает функция**:

Возвращает `True`, если атрибуты `token`, `status` и `is_thinking` обоих объектов равны, `False` в противном случае.

#### `get_dict`

```python
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

**Назначение**: Возвращает словарное представление рассуждения.

**Параметры**:

-   Нет

**Возвращает**:

-   `Dict`: Словарное представление рассуждения.

**Как работает функция**:

Возвращает словарь, представляющий рассуждение, на основе следующих правил:

1.  Если атрибут `label` не `None`, возвращает словарь с ключами `"label"` и `"status"`.
2.  Если атрибут `is_thinking` равен `None`:
    *   Если атрибут `status` равен `None`, возвращает словарь с ключом `"token"`.
    *   Иначе возвращает словарь с ключами `"token"` и `"status"`.
3.  Иначе возвращает словарь с ключами `"token"`, `"status"` и `"is_thinking"`.

### `Sources`

```python
class Sources(ResponseType):
    """
    Класс для представления источников.
    """
```

**Описание**: Класс для представления источников, наследуется от `ResponseType`.

**Атрибуты**:

-   `list` (List[Dict[str, str]]): Список словарей источников.

**Методы**:

-   `__init__`: Инициализирует объект списком словарей источников.
-   `add_source`: Добавляет источник в список, очищая URL при необходимости.
-   `__str__`: Возвращает отформатированные источники в виде строки.

#### `__init__`

```python
    def __init__(self, sources: List[Dict[str, str]]) -> None:
        """Initialize with a list of source dictionaries."""
        self.list = []
        for source in sources:
            self.add_source(source)
```

**Назначение**: Инициализирует объект списком словарей источников.

**Параметры**:

-   `sources` (List[Dict[str, str]]): Список словарей источников.

**Как работает функция**:

1.  Инициализирует атрибут `list` пустым списком.
2.  Перебирает все источники в списке `sources` и добавляет их в список `list`, используя метод `add_source`.

#### `add_source`

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

-   `source` (Union[Dict[str, str], str]): Источник (словарь или строка).

**Как работает функция**:

1.  Если `source` является строкой, то преобразует ее в словарь с ключом `"url"`.
2.  Извлекает URL из источника, используя ключи `"url"` или `"link"`.
3.  Если URL не `None`, то:
    *   Удаляет параметры `utm_source` из URL.
    *   Устанавливает очищенный URL в словаре `source`.
    *   Добавляет источник в список `list`.

#### `__str__`

```python
    def __str__(self) -> str:
        """Return formatted sources as a string."""
        if not self.list:
            return ""
        return "\n\n\n\n" + ("\n>\n".join([
            f"> [{idx}] {format_link(link['url'], link.get('title', None))}"
            for idx, link in enumerate(self.list)
        ]))
```

**Назначение**: Возвращает отформатированные источники в виде строки.

**Параметры**:

-   Нет

**Возвращает**:

-   `str`: Отформатированные источники в виде строки.

**Как работает функция**:

1.  Если список `list` пустой, возвращает пустую строку.
2.  Иначе форматирует каждый источник в списке, используя функцию `format_link`, и объединяет их в одну строку, разделяя символами новой строки `\n` и `>\n`.

### `YouTube`

```python
class YouTube(HiddenResponse):
    """
    Класс для представления YouTube видео.
    """
```

**Описание**: Класс для представления YouTube видео, наследуется от `HiddenResponse`.

**Атрибуты**:

-   `ids` (List[str]): Список идентификаторов YouTube видео.

**Методы**:

-   `__init__`: Инициализирует объект списком идентификаторов YouTube видео.
-   `to_string`: Возвращает HTML-код для встраивания YouTube видео.

#### `__init__`

```python
    def __init__(self, ids: List[str]) -> None:
        """Initialize with a list of YouTube IDs."""
        self.ids = ids
```

**Назначение**: Инициализирует объект списком идентификаторов YouTube видео.

**Параметры**:

-   `ids` (List[str]): Список идентификаторов YouTube видео.

**Как работает функция**:

Устанавливает атрибут `ids` объекта в переданное значение.

#### `to_string`

```python
    def to_string(self) -> str:
        """Return YouTube embeds as a string."""
        if not self.ids:
            return ""
        return "\n\n" + ("\n".join([
            f'<iframe type="text/html" src="https://www.youtube.com/embed/{id}"></iframe>'
            for id in self.ids
        ]))
```

**Назначение**: Возвращает HTML-код для встраивания YouTube видео.

**Параметры**:

-   Нет

**Возвращает**:

-   `str`: HTML-код для встраивания YouTube видео.

**Как работает функция**:

1.  Если список `ids` пустой, возвращает пустую строку.
2.  Иначе создает HTML-код для встраивания каждого YouTube видео в списке и объединяет их в одну строку, разделяя символами новой строки `\n`.

### `AudioResponse`

```python
class AudioResponse(ResponseType):
    """
    Класс для представления аудио ответа.
    """
```

**Описание**: Класс для представления аудио ответа, наследуется от `ResponseType`.

**Атрибуты**:

-   `data` (Union[bytes, str]): Аудио данные (байты или URI).

**Методы**:

-   `__init__`: Инициализирует объект аудио данными.
-   `to_uri`: Возвращает аудио данные в виде URI данных в формате base64.
-   `__str__`: Возвращает аудио в виде HTML-элемента.

#### `__init__`

```python
    def __init__(self, data: Union[bytes, str]) -> None:
        """Initialize with audio data bytes."""
        self.data = data
```

**Назначение**: Инициализирует объект аудио данными.

**Параметры**:

-   `data` (Union[bytes, str]): Аудио данные (байты или URI).

**Как работает функция**:

Устанавливает атрибут `data` объекта в переданное значение.

#### `to_uri`

```python
    def to_uri(self) -> str:
        if isinstance(self.data, str):
            return self.data
        """Return audio data as a base64-encoded data URI."""
        data_base64 = base64.b64encode(self.data).decode()
        return f"data:audio/mpeg;base64,{data_base64}"
```

**Назначение**: Возвращает аудио данные в виде URI данных в формате base64.

**Параметры**:

-   Нет

**Возвращает**:

-   `str`: Аудио данные в виде URI данных в формате base64.

**Как работает функция**:

1. Если `self.data` - строка, возвращает ее.
2. Кодирует аудио данные в формат base64.
3. Форматирует аудио данные в виде URI данных в формате base64.

#### `__str__`

```python
    def __str__(self) -> str:
        """Return audio as html element."""
        return f'<audio controls src="{self.to_uri()}"></audio>'
```

**Назначение**: Возвращает аудио в виде HTML-элемента.

**Параметры**:

-   Нет

**Возвращает**:

-   `str`: Аудио в виде HTML-элемента.

**Как работает функция**:

Форматирует аудио данные в виде HTML-элемента `<audio>`.

### `BaseConversation`

```python
class BaseConversation(ResponseType):
    """
    Базовый класс для представления разговора.
    """
```

**Описание**: Базовый класс для представления разговора, наследуется от `ResponseType`.

**Методы**:

-   `__str__`: Возвращает пустую строку по