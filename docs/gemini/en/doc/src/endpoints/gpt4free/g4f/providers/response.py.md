# Module g4f.providers.response

## Overview

This module defines various classes for handling and formatting responses from different providers. It includes utilities for quoting URLs, titles, and formatting links and images in markdown. It also defines abstract and concrete response classes for different types of data such as JSON, raw text, hidden messages, reasoning steps, sources, YouTube videos, audio, images, and videos.

## More details

This module provides a structured way to manage and represent different types of responses from various providers. It includes utility functions for formatting URLs and titles, as well as classes for representing different response types like JSON, raw text, and media. The module supports the conversion of responses into string representations, making it easier to handle and display the data in a consistent manner.

## Functions

### `quote_url`

```python
def quote_url(url: str) -> str:
    """
     экранирует части URL, сохраняя структуру домена.

    Args:
        url (str): URL для экранирования.

    Returns:
        str: правильно экранированный URL.
    """
```

**Purpose**: экранирует части URL, сохраняя структуру домена.

**Parameters**:
- `url` (str): URL для экранирования.

**Returns**:
- `str`: правильно экранированный URL.

**How the function works**:
- Если URL содержит символы `%`, он сначала декодируется с помощью `unquote_plus`, чтобы избежать двойного декодирования.
- URL разделяется на части по `//`, чтобы отделить протокол от остальной части URL.
- Если в URL нет `//`, считается, что это относительный URL, и вся строка экранируется с помощью `quote_plus`.
- Если `//` присутствует, URL разделяется на протокол и остальную часть.
- Остальная часть разделяется на домен и путь.
- Если после домена нет `/`, считается, что это URL домена, и возвращается протокол вместе с доменом.
- В противном случае домен и путь объединяются с экранированным путем с помощью `quote_plus`.

**Examples**:
```python
>>> quote_url("https://example.com/path?param=value")
'https://example.com/path%3Fparam%3Dvalue'
>>> quote_url("example.com/path")
'example.com%2Fpath'
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

**Purpose**: Нормализует пробелы в заголовке.

**Parameters**:
- `title` (str): Заголовок для нормализации.

**Returns**:
- `str`: Заголовок с нормализованными пробелами.

**How the function works**:
- Если заголовок существует, он разделяется на слова, и затем слова объединяются с помощью одного пробела между ними.
- Если заголовок пустой, возвращается пустая строка.

**Examples**:
```python
>>> quote_title("Пример   заголовка  с  пробелами")
'Пример заголовка с пробелами'
>>> quote_title("")
''
```

### `format_link`

```python
def format_link(url: str, title: Optional[str] = None) -> str:
    """
    Форматирует URL и заголовок в виде ссылки Markdown.

    Args:
        url (str): URL для ссылки.
        title (Optional[str], optional): Заголовок для отображения. Если `None`, извлекается из URL. По умолчанию `None`.

    Returns:
        str: Отформатированная ссылка Markdown.
    """
```

**Purpose**: Форматирует URL и заголовок в виде ссылки Markdown.

**Parameters**:
- `url` (str): URL для ссылки.
- `title` (Optional[str], optional): Заголовок для отображения. Если `None`, извлекается из URL. По умолчанию `None`.

**Returns**:
- `str`: Отформатированная ссылка Markdown.

**How the function works**:
- Если заголовок не указан, он пытается извлечь его из URL, разделяя URL по `//`, а затем по `?`.
- Если заголовок не может быть извлечен из URL, используется сам URL в качестве заголовка.
- Затем заголовок и URL экранируются с помощью `quote_title` и `quote_url` соответственно.
- Возвращает отформатированную строку Markdown в виде `[заголовок](URL)`.

**Examples**:
```python
>>> format_link("https://example.com/path?param=value", "Пример")
'[Пример](https://example.com/path%3Fparam%3Dvalue)'
>>> format_link("https://example.com/path")
'[example.com/path](https://example.com/path)'
```

### `format_image`

```python
def format_image(image: str, alt: str, preview: Optional[str] = None) -> str:
    """
    Форматирует данное изображение как строку Markdown.

    Args:
        image (str): Изображение для форматирования.
        alt (str): Альтернативный текст для изображения.
        preview (Optional[str], optional): Формат URL предварительного просмотра. По умолчанию используется исходное изображение.

    Returns:
        str: Отформатированная строка Markdown.
    """
```

**Purpose**: Форматирует данное изображение как строку Markdown.

**Parameters**:
- `image` (str): Изображение для форматирования.
- `alt` (str): Альтернативный текст для изображения.
- `preview` (Optional[str], optional): Формат URL предварительного просмотра. По умолчанию используется исходное изображение.

**Returns**:
- `str`: Отформатированная строка Markdown.

**How the function works**:
- Если предоставлен URL предварительного просмотра, он заменяет `{image}` в URL предварительного просмотра на фактический URL изображения.
- Заголовок и URL предварительного просмотра экранируются с помощью `quote_title` и `quote_url` соответственно.
- Возвращает отформатированную строку Markdown в виде `[![alt](preview)](image)`.

