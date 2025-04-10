# Модуль для работы с файлами для ChatGPT
=================================================

Модуль предназначен для чтения, обработки и объединения текстовых файлов, а также для очистки содержимого файлов от HTML-тегов и docstring-ов.

## Обзор

Этот модуль содержит функции для работы с файлами, такие как чтение текстовых файлов, удаление HTML-тегов и удаление docstring-ов из содержимого файлов. Он также включает функциональность для рекурсивного удаления содержимого директорий и объединения содержимого нескольких файлов в один или несколько выходных файлов, в зависимости от заданного максимального количества символов.

## Подробнее

Модуль предоставляет инструменты для предобработки текстовых данных, что полезно для подготовки данных для моделей машинного обучения, таких как ChatGPT. Он позволяет очищать данные от нежелательных элементов, таких как HTML-теги и docstring-и, а также объединять данные из нескольких файлов в один файл.

## Функции

### `clean_html`

**Назначение**: Удаляет HTML-теги из содержимого.

**Параметры**:
- `content` (str): HTML-содержимое для очистки.

**Возвращает**:
- `str`: Содержимое без HTML-тегов.

**Как работает функция**:
Функция использует библиотеку `BeautifulSoup` для разбора HTML-содержимого и извлечения текста без HTML-тегов.

**Примеры**:
```python
>>> clean_html('<p>Hello, World!</p>')
'Hello, World!'
```

### `remove_docstrings`

**Назначение**: Удаляет все блоки с тройными кавычками `"""` и `'''` из текста.

**Параметры**:
- `content` (str): Текстовое содержимое, из которого нужно удалить блоки с тройными кавычками.

**Возвращает**:
- `str`: Текст без блоков с тройными кавычками.

**Как работает функция**:
Функция использует регулярные выражения для поиска и удаления многострочных docstring-ов, заключенных в тройные двойные или тройные одинарные кавычки.

**Примеры**:
```python
>>> remove_docstrings('\'\'\'def foo():\n    """This is a docstring"""\n    pass\'\'\')
'def foo():\n    pass'
```

### `delete_directory_contents`

**Назначение**: Рекурсивно удаляет все содержимое указанной директории.

**Параметры**:
- `directory` (Path): Путь к директории, содержимое которой нужно удалить.

**Возвращает**:
- `None`

**Как работает функция**:
Функция рекурсивно перебирает все элементы в указанной директории. Если элемент является директорией, функция вызывает себя для удаления содержимого этой директории. Если элемент является файлом, функция пытается удалить его. После удаления содержимого директории, функция пытается удалить саму директорию. В случае возникновения ошибок при удалении файлов или директорий, функция логирует ошибки с использованием модуля `logger` из `src.logger`.

**Примеры**:
```python
>>> delete_directory_contents(Path('../tmp/chat_gpt/aliexpress'))
```

### `read_text_files`

**Назначение**: Читает все указанные Python файлы в каталоге и сохраняет объединенный текст в несколько файлов, если размер содержания превышает `max_chars` символов.

**Параметры**:
- `directory` (str): Каталог для поиска файлов.
- `output_file` (str): Базовое имя файла для сохранения объединенного текста.
- `remove_docs` (bool): Если `True`, удаляет блоки с тройными кавычками из текста. По умолчанию `False`.
- `max_chars` (int): Максимальное количество символов для каждого файла. По умолчанию 2000.

**Возвращает**:
- `None`

**Как работает функция**:
Функция выполняет следующие шаги:
1. Определяет пути для выходных файлов и создает директорию для них, если она не существует.
2. Инициализирует счетчик символов и создает первый выходной файл.
3. Рекурсивно обходит все файлы в указанной директории.
4. Для каждого Python файла:
   - Читает содержимое файла.
   - Если файл пустой, пропускает его.
   - Если `remove_docs` равен `True`, удаляет docstring-и из содержимого файла.
   - Проверяет, нужно ли создавать новый файл, если текущий размер содержимого превышает `max_chars`.
   - Записывает содержимое файла в текущий выходной файл.
5. Закрывает последний выходной файл.
6. В случае возникновения ошибок при обработке файлов, функция логирует ошибки с использованием модуля `logger` из `src.logger`.

**Примеры**:
```python
>>> read_text_files('src', 'output.txt', remove_docs=True)