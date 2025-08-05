# Модуль для очистки и упрощения HTML-кода

## Обзор

Модуль `html_simplification` предназначен для минимизации и очистки HTML-кода. Он удаляет нежелательные теги и атрибуты, обрабатывает особые случаи, такие как скрипты, стили и комментарии. Основной акцент делается на содержимом тега `<body>`. Модуль также позволяет удалять "незначимые" теги-контейнеры, сохраняя только те теги, которые содержат текст или являются допустимыми пустыми тегами (например, `<br>`). Для надежного парсинга HTML используется библиотека `BeautifulSoup`.

## Подробней

Этот модуль предоставляет функции для упрощения HTML-кода, делая его более читаемым и легким для обработки. Он использует библиотеку `BeautifulSoup` для парсинга HTML и класс `Config` для управления параметрами упрощения. Модуль позволяет удалять HTML-комментарии, скрипты, стили, нормализовать пробелы и сохранять только значимые теги.

## Классы

### `Config`

**Описание**: Класс `Config` предоставляет конфигурацию для функции `simplify_html`. Он определяет, какие теги и атрибуты следует сохранить, какие теги нужно развернуть (удалить, оставив только содержимое), а также другие параметры очистки HTML.

**Атрибуты**:

-   `allowed_tags` (Set[str]): Множество тегов в нижнем регистре, которые нужно оставить. Если пустое, все теги остаются.
-   `allowed_attributes` (Dict[str, Set[str]]): Словарь, где ключи - имена тегов (в нижнем регистре), а значения - множества разрешенных атрибутов для этого тега.
-   `unwrap_tags` (Set[str]): Множество тегов (в нижнем регистре), которые нужно "развернуть" (удалить тег, оставив содержимое) на финальном этапе, независимо от других правил.
-   `VOID_TAGS` (Set[str]): Множество тегов, считающихся "пустыми" (void elements), используется при `keep_only_significant=True`.
-   `remove_comments` (bool): Определяет, нужно ли удалять HTML-комментарии (`<!-- ... -->`).
-   `remove_scripts_styles` (bool): Определяет, нужно ли удалять теги `<script>` и `<style>` вместе с их содержимым.
-   `normalize_whitespace` (bool): Определяет, нужно ли заменять множественные пробелы на один и удалять пробелы в начале/конце.
-   `keep_only_significant` (bool): Определяет, нужно ли удалять теги, не содержащие значимый контент.
-   `parser` (str): Парсер для BeautifulSoup (`'html.parser'`, `'lxml'`, `'html5lib'`).

```python
@dataclass
class Config:
    """
    Конфигурация для функции simplify_html.
    """
    allowed_tags: Set[str] = field(default_factory=lambda: {'p', 'b', 'a', 'br', 'img', 'h1', 'hr', 'div', 'span', 'table', 'tbody', 'tr', 'td', 'th', 'ul', 'ol', 'li', 'strong', 'em', 'i', 'u'})
    allowed_attributes: Dict[str, Set[str]] = field(default_factory=lambda: {'a': {'href', 'title'}, 'img': {'src', 'alt', 'title'}, '*': {'style'}})
    unwrap_tags: Set[str] = field(default_factory=set)
    VOID_TAGS: Set[str] = field(default_factory=lambda: {
        'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
        'link', 'meta', 'param', 'source', 'track', 'wbr'
    })
    remove_comments: bool = True
    remove_scripts_styles: bool = True
    normalize_whitespace: bool = True
    keep_only_significant: bool = False
    parser: str = 'html.parser'
```

## Функции

### `strip_tags`

```python
def strip_tags(html_content: str | None, parser: Optional[str] = None) -> str:
    """
    Полностью удаляет все HTML/XML теги из строки, оставляя только текст.
    Также преобразует HTML-сущности (типа &) в соответствующие символы.
    Фокусируется на содержимом тега <body>, если он присутствует.

    Args:
        html_content (str | None): Строка с HTML-кодом или None.
        parser (Optional[str]): Парсер для BeautifulSoup ('html.parser', 'lxml', 'html5lib').
                                Если None, используется 'html.parser'.

    Returns:
        str: Текст без HTML-тегов. Возвращает пустую строку при ошибке, None или пустом вводе.

    Raises:
        Exception: BeautifulSoup может генерировать исключения при серьезных проблемах парсинга,
                   которые логируются.

    Example:
        >>> html_input = '<html><head><title>T</title></head><body><p>Hello <b>World</b>!</p><!-- comment --></body></html>'
        >>> strip_tags(html_input)
        'Hello World !'
        >>> strip_tags('Текст с <сущностями> & символами')
        'Текст с <сущностями> & символами'
        >>> strip_tags(None)
        ''
    """
```

**Назначение**: Функция `strip_tags` полностью удаляет все HTML/XML теги из входной строки, оставляя только текст. Она также преобразует HTML-сущности (например, `&amp;`) в соответствующие символы.

**Параметры**:

-   `html_content` (str | None): Строка с HTML-кодом. Если `None`, функция возвращает пустую строку.
-   `parser` (Optional[str]): Парсер для `BeautifulSoup`. Если не указан, используется `'html.parser'`