**Examples**:
```python
>>> format_image("https://example.com/image.jpg", "Пример", "https://example.com/preview/{image}")
'[![Пример](https://example.com/preview/https%3A//example.com/image.jpg)](https://example.com/image.jpg)'
>>> format_image("https://example.com/image.jpg", "Пример")
'[![Пример](https://example.com/image.jpg)](https://example.com/image.jpg)'
```

### `format_images_markdown`

```python
def format_images_markdown(images: Union[str, List[str]], alt: str,
                           preview: Union[str, List[str]] = None) -> str:
    """
    Форматирует данные изображения как строку Markdown.

    Args:
        images (Union[str, List[str]]): Изображение или список изображений для форматирования.
        alt (str): Альтернативный текст для изображений.
        preview (Union[str, List[str]], optional): Формат URL предварительного просмотра или список URL-адресов предварительного просмотра.
            Если не указано, используются исходные изображения. По умолчанию `None`.

    Returns:
        str: Отформатированная строка Markdown.
    """
```

**Purpose**: Форматирует данное изображение как строку Markdown.

**Parameters**:
- `images` (Union[str, List[str]]): Изображение или список изображений для форматирования.
- `alt` (str): Альтернативный текст для изображений.
- `preview` (Union[str, List[str]], optional): Формат URL предварительного просмотра или список URL-адресов предварительного просмотра. Если не указано, используются исходные изображения. По умолчанию `None`.

**Returns**:
- `str`: Отформатированная строка Markdown.

**How the function works**:
- Если `images` — список, содержащий только одно изображение, оно извлекается из списка.
- Если `images` — строка, вызывается `format_image` для форматирования изображения.
- Если `images` — список, он перебирается, и для каждого изображения вызывается `format_image`.
- Для каждого изображения альтернативный текст формируется как `#idx+1 alt`, где `idx` — индекс изображения.
- Результаты объединяются с помощью `\n`.
- Результат обрамляется флагами `<!-- generated images start -->` и `<!-- generated images end -->`.

**Examples**:
```python
>>> format_images_markdown("https://example.com/image.jpg", "Пример")
'\n<!-- generated images start -->\n[![Пример](https://example.com/image.jpg)](https://example.com/image.jpg)\n<!-- generated images end -->\n'
>>> format_images_markdown(["https://example.com/image1.jpg", "https://example.com/image2.jpg"], "Пример", ["https://example.com/preview1/{image}", "https://example.com/preview2/{image}"])
'\n<!-- generated images start -->\n[![#1 Пример](https://example.com/preview1/https%3A//example.com/image1.jpg)](https://example.com/image1.jpg)\\n[![#2 Пример](https://example.com/preview2/https%3A//example.com/image2.jpg)](https://example.com/image2.jpg)\n<!-- generated images end -->\n'
```

## Classes

### `ResponseType`

**Description**: Абстрактный базовый класс для всех типов ответа.

**Methods**:
- `__str__`: Преобразует ответ в строковое представление.

### `JsonMixin`

**Description**: Миксин для классов, которые могут быть представлены в виде JSON.

**Methods**:
- `__init__`: Инициализирует с помощью ключевых аргументов в качестве атрибутов.
- `get_dict`: Возвращает словарь не приватных атрибутов.
- `reset`: Сбрасывает все атрибуты.

### `RawResponse`

**Description**: Класс для представления необработанного ответа.
**Inherits**:
- `ResponseType`: Базовый класс для всех типов ответов.
- `JsonMixin`: Миксин для классов, которые могут быть представлены в виде JSON.

### `HiddenResponse`

**Description**: Базовый класс для скрытых ответов, которые не должны отображаться.

**Methods**:
- `__str__`: Возвращает пустую строку.

### `FinishReason`

**Description**: Класс для представления причины завершения.
**Inherits**:
- `HiddenResponse`: Базовый класс для скрытых ответов.
- `JsonMixin`: Миксин для классов, которые могут быть представлены в виде JSON.

**Methods**:
- `__init__`: Инициализирует с причиной.

### `ToolCalls`

**Description**: Класс для представления вызовов инструментов.
**Inherits**:
- `HiddenResponse`: Базовый класс для скрытых ответов.

**Methods**:
- `__init__`: Инициализирует списком вызовов инструментов.
- `get_list`: Возвращает список вызовов инструментов.

### `Usage`

**Description**: Класс для представления информации об использовании.
**Inherits**:
- `HiddenResponse`: Базовый класс для скрытых ответов.
- `JsonMixin`: Миксин для классов, которые могут быть представлены в виде JSON.

### `AuthResult`

**Description**: Класс для представления результата аутентификации.
**Inherits**:
- `HiddenResponse`: Базовый класс для скрытых ответов.
- `JsonMixin`: Миксин для классов, которые могут быть представлены в виде JSON.

### `TitleGeneration`

**Description**: Класс для представления сгенерированного заголовка.
**Inherits**:
- `HiddenResponse`: Базовый класс для скрытых ответов.

**Methods**:
- `__init__`: Инициализирует заголовком.

### `DebugResponse`

**Description**: Класс для представления отладочного сообщения.
**Inherits**:
- `HiddenResponse`: Базовый класс для скрытых ответов.

