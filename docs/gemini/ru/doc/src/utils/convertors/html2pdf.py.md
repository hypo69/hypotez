# Модуль `html2pdf`

## Обзор

Модуль `html2pdf` предоставляет утилиты для конвертации HTML в различные форматы, включая escape-последовательности, словари, объекты SimpleNamespace и PDF. Модуль содержит функции для преобразования HTML-строк в различные представления, а также для создания PDF-файлов из HTML-контента.

## Подробней

Модуль предназначен для обработки и преобразования HTML-данных. Он включает функции для экранирования и обратного преобразования HTML-тегов, преобразования HTML в словари и объекты SimpleNamespace, а также для создания PDF-файлов из HTML-контента.

## Функции

### `html2escape`

```python
def html2escape(input_str: str) -> str:
    """
    Convert HTML to escape sequences.

    Args:
        input_str (str): The HTML code.

    Returns:
        str: HTML converted into escape sequences.

    Example:
        >>> html = "<p>Hello, world!</p>"
        >>> result = html2escape(html)
        >>> print(result)
        &lt;p&gt;Hello, world!&lt;/p&gt;
    """
```

**Назначение**: Преобразует HTML-код в escape-последовательности.

**Параметры**:
- `input_str` (str): HTML-код для преобразования.

**Возвращает**:
- `str`: HTML, преобразованный в escape-последовательности.

**Как работает функция**:
Функция `html2escape` использует метод `StringFormatter.escape_html_tags` для преобразования HTML-кода в escape-последовательности. Это необходимо для безопасного отображения HTML-кода, предотвращая его интерпретацию как HTML-теги.

**Примеры**:
```python
html = "<p>Hello, world!</p>"
result = html2escape(html)
print(result)  # Вывод: &lt;p&gt;Hello, world!&lt;/p&gt;
```

### `escape2html`

```python
def escape2html(input_str: str) -> str:
    """
    Convert escape sequences to HTML.

    Args:
        input_str (str): The string with escape sequences.

    Returns:
        str: The escape sequences converted back into HTML.

    Example:
        >>> escaped = "&lt;p&gt;Hello, world!&lt;/p&gt;"
        >>> result = escape2html(escaped)
        >>> print(result)
        <p>Hello, world!</p>
    """
```

**Назначение**: Преобразует escape-последовательности обратно в HTML-код.

**Параметры**:
- `input_str` (str): Строка с escape-последовательностями.

**Возвращает**:
- `str`: HTML-код, полученный из escape-последовательностей.

**Как работает функция**:
Функция `escape2html` использует метод `StringFormatter.unescape_html_tags` для преобразования escape-последовательностей обратно в HTML-код. Это позволяет отображать HTML-код в браузере или других HTML-рендерах.

**Примеры**:
```python
escaped = "&lt;p&gt;Hello, world!&lt;/p&gt;"
result = escape2html(escaped)
print(result)  # Вывод: <p>Hello, world!</p>
```

### `html2dict`

```python
def html2dict(html_str: str) -> Dict[str, str]:
    """
    Convert HTML to a dictionary where tags are keys and content are values.

    Args:
        html_str (str): The HTML string to convert.

    Returns:
        dict: A dictionary with HTML tags as keys and their content as values.

    Example:
        >>> html = "<p>Hello</p><a href='link'>World</a>"
        >>> result = html2dict(html)
        >>> print(result)
        {'p': 'Hello', 'a': 'World'}
    """
    class HTMLToDictParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.result = {}
            self.current_tag = None

        def handle_starttag(self, tag, attrs):
            self.current_tag = tag

        def handle_endtag(self, tag):
            self.current_tag = None

        def handle_data(self, data):
            if self.current_tag:
                self.result[self.current_tag] = data.strip()

    parser = HTMLToDictParser()
    parser.feed(html_str)
    return parser.result
```

**Назначение**: Преобразует HTML-код в словарь, где ключами являются теги, а значениями - содержимое этих тегов.

**Параметры**:
- `html_str` (str): HTML-код для преобразования.

**Возвращает**:
- `dict`: Словарь, где ключи - HTML-теги, а значения - их содержимое.

**Как работает функция**:
Функция `html2dict` использует класс `HTMLToDictParser`, который наследуется от `HTMLParser`. Этот класс переопределяет методы `handle_starttag`, `handle_endtag` и `handle_data` для извлечения тегов и их содержимого.
1. **Инициализация парсера**: Создается экземпляр класса `HTMLToDictParser`.
2. **Обработка HTML**: Метод `feed` передает HTML-строку парсеру.
3. **Извлечение данных**:
   - `handle_starttag`: Запоминает текущий открытый тег.
   - `handle_data`: Извлекает данные между открывающим и закрывающим тегами и сохраняет их в словаре `result`.
4. **Возврат результата**: Возвращает словарь, содержащий теги и их содержимое.