**Возвращает**:

-   `str`: Текст без HTML-тегов. Возвращает пустую строку в случае ошибки, `None` или пустом входном значении.

**Вызывает исключения**:

-   `Exception`: Возникает, если `BeautifulSoup` сталкивается с серьезными проблемами при парсинге HTML.

**Как работает функция**:

1.  Функция проверяет входные данные на `None` или некорректный тип.
2.  Инициализирует `BeautifulSoup` с использованием указанного парсера (или парсера по умолчанию).
3.  Находит тег `<body>` в HTML-коде. Если тег `<body>` не найден, обрабатывает весь контент как тело.
4.  Удаляет все теги `<script>` и `<style>`.
5.  Извлекает текст из HTML, используя пробел в качестве разделителя.
6.  Преобразует HTML-сущности в соответствующие символы с помощью `html.unescape`.
7.  Удаляет лишние пробелы и возвращает очищенный текст.

**Примеры**:

```python
>>> html_input = '<html><head><title>T</title></head><body><p>Hello <b>World</b>!</p><!-- comment --></body></html>'
>>> strip_tags(html_input)
'Hello World !'
>>> strip_tags('Текст с <сущностями> & символами')
'Текст с <сущностями> & символами'
>>> strip_tags(None)
''
```

### `simplify_html`

```python
def simplify_html(
    html_content: str | None,
    config: Optional[Config] = None,
    parser: Optional[str] = None,
) -> str:
    """
    Упрощает HTML-код, фокусируясь на содержимом тега <body> и используя параметры
    из объекта Config (переданного или созданного по умолчанию).

    Args:
        html_content (str | None): Строка с HTML-кодом или None.
        config (Optional[Config]): Объект конфигурации. Если None, используется Config()
                                   с настройками по умолчанию.
        parser (Optional[str]): Парсер для BeautifulSoup ('html.parser', 'lxml', 'html5lib').
                                Если указан, переопределяет `config.parser`.

    Returns:
        str: Упрощенный HTML-код содержимого <body>. Возвращает пустую строку при ошибке,
             None/пустом вводе или если тег <body> не найден.

    Raises:
        Exception: BeautifulSoup может генерировать исключения при серьезных проблемах парсинга,
                   которые логируются.

    Example:
        >>> default_cfg = Config(allowed_tags={'div','span'})
        >>> sample_cls_id = '<body><div class="main" id="cont"><span style="color:red">Text</span></div></body>'
        >>> simplify_html(sample_cls_id, config=default_cfg)
        '<div><span style="color:red">Text</span></div>'

        >>> allow_cls_id_cfg = Config(allowed_tags={'div','span'}, allowed_attributes={'*':{'class','id','style'}})
        >>> simplify_html(sample_cls_id, config=allow_cls_id_cfg)
        '<div class="main" id="cont"><span style="color:red">Text</span></div>'
    """
```

**Назначение**: Функция `simplify_html` упрощает HTML-код, используя заданные параметры конфигурации.

**Параметры**:

-   `html_content` (str | None): Строка с HTML-кодом. Если `None`, функция возвращает пустую строку.
-   `config` (Optional[Config]): Объект конфигурации типа `Config`. Если `None`, используется конфигурация по умолчанию.
-   `parser` (Optional[str]): Парсер для `BeautifulSoup`. Если указан, переопределяет `config.parser`.

**Возвращает**:

-   `str`: Упрощенный HTML-код. Возвращает пустую строку в случае ошибки, `None` или пустом входном значении.

**Вызывает исключения**:

-   `Exception`: Возникает, если `BeautifulSoup` сталкивается с серьезными проблемами при парсинге HTML.

**Как работает функция**:

1.  Функция принимает HTML-контент, объект конфигурации и парсер в качестве аргументов.
2.  Если объект конфигурации не предоставлен, создается объект конфигурации по умолчанию.
3.  Выбор парсера: приоритет у аргумента функции, затем у конфига
4.  Определяет парсер для `BeautifulSoup`, используя аргумент `parser` или значение из конфигурации.
5.  Извлекает содержимое тега `<body>`. Если тег `<body>` не найден, пытается обработать HTML как фрагмент.
6.  Удаляет комментарии, скрипты и стили, если это указано в конфигурации.
7.  Удаляет "незначимые" теги-контейнеры, если включена опция `keep_only_significant`.
8.  Выполняет фильтрацию тегов и атрибутов на основе конфигурации.
9.  Нормализует пробелы, если это указано в конфигурации.
10. Возвращает упрощенный HTML-код.

**Примеры**:

```python
>>> default_cfg = Config(allowed_tags={'div','span'})
>>> sample_cls_id = '<body><div class="main" id="cont"><span style="color:red">Text</span></div></body>'
>>> simplify_html(sample_cls_id, config=default_cfg)
'<div><span style="color:red">Text</span></div>'

>>> allow_cls_id_cfg = Config(allowed_tags={'div','span'}, allowed_attributes={'*':{'class','id','style'}})
>>> simplify_html(sample_cls_id, config=allow_cls_id_cfg)
'<div class="main" id="cont"><span style="color:red">Text</span></div>'
```