**Methods**:
- `__init__`: Инициализирует сообщением журнала.

### `Reasoning`

**Description**: Класс для представления этапа рассуждения.
**Inherits**:
- `ResponseType`: Базовый класс для всех типов ответов.

**Methods**:
- `__init__`: Инициализирует с помощью токена, статуса и состояния мышления.
- `__str__`: Возвращает строковое представление на основе доступных атрибутов.
- `__eq__`: Сравнивает два экземпляра класса `Reasoning` на равенство.
- `get_dict`: Возвращает словарное представление рассуждения.

### `Sources`

**Description**: Класс для представления списка источников.
**Inherits**:
- `ResponseType`: Базовый класс для всех типов ответов.

**Methods**:
- `__init__`: Инициализирует списком словарных источников.
- `add_source`: Добавляет источник в список, при необходимости очищая URL.
- `__str__`: Возвращает отформатированные источники в виде строки.

### `YouTube`

**Description**: Класс для представления списка идентификаторов YouTube.
**Inherits**:
- `HiddenResponse`: Базовый класс для скрытых ответов.

**Methods**:
- `__init__`: Инициализирует списком идентификаторов YouTube.
- `to_string`: Возвращает вложения YouTube в виде строки.

### `AudioResponse`

**Description**: Класс для представления аудиоданных.
**Inherits**:
- `ResponseType`: Базовый класс для всех типов ответов.

**Methods**:
- `__init__`: Инициализирует с помощью байтов аудиоданных.
- `to_uri`: Возвращает аудиоданные в виде URI данных, закодированных в base64.
- `__str__`: Возвращает аудио в виде html-элемента.

### `BaseConversation`

**Description**: Базовый класс для всех типов разговоров.
**Inherits**:
- `ResponseType`: Базовый класс для всех типов ответов.

**Methods**:
- `__str__`: Возвращает пустую строку по умолчанию.

### `JsonConversation`

**Description**: Класс для представления JSON-разговора.
**Inherits**:
- `BaseConversation`: Базовый класс для всех типов разговоров.
- `JsonMixin`: Миксин для классов, которые могут быть представлены в виде JSON.

### `SynthesizeData`

**Description**: Класс для представления данных синтеза.
**Inherits**:
- `HiddenResponse`: Базовый класс для скрытых ответов.
- `JsonMixin`: Миксин для классов, которые могут быть представлены в виде JSON.

**Methods**:
- `__init__`: Инициализирует с помощью поставщика и данных.

### `SuggestedFollowups`

**Description**: Класс для представления предлагаемых последующих действий.
**Inherits**:
- `HiddenResponse`: Базовый класс для скрытых ответов.

**Methods**:
- `__init__`: Инициализирует с помощью списка предложений.

### `RequestLogin`

**Description**: Класс для представления запроса на вход в систему.
**Inherits**:
- `HiddenResponse`: Базовый класс для скрытых ответов.

**Methods**:
- `__init__`: Инициализирует с помощью метки и URL-адреса для входа в систему.
- `to_string`: Возвращает отформатированную ссылку для входа в систему в виде строки.

### `MediaResponse`

**Description**: Базовый класс для ответов, содержащих медиаданные (изображения, видео).
**Inherits**:
- `ResponseType`: Базовый класс для всех типов ответов.

**Methods**:
- `__init__`: Инициализирует с помощью URL-адресов изображений, альтернативного текста и параметров.
- `get`: Получает значение параметра по ключу.
- `get_list`: Возвращает изображения в виде списка.

### `ImageResponse`

**Description**: Класс для представления ответа с изображением.
**Inherits**:
- `MediaResponse`: Базовый класс для ответов, содержащих медиаданные.

**Methods**:
- `__str__`: Возвращает изображения в виде Markdown.

### `VideoResponse`

**Description**: Класс для представления видеоответа.
**Inherits**:
- `MediaResponse`: Базовый класс для ответов, содержащих медиаданные.

**Methods**:
- `__str__`: Возвращает видео в виде html-элементов.

### `ImagePreview`

**Description**: Класс для предварительного просмотра изображения.
**Inherits**:
- `ImageResponse`: Класс для представления ответа с изображением.

**Methods**:
- `__str__`: Возвращает пустую строку для предварительного просмотра.
- `to_string`: Возвращает изображения в виде Markdown.

### `PreviewResponse`

**Description**: Класс для ответа предварительного просмотра.
**Inherits**:
- `HiddenResponse`: Базовый класс для скрытых ответов.

**Methods**:
- `__init__`: Инициализирует с помощью данных.
- `to_string`: Возвращает данные в виде строки.

### `Parameters`

**Description**: Класс для представления параметров.
**Inherits**:
- `ResponseType`: Базовый класс для всех типов ответов.
- `JsonMixin`: Миксин для классов, которые могут быть представлены в виде JSON.

**Methods**:
- `__str__`: Возвращает пустую строку.

### `ProviderInfo`

**Description**: Класс для представления информации о поставщике.
**Inherits**:
- `JsonMixin`: Миксин для классов, которые могут быть представлены в виде JSON.
- `HiddenResponse`: Базовый класс для скрытых ответов.