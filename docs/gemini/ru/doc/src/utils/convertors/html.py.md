# Модуль для конвертации HTML

## Обзор

Модуль `src.utils.convertors.html` предоставляет набор функций для конвертации HTML-кода в другие форматы, такие как escape-последовательности, словари, объекты `SimpleNamespace` и PDF-файлы.

## Подробей

Модуль предназначен для обработки HTML-кода в различных сценариях, таких как:

- Преобразование HTML-кода в escape-последовательности для безопасного хранения или передачи.
- Разбор HTML-кода в структуру данных для последующей обработки.
- Создание PDF-файлов из HTML-контента.

## Классы

### `class HTMLToDictParser`

**Описание**: Класс, реализующий парсер HTML-кода для преобразования в словарь.

**Наследует**: `html.parser.HTMLParser`

**Атрибуты**:

- `result (dict)`: Словарь, в котором ключи - теги HTML, а значения - их содержимое.
- `current_tag (str)`: Текущий обрабатываемый тег.

**Методы**:

- `handle_starttag(tag: str, attrs: list)`: Обрабатывает начало HTML-тега.
- `handle_endtag(tag: str)`: Обрабатывает конец HTML-тега.
- `handle_data(data: str)`: Обрабатывает текстовое содержимое HTML-тега.

## Функции

### `html2escape`

**Назначение**: Преобразует HTML-код в escape-последовательности.

**Параметры**:

- `input_str (str)`: HTML-код для преобразования.

**Возвращает**:

- `str`: HTML-код, преобразованный в escape-последовательности.

**Примеры**:

```python
>>> html = "<p>Hello, world!</p>"
>>> result = html2escape(html)
>>> print(result)
&lt;p&gt;Hello, world!&lt;/p&gt;
```

### `escape2html`

**Назначение**: Преобразует escape-последовательности в HTML-код.

**Параметры**:

- `input_str (str)`: Строка с escape-последовательностями.

**Возвращает**:

- `str`: Escape-последовательности, преобразованные обратно в HTML-код.

**Примеры**:

```python
>>> escaped = "&lt;p&gt;Hello, world!&lt;/p&gt;"
>>> result = escape2html(escaped)
>>> print(result)
<p>Hello, world!</p>
```

### `html2dict`

**Назначение**: Преобразует HTML-код в словарь, где ключи - теги HTML, а значения - их содержимое.

**Параметры**:

- `html_str (str)`: HTML-код для преобразования.

**Возвращает**:

- `dict`: Словарь с тегами HTML в качестве ключей и их содержимым в качестве значений.

**Примеры**:

```python
>>> html = "<p>Hello</p><a href='link'>World</a>"
>>> result = html2dict(html)
>>> print(result)
{'p': 'Hello', 'a': 'World'}
```

### `html2ns`

**Назначение**: Преобразует HTML-код в объект `SimpleNamespace`, где теги HTML - это атрибуты, а их содержимое - значения.

**Параметры**:

- `html_str (str)`: HTML-код для преобразования.

**Возвращает**:

- `SimpleNamespace`: Объект `SimpleNamespace` с тегами HTML в качестве атрибутов и их содержимым в качестве значений.

**Примеры**:

```python
>>> html = "<p>Hello</p><a href='link'>World</a>"
>>> result = html2ns(html)
>>> print(result.p)
Hello
>>> print(result.a)
World
```

### `html2pdf`

**Назначение**: Преобразует HTML-контент в PDF-файл с помощью библиотеки `WeasyPrint`.

**Параметры**:

- `html_str (str)`: HTML-контент в виде строки.
- `pdf_file (str | Path)`: Путь к выходному PDF-файлу.

**Возвращает**:

- `bool | None`: `True`, если генерация PDF прошла успешно; `None` в противном случае.

**Примеры**:

```python
>>> html = "<html><body><h1>Hello, world!</h1></body></html>"
>>> pdf_file = "output.pdf"
>>> result = html2pdf(html, pdf_file)
>>> print(result)
True
```

### `html_to_docx`

**Назначение**: Преобразует HTML-файл в документ Word (.docx) с помощью LibreOffice.

**Параметры**:

- `html_file (str)`: Путь к входному HTML-файлу.
- `output_docx (Path | str)`: Путь к выходному DOCX-файлу.

**Возвращает**:

- `bool`: `True`, если преобразование прошло успешно; `False` в противном случае.

**Примеры**:

```python
>>> html_file = "input.html"
>>> output_docx = "output.docx"
>>> result = html_to_docx(html_file, output_docx)
>>> print(result)
True
```

## Примеры

```python
# Преобразование HTML в escape-последовательности
html = "<p>Hello, world!</p>"
escaped_html = html2escape(html)
print(escaped_html)  # Вывод: &lt;p&gt;Hello, world!&lt;/p&gt;

# Преобразование escape-последовательностей в HTML
escaped_html = "&lt;p&gt;Hello, world!&lt;/p&gt;"
html = escape2html(escaped_html)
print(html)  # Вывод: <p>Hello, world!</p>

# Преобразование HTML в словарь
html = "<p>Hello</p><a href='link'>World</a>"
html_dict = html2dict(html)
print(html_dict)  # Вывод: {'p': 'Hello', 'a': 'World'}

# Преобразование HTML в объект SimpleNamespace
html = "<p>Hello</p><a href='link'>World</a>"
html_ns = html2ns(html)
print(html_ns.p)  # Вывод: Hello
print(html_ns.a)  # Вывод: World

# Преобразование HTML в PDF
html = "<html><body><h1>Hello, world!</h1></body></html>"
pdf_file = "output.pdf"
result = html2pdf(html, pdf_file)
print(result)  # Вывод: True

# Преобразование HTML в DOCX
html_file = "input.html"
output_docx = "output.docx"
result = html_to_docx(html_file, output_docx)
print(result)  # Вывод: True
```