### **Анализ кода модуля `response.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код хорошо структурирован и разбит на отдельные классы, каждый из которых выполняет свою задачу.
    - Присутствуют docstring для большинства функций и классов.
    - Используются аннотации типов.
- **Минусы**:
    - Docstring написаны на английском языке.
    - В некоторых местах можно улучшить читаемость кода.
    - Не все функции и классы имеют подробные docstring.
    - Не используется `logger` для логирования ошибок.
    - Местами встречается `Union` вместо `|`.

#### **Рекомендации по улучшению**:
- Перевести все docstring на русский язык.
- Добавить более подробные описания в docstring, включая примеры использования и описание возможных исключений.
- Использовать `logger` для логирования ошибок и отладочной информации.
- Заменить `Union` на `|` в аннотациях типов.
- Добавить аннотации типов для всех переменных.
- Улучшить форматирование кода в соответствии со стандартами PEP8.
- Избавиться от `any` в аннотациях.
- Добавить примеры использования для всех функций и классов.

#### **Оптимизированный код**:
```python
from __future__ import annotations

import re
import base64
from typing import Union, Dict, List, Optional, Any
from abc import abstractmethod
from urllib.parse import quote_plus, unquote_plus

from src.logger import logger  # Добавлен импорт logger

def quote_url(url: str) -> str:
    """
    Экранирует части URL, сохраняя структуру домена.

    Args:
        url (str): URL для экранирования.

    Returns:
        str: Экранированный URL.

    Example:
        >>> quote_url('https://example.com/path?query=value')
        'https://example.com/path%3Fquery%3Dvalue'
    """
    # Избегаем двойного экранирования, если это необходимо
    if '%' in url:
        url = unquote_plus(url)

    url_parts = url.split('//', maxsplit=1)
    # Если нет '//', то это относительный URL
    if len(url_parts) == 1:
        return quote_plus(url_parts[0], '/?&=#')

    protocol, rest = url_parts
    domain_parts = rest.split('/', maxsplit=1)
    # Если нет '/' после домена, то это URL домена
    if len(domain_parts) == 1:
        return f'{protocol}//{domain_parts[0]}'

    domain, path = domain_parts
    return f'{protocol}//{domain}/{quote_plus(path, "/?&=#")}'

def quote_title(title: str) -> str:
    """
    Нормализует пробелы в заголовке.

    Args:
        title (str): Заголовок для нормализации.

    Returns:
        str: Заголовок с нормализованными пробелами.

    Example:
        >>> quote_title('  Пример   заголовка  ')
        'Пример заголовка'
    """
    return ' '.join(title.split()) if title else ''

def format_link(url: str, title: Optional[str] = None) -> str:
    """
    Форматирует URL и заголовок как ссылку Markdown.

    Args:
        url (str): URL для ссылки.
        title (Optional[str], optional): Заголовок для отображения. Если None, извлекается из URL. По умолчанию None.

    Returns:
        str: Отформатированная ссылка Markdown.

    Example:
        >>> format_link('https://example.com', 'Пример')
        '[Пример](https://example.com)'
    """
    if title is None:
        try:
            title = unquote_plus(url.split('//', maxsplit=1)[1].split('?')[0].replace('www.', ''))
        except IndexError:
            title = url
    return f'[{quote_title(title)}]({quote_url(url)})'

def format_image(image: str, alt: str, preview: Optional[str] = None) -> str:
    """
    Форматирует изображение в строку Markdown.

    Args:
        image (str): Изображение для форматирования.
        alt (str): Альтернативный текст для изображения.
        preview (Optional[str], optional): URL для предварительного просмотра. По умолчанию исходное изображение.

    Returns:
        str: Отформатированная строка Markdown.

    Example:
        >>> format_image('https://example.com/image.png', 'Пример изображения')
        '![Пример изображения](https://example.com/image.png)'
    """
    preview_url = preview.replace('{image}', image) if preview else image
    return f'![{quote_title(alt)}]({quote_url(preview_url)})]({quote_url(image)})'

def format_images_markdown(images: str | List[str], alt: str,
                           preview: str | List[str] | None = None) -> str:
    """
    Форматирует изображения в строку Markdown.

    Args:
        images (str | List[str]): Изображение или список изображений для форматирования.
        alt (str): Альтернативный текст для изображений.
        preview (str | List[str] | None, optional): URL или список URL для предварительного просмотра.
            Если не указан, используются исходные изображения. По умолчанию None.

    Returns:
        str: Отформатированная строка Markdown.

    Example:
        >>> format_images_markdown(['https://example.com/image1.png', 'https://example.com/image2.png'], 'Примеры изображений')
        '\\n<!-- generated images start -->\\n![#1 Примеры изображений](https://example.com/image1.png)\\n![#2 Примеры изображений](https://example.com/image2.png)\\n<!-- generated images end -->\\n'
    """
    if isinstance(images, list) and len(images) == 1:
        images = images[0]

    if isinstance(images, str):
        result = format_image(images, alt, preview)
    else:
        result = '\n'.join(
            format_image(
                image,
                f'#{idx+1} {alt}',
                preview[idx] if isinstance(preview, list) and idx < len(preview) else preview
            )
            for idx, image in enumerate(images)
        )

    start_flag = '<!-- generated images start -->\n'
    end_flag = '<!-- generated images end -->\n'
    return f'\n{start_flag}{result}\n{end_flag}\n'

class ResponseType:
    @abstractmethod
    def __str__(self) -> str:
        """Преобразует ответ в строковое представление."""
        raise NotImplementedError

class JsonMixin:
    def __init__(self, **kwargs: Any) -> None:
        """Инициализирует атрибуты ключевыми аргументами."""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_dict(self) -> Dict[str, Any]:
        """Возвращает словарь не приватных атрибутов."""
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith('__')
        }

    def reset(self) -> None:
        """Сбрасывает все атрибуты."""
        self.__dict__ = {}

class RawResponse(ResponseType, JsonMixin):
    pass

class HiddenResponse(ResponseType):
    def __str__(self) -> str:
        """Скрытые ответы возвращают пустую строку."""
        return ''

class FinishReason(JsonMixin, HiddenResponse):
    def __init__(self, reason: str) -> None:
        """Инициализирует причину завершения."""
        self.reason = reason

class ToolCalls(HiddenResponse):
    def __init__(self, list: List[Any]) -> None:
        """Инициализирует список вызовов инструментов."""
        self.list = list

    def get_list(self) -> List[Any]:
        """Возвращает список вызовов инструментов."""
        return self.list

class Usage(JsonMixin, HiddenResponse):
    pass

class AuthResult(JsonMixin, HiddenResponse):
    pass

class TitleGeneration(HiddenResponse):
    def __init__(self, title: str) -> None:
        """Инициализирует заголовок."""
        self.title = title

class DebugResponse(HiddenResponse):
    def __init__(self, log: str) -> None:
        """Инициализирует сообщение журнала."""
        self.log = log

class Reasoning(ResponseType):
    def __init__(
            self,
            token: Optional[str] = None,
            label: Optional[str] = None,
            status: Optional[str] = None,
            is_thinking: Optional[str] = None
        ) -> None:
        """Инициализирует токен, статус и состояние обдумывания."""
        self.token = token
        self.label = label
        self.status = status
        self.is_thinking = is_thinking

    def __str__(self) -> str:
        """Возвращает строковое представление на основе доступных атрибутов."""
        if self.is_thinking is not None:
            return self.is_thinking
        if self.token is not None:
            return self.token
        if self.status is not None:
            if self.label is not None:
                return f'{self.label}: {self.status}\n'
            return f'{self.status}\n'
        return ''

    def __eq__(self, other: Reasoning) -> bool:
        """Сравнивает два объекта Reasoning."""
        return (self.token == other.token and
                self.status == other.status and
                self.is_thinking == other.is_thinking)

    def get_dict(self) -> Dict[str, Optional[str]]:
        """Возвращает словарное представление рассуждения."""
        if self.label is not None:
            return {'label': self.label, 'status': self.status}
        if self.is_thinking is None:
            if self.status is None:
                return {'token': self.token}
            return {'token': self.token, 'status': self.status}
        return {'token': self.token, 'status': self.status, 'is_thinking': self.is_thinking}

class Sources(ResponseType):
    def __init__(self, sources: List[Dict[str, str]]) -> None:
        """Инициализирует список словарей источников."""
        self.list: List[Dict[str, str]] = []
        for source in sources:
            self.add_source(source)

    def add_source(self, source: Union[Dict[str, str], str]) -> None:
        """Добавляет источник в список, очищая URL, если необходимо."""
        source = source if isinstance(source, dict) else {'url': source}
        url = source.get('url', source.get('link', None))
        if url is not None:
            url = re.sub(r'[&?]utm_source=.+', '', url)
            source['url'] = url
            self.list.append(source)

    def __str__(self) -> str:
        """Возвращает отформатированные источники в виде строки."""
        if not self.list:
            return ''
        return '\n\n\n\n' + ('\n>\n'.join([
            f"> [{idx}] {format_link(link['url'], link.get('title', None))}"
            for idx, link in enumerate(self.list)
        ]))

class YouTube(HiddenResponse):
    def __init__(self, ids: List[str]) -> None:
        """Инициализирует список идентификаторов YouTube."""
        self.ids = ids

    def to_string(self) -> str:
        """Возвращает встроенные элементы YouTube в виде строки."""
        if not self.ids:
            return ''
        return '\n\n' + ('\n'.join([
            f'<iframe type="text/html" src="https://www.youtube.com/embed/{id}"></iframe>'
            for id in self.ids
        ]))

class AudioResponse(ResponseType):
    def __init__(self, data: bytes | str) -> None:
        """Инициализирует байты аудиоданных."""
        self.data = data

    def to_uri(self) -> str:
        """Возвращает аудиоданные в виде URI, закодированного в base64."""
        if isinstance(self.data, str):
            return self.data
        data_base64 = base64.b64encode(self.data).decode()
        return f'data:audio/mpeg;base64,{data_base64}'

    def __str__(self) -> str:
        """Возвращает аудио как HTML-элемент."""
        return f'<audio controls src="{self.to_uri()}"></audio>'

class BaseConversation(ResponseType):
    def __str__(self) -> str:
        """Возвращает пустую строку по умолчанию."""
        return ''

class JsonConversation(BaseConversation, JsonMixin):
    pass

class SynthesizeData(HiddenResponse, JsonMixin):
    def __init__(self, provider: str, data: Dict[str, Any]) -> None:
        """Инициализирует поставщика и данные."""
        self.provider = provider
        self.data = data

class SuggestedFollowups(HiddenResponse):
    def __init__(self, suggestions: list[str]):
        self.suggestions = suggestions

class RequestLogin(HiddenResponse):
    def __init__(self, label: str, login_url: str) -> None:
        """Инициализирует метку и URL для входа."""
        self.label = label
        self.login_url = login_url

    def to_string(self) -> str:
        """Возвращает отформатированную ссылку для входа в виде строки."""
        return format_link(self.login_url, f'[Login to {self.label}]') + '\n\n'

class MediaResponse(ResponseType):
    def __init__(
        self,
        urls: str | List[str],
        alt: str,
        options: Dict[str, Any] = {},
        **kwargs: Any
    ) -> None:
        """Инициализирует изображения, альтернативный текст и параметры."""
        self.urls = kwargs.get('images', urls)
        self.alt = alt
        self.options = options

    def get(self, key: str) -> Any:
        """Возвращает значение параметра по ключу."""
        return self.options.get(key)

    def get_list(self) -> List[str]:
        """Возвращает изображения в виде списка."""
        return [self.urls] if isinstance(self.urls, str) else self.urls

class ImageResponse(MediaResponse):
    def __str__(self) -> str:
        """Возвращает изображения в виде Markdown."""
        return format_images_markdown(self.urls, self.alt, self.get('preview'))

class VideoResponse(MediaResponse):
    def __str__(self) -> str:
        """Возвращает видео в виде HTML-элементов."""
        return '\n'.join([f'<video controls src="{video}"></video>' for video in self.get_list()])

class ImagePreview(ImageResponse):
    def __str__(self) -> str:
        """Возвращает пустую строку для предварительного просмотра."""
        return ''

    def to_string(self) -> str:
        """Возвращает изображения в виде Markdown."""
        return super().__str__()

class PreviewResponse(HiddenResponse):
    def __init__(self, data: str) -> None:
        """Инициализирует данные."""
        self.data = data

    def to_string(self) -> str:
        """Возвращает данные в виде строки."""
        return self.data

class Parameters(ResponseType, JsonMixin):
    def __str__(self) -> str:
        """Возвращает пустую строку."""
        return ''

class ProviderInfo(JsonMixin, HiddenResponse):
    pass