**Примеры**:
```python
html = "<p>Hello</p><a href='link'>World</a>"
result = html2dict(html)
print(result)  # Вывод: {'p': 'Hello', 'a': 'World'}
```

**Внутренние функции**:

### `HTMLToDictParser`

```python
class HTMLToDictParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = {}
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag

    def handle_endtag(self, tag):
        self.current_tag = None

    def handle_data(self, data):
        if self.current_tag:
            self.result[self.current_tag] = data.strip()
```

**Описание**:
Класс `HTMLToDictParser` наследуется от `HTMLParser` и используется для парсинга HTML-кода и извлечения тегов и их содержимого в словарь.

**Наследует**:
- `HTMLParser`

**Атрибуты**:
- `result` (dict): Словарь для хранения результатов парсинга.
- `current_tag` (str): Текущий обрабатываемый тег.

**Методы**:

- `handle_starttag(self, tag, attrs)`:
    - **Назначение**: Обрабатывает открывающий тег HTML.
    - **Параметры**:
        - `tag` (str): Имя тега.
        - `attrs` (list): Список атрибутов тега.
    - **Как работает**: Устанавливает `current_tag` в текущий тег.

- `handle_endtag(self, tag)`:
    - **Назначение**: Обрабатывает закрывающий тег HTML.
    - **Параметры**:
        - `tag` (str): Имя тега.
    - **Как работает**: Сбрасывает `current_tag` в `None`.

- `handle_data(self, data)`:
    - **Назначение**: Обрабатывает текстовые данные между тегами.
    - **Параметры**:
        - `data` (str): Текстовые данные.
    - **Как работает**: Если `current_tag` установлен, добавляет данные в словарь `result` с ключом `current_tag`.

### `html2ns`

```python
def html2ns(html_str: str) -> SimpleNamespace:
    """
    Convert HTML to a SimpleNamespace object where tags are attributes and content are values.

    Args:
        html_str (str): The HTML string to convert.

    Returns:
        SimpleNamespace: A SimpleNamespace object with HTML tags as attributes and their content as values.

    Example:
        >>> html = "<p>Hello</p><a href='link'>World</a>"
        >>> result = html2ns(html)
        >>> print(result.p)
        Hello
        >>> print(result.a)
        World
    """
    html_dict = html2dict(html_str)
    return SimpleNamespace(**html_dict)
```

**Назначение**: Преобразует HTML-код в объект `SimpleNamespace`, где теги становятся атрибутами объекта, а их содержимое - значениями атрибутов.

**Параметры**:
- `html_str` (str): HTML-код для преобразования.

**Возвращает**:
- `SimpleNamespace`: Объект `SimpleNamespace` с HTML-тегами в качестве атрибутов и их содержимым в качестве значений.

**Как работает функция**:
Функция `html2ns` использует функцию `html2dict` для преобразования HTML-кода в словарь, а затем создает объект `SimpleNamespace` из этого словаря. Это позволяет обращаться к содержимому HTML-тегов как к атрибутам объекта.

**Примеры**:
```python
html = "<p>Hello</p><a href='link'>World</a>"
result = html2ns(html)
print(result.p)  # Вывод: Hello
print(result.a)  # Вывод: World
```

### `html2pdf`

```python
def html2pdf(html_str: str, pdf_file: str | Path) -> bool | None:
    """Converts HTML content to a PDF file using WeasyPrint."""
    try:
        HTML(string=html_str).write_pdf(pdf_file)
        return True
    except Exception as e:
        print(f"Error during PDF generation: {e}")
        return
```

**Назначение**: Преобразует HTML-код в PDF-файл.

**Параметры**:
- `html_str` (str): HTML-код для преобразования.
- `pdf_file` (str | Path): Путь к выходному PDF-файлу.

**Возвращает**:
- `bool | None`: `True`, если PDF-файл успешно создан, `None` в случае ошибки.

**Как работает функция**:
Функция `html2pdf` использует библиотеку `WeasyPrint` для преобразования HTML-кода в PDF-файл.
1. **Создание PDF**: Метод `HTML(string=html_str).write_pdf(pdf_file)` создает PDF-файл из HTML-кода и сохраняет его по указанному пути.
2. **Обработка ошибок**: Если в процессе создания PDF-файла возникает исключение, функция логирует ошибку и возвращает `None`.

**Примеры**:
```python
html = "<p>Hello, world!</p>"
pdf_file = "example.pdf"
result = html2pdf(html, pdf_file)
if result:
    print("PDF file created successfully.")
else:
    print("Failed to create PDF file.")
```
ASCII flowchart:

```
A: HTML content и путь к PDF
|
B: Используем WeasyPrint для конвертации HTML в PDF
|
C: Проверяем успешность операции
|
D: Возвращаем True, если успешно, иначе None
```

## Заключение

Модуль `html2pdf` предоставляет набор инструментов для преобразования HTML в различные форматы, что может быть полезно для различных задач, таких как обработка веб-страниц, создание отчетов и документов.