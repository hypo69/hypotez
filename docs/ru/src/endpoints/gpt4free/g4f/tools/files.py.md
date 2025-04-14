# Модуль для работы с файлами

## Обзор

Модуль `files.py` предоставляет инструменты для обработки различных типов файлов, включая текстовые файлы, PDF, DOCX, ODT, EPUB, XLSX, HTML и ZIP архивы. Он также включает функциональность для скачивания файлов по URL-адресам, извлечения текста из них и кэширования результатов. Модуль поддерживает очистку и разделение текста на фрагменты с использованием библиотеки `spaCy`.

## Подробнее

Этот модуль играет важную роль в проекте `hypotez`, обеспечивая возможность извлечения и обработки текстовой информации из файлов разных форматов. Он позволяет скачивать файлы, кэшировать содержимое для повторного использования, а также разделять текст на части для дальнейшей обработки, например, с использованием моделей машинного обучения.

## Функции

### `secure_filename`

```python
def secure_filename(filename: str) -> str:
    """
    Очищает имя файла, удаляя небезопасные символы.

    Args:
        filename (str): Имя файла для очистки.

    Returns:
        str: Очищенное имя файла.
    """
```

**Назначение**:
Функция `secure_filename` принимает строку с именем файла и возвращает очищенную версию имени, в которой удалены все символы, кроме букв, цифр, основных знаков препинания, а также символов Unicode.

**Как работает функция**:

1.  Если `filename` равно `None`, функция возвращает `None`.
2.  Заменяет все символы, кроме букв, цифр, символов `.,_-+` и Unicode символов, на символ `_`.
3.  Усекает имя файла до 100 символов и удаляет символы `.,_-+` в начале и конце строки.

**Примеры**:

```python
secure_filename("example file.txt")  # Результат: "example_file.txt"
secure_filename("file@with#unsafe$chars%.txt")  # Результат: "file_with_unsafe_chars_.txt"
secure_filename(None)  # Результат: None
```

### `supports_filename`

```python
def supports_filename(filename: str):
    """
    Проверяет, поддерживается ли указанный формат файла.

    Args:
        filename (str): Имя файла для проверки.

    Returns:
        bool: `True`, если формат файла поддерживается, `False` в противном случае.

    Raises:
        MissingRequirementsError: Если отсутствуют необходимые библиотеки для обработки указанного формата файла.
    """
```

**Назначение**:
Функция `supports_filename` определяет, поддерживается ли указанный формат файла для обработки, проверяя наличие необходимых библиотек.

**Как работает функция**:

1.  Проверяет расширение файла и наличие соответствующих библиотек (`PyPDF2`, `pdfplumber`, `pdfminer`, `docx`, `docx2txt`, `odfpy`, `ebooklib`, `openpyxl`, `beautifulsoup4`).
2.  Если для обработки файла требуется определенная библиотека, но она не установлена, функция вызывает исключение `MissingRequirementsError`.

**Примеры**:

```python
supports_filename("example.pdf")  # Вернет True, если установлена хотя бы одна из библиотек PyPDF2, pdfplumber или pdfminer.
supports_filename("example.docx")  # Вернет True, если установлена хотя бы одна из библиотек docx или docx2txt.
```

### `get_bucket_dir`

```python
def get_bucket_dir(*parts):
    """
    Формирует путь к каталогу bucket.

    Args:
        *parts: Переменное количество частей пути для объединения.

    Returns:
        str: Полный путь к каталогу bucket.
    """
```

**Назначение**:
Функция `get_bucket_dir` создает путь к каталогу "buckets", объединяя переданные части пути и очищая их с помощью `secure_filename`.

**Как работает функция**:

1.  Объединяет путь к каталогу cookies с подкаталогом "buckets".
2.  Очищает каждую часть пути с использованием функции `secure_filename`.
3.  Объединяет все части пути в один полный путь.

**Примеры**:

```python
get_bucket_dir("bucket1", "file name.txt")  # Пример возвращаемого значения: "/path/to/cookies/buckets/bucket1/file_name.txt"
```

### `get_buckets`

```python
def get_buckets():
    """
    Получает список директорий bucket.

    Returns:
        list: Список имен директорий bucket или None в случае ошибки.
    """
```

**Назначение**:
Функция `get_buckets` возвращает список всех директорий внутри каталога "buckets".

**Как работает функция**:

1.  Формирует путь к каталогу "buckets".
2.  Пытается получить список всех директорий в каталоге "buckets".
3.  Возвращает список директорий или `None`, если произошла ошибка.

**Примеры**:

```python
get_buckets()  # Пример возвращаемого значения: ["bucket1", "bucket2", "bucket3"]
```

### `spacy_refine_chunks`

```python
def spacy_refine_chunks(source_iterator):
    """
    Обрабатывает фрагменты текста с использованием spaCy для улучшения качества.

    Args:
        source_iterator (Iterator[str]): Итератор, предоставляющий фрагменты текста.

    Yields:
        str: Улучшенные фрагменты текста.

    Raises:
        MissingRequirementsError: Если библиотека spaCy не установлена.
    """
```

**Назначение**:
Функция `spacy_refine_chunks` использует библиотеку `spaCy` для обработки и улучшения фрагментов текста, предоставляемых итератором.

**Как работает функция**:

1.  Проверяет, установлена ли библиотека `spaCy`. Если нет, вызывает исключение `MissingRequirementsError`.
2.  Загружает модель `en_core_web_sm` из `spaCy`.
3.  Для каждой страницы текста, предоставляемой `source_iterator`:
    *   Обрабатывает текст с помощью `nlp(page)`.
    *   Извлекает предложения из документа.
    *   Сортирует предложения по длине текста в обратном порядке и выбирает два самых длинных предложения.
    *   Возвращает текст каждого из выбранных предложений.

**Примеры**:

Предположим, `source_iterator` предоставляет текст "This is a sentence. This is another sentence. And this is a third one.". Тогда `spacy_refine_chunks` вернет два самых длинных предложения из этого текста.

### `get_filenames`

```python
def get_filenames(bucket_dir: Path):
    """
    Получает список имен файлов из файла FILE_LIST в указанной директории bucket.

    Args:
        bucket_dir (Path): Путь к директории bucket.

    Returns:
        list: Список имен файлов.
    """
```

**Назначение**:
Функция `get_filenames` читает список имен файлов из файла `FILE_LIST` в указанной директории bucket.

**Как работает функция**:

1.  Формирует путь к файлу `FILE_LIST` в директории `bucket_dir`.
2.  Если файл существует, открывает его и читает построчно, удаляя пробельные символы в начале и конце каждой строки.
3.  Возвращает список имен файлов.

**Примеры**:

```python
bucket_dir = Path("/path/to/bucket")
# Предположим, что файл /path/to/bucket/files.txt содержит строки "file1.txt\nfile2.txt\n"
get_filenames(bucket_dir)  # Результат: ["file1.txt", "file2.txt"]
```

### `stream_read_files`

```python
def stream_read_files(bucket_dir: Path, filenames: list, delete_files: bool = False) -> Iterator[str]:
    """
    Считывает содержимое файлов из указанной директории bucket и возвращает его в виде потока.

    Args:
        bucket_dir (Path): Путь к директории bucket.
        filenames (list): Список имен файлов для чтения.
        delete_files (bool): Если `True`, файлы будут удалены после прочтения.

    Yields:
        str: Содержимое файлов.
    """
```

**Назначение**:
Функция `stream_read_files` считывает содержимое файлов из указанной директории и возвращает его в виде потока (итератора). Функция поддерживает чтение различных типов файлов, включая ZIP архивы, PDF, DOCX, ODT, EPUB, XLSX, HTML и текстовые файлы.

**Как работает функция**:

1.  Итерируется по списку имен файлов.
2.  Для каждого файла проверяет его существование и размер. Если файл не существует или его размер равен нулю, переходит к следующему файлу.
3.  Если файл является ZIP архивом, распаковывает его в директорию `bucket_dir` и рекурсивно вызывает `stream_read_files` для распакованных файлов. После обработки ZIP архива, удаляет распакованные файлы, если `delete_files` равно `True`.
4.  Для каждого файла, отличного от ZIP архива, считывает его содержимое в зависимости от типа файла (PDF, DOCX, ODT, EPUB, XLSX, HTML или текстовый файл) и возвращает его в виде потока.
5.  Поддерживаемые библиотеки для чтения файлов: `PyPDF2`, `pdfplumber`, `pdfminer`, `docx`, `docx2txt`, `odfpy`, `ebooklib`, `pandas`, `BeautifulSoup`.

**Примеры**:

```python
bucket_dir = Path("/path/to/bucket")
filenames = ["file1.txt", "file2.pdf", "archive.zip"]
# Предположим, что file1.txt содержит "Hello, world!\n", file2.pdf содержит текст из PDF файла, archive.zip содержит file3.txt с текстом "Inside the archive.\n"
for chunk in stream_read_files(bucket_dir, filenames):
    print(chunk)
# Вывод:
# ```file1.txt\n
# Hello, world!\n
# \n```\n\n
# (содержимое file2.pdf)
# \n```\n\n
# ```archive.zip\n
# Inside the archive.\n
# \n```\n\n
```

### `cache_stream`

```python
def cache_stream(stream: Iterator[str], bucket_dir: Path) -> Iterator[str]:
    """
    Кэширует содержимое потока в файл и возвращает его в виде потока.

    Args:
        stream (Iterator[str]): Итератор, предоставляющий фрагменты текста.
        bucket_dir (Path): Путь к директории bucket.

    Yields:
        str: Фрагменты текста из потока.
    """
```

**Назначение**:
Функция `cache_stream` принимает поток данных (итератор строк) и директорию, кэширует данные потока в файл и возвращает этот поток. Если кэш уже существует, функция возвращает данные из кэша.

**Как работает функция**:

1.  Определяет пути к файлу кэша и временному файлу.
2.  Если файл кэша существует, функция читает данные из кэша и возвращает их.
3.  Если файл кэша не существует, функция открывает временный файл для записи.
4.  Функция итерируется по входящему потоку данных, записывает каждый фрагмент в временный файл и возвращает этот фрагмент.
5.  После завершения потока, временный файл переименовывается в файл кэша.

**Примеры**:

```python
bucket_dir = Path("/path/to/bucket")
data_stream = iter(["chunk1", "chunk2", "chunk3"])
cached_stream = cache_stream(data_stream, bucket_dir)
for chunk in cached_stream:
    print(chunk)
# Вывод:
# chunk1
# chunk2
# chunk3
```

### `is_complete`

```python
def is_complete(data: str):
    """
    Проверяет, является ли переданный блок данных полным.

    Args:
        data (str): Блок данных для проверки.

    Returns:
        bool: `True`, если блок данных является полным, `False` в противном случае.
    """
```

**Назначение**:
Функция `is_complete` проверяет, является ли переданный блок данных полным, определяя, заканчивается ли он определенной последовательностью символов и содержит ли четное количество разделителей.

**Как работает функция**:

1.  Проверяет, заканчивается ли строка `data` на `\n\`\`\`\n\n`.
2.  Проверяет, является ли количество `\`\`\`` в строке `data` четным.
3.  Возвращает `True`, если оба условия выполняются, и `False` в противном случае.

**Примеры**:

```python
is_complete("some data\n```\n\n")  # Результат: True
is_complete("some data\n```\n")  # Результат: False
is_complete("some ``` data\n```\n\n")  # Результат: True
is_complete("some ``` data\n```\n")  # Результат: False
```

### `read_path_chunked`

```python
def read_path_chunked(path: Path):
    """
    Читает файл по частям (chunks).

    Args:
        path (Path): Путь к файлу.

    Yields:
        str: Часть файла.
    """
```

**Назначение**:
Функция `read_path_chunked` читает файл по частям (chunks) заданного размера, разделяя файл на строки и объединяя их в чанки до достижения определенного размера.

**Как работает функция**:

1.  Открывает файл для чтения в кодировке UTF-8.
2.  Инициализирует переменные: `current_chunk_size` для отслеживания размера текущего чанка в байтах и `buffer` для хранения содержимого текущего чанка.
3.  Читает файл построчно.
4.  Для каждой строки:
    *   Добавляет длину строки в байтах к `current_chunk_size`.
    *   Добавляет строку в `buffer`.
    *   Если `current_chunk_size` превышает 4096 байт, проверяет, является ли `buffer` полным с помощью функции `is_complete`.
    *   Если `buffer` полный или `current_chunk_size` превышает 8192 байта, возвращает `buffer` и очищает `buffer` и `current_chunk_size`.
5.  Если после завершения чтения файла в `buffer` остались данные, возвращает `buffer`.

**Примеры**:

Предположим, у нас есть файл `example.txt` с содержимым:

```
This is the first line.
This is the second line.
This is the third line.
```

```python
file_path = Path("example.txt")
for chunk in read_path_chunked(file_path):
    print(chunk)
```

### `read_bucket`

```python
def read_bucket(bucket_dir: Path):
    """
    Читает содержимое файлов кэша из указанной директории bucket.

    Args:
        bucket_dir (Path): Путь к директории bucket.

    Yields:
        str: Содержимое файлов кэша.
    """
```

**Назначение**:
Функция `read_bucket` читает содержимое файлов кэша из указанной директории bucket. Функция ищет файлы кэша, созданные с использованием библиотеки `spaCy` и обычные файлы кэша, и возвращает их содержимое в виде потока.

**Как работает функция**:

1.  Формирует пути к файлам кэша (`PLAIN_CACHE` и файлам `spacy_*.cache`).
2.  Если существует файл `PLAIN_CACHE` и отсутствует файл `spacy_0001.cache`, функция читает содержимое файла `PLAIN_CACHE` и возвращает его.
3.  Итерируется по файлам `spacy_*.cache` и `plain_*.cache` с индексами от 1 до 999.
4.  Для каждого файла проверяет его существование. Если файл существует, функция читает его содержимое и возвращает его.
5.  Если файл не существует, функция прерывает итерацию.

**Примеры**:

```python
bucket_dir = Path("/path/to/bucket")
# Предположим, что в директории /path/to/bucket существуют файлы spacy_0001.cache и plain_0002.cache.
for chunk in read_bucket(bucket_dir):
    print(chunk)
# Вывод:
# (содержимое файла spacy_0001.cache)
# (содержимое файла plain_0002.cache)
```

### `stream_read_parts_and_refine`

```python
def stream_read_parts_and_refine(bucket_dir: Path, delete_files: bool = False) -> Iterator[str]:
    """
    Считывает части файлов и улучшает их с использованием spaCy.

    Args:
        bucket_dir (Path): Путь к директории bucket.
        delete_files (bool): Если `True`, части файлов будут удалены после обработки.

    Yields:
        str: Улучшенные части файлов.
    """
```

**Назначение**:
Функция `stream_read_parts_and_refine` считывает части файлов из указанной директории bucket, улучшает их с использованием библиотеки `spaCy` и возвращает улучшенные части файлов в виде потока.

**Как работает функция**:

1.  Формирует пути к файлам кэша (`PLAIN_CACHE`, `spacy_*.cache` и `plain_*.cache`).
2.  Если существует файл `PLAIN_CACHE` и отсутствуют файлы `spacy_0001.cache` и `plain_0001.cache`, функция разделяет файл `PLAIN_CACHE` на части с помощью функции `split_file_by_size_and_newline`.
3.  Итерируется по файлам `plain_*.cache` с индексами от 1 до 999.
4.  Для каждого файла формирует пути к временному файлу и файлу кэша (`spacy_*.cache`).
5.  Если существует файл кэша (`spacy_*.cache`), функция читает его содержимое и возвращает его.
6.  Если файл кэша не существует и существует файл `plain_*.cache`, функция открывает временный файл для записи и обрабатывает файл `plain_*.cache` с помощью функции `spacy_refine_chunks`. Результат записывается во временный файл и возвращается.
7.  После обработки файл `plain_*.cache` удаляется, если `delete_files` равно `True`.

**Примеры**:

```python
bucket_dir = Path("/path/to/bucket")
# Предположим, что в директории /path/to/bucket существуют файлы plain_0001.cache, plain_0002.cache и plain_0003.cache.
for chunk in stream_read_parts_and_refine(bucket_dir, delete_files=True):
    print(chunk)
# Вывод:
# (содержимое файла plain_0001.cache, обработанное с помощью spaCy)
# (содержимое файла plain_0002.cache, обработанное с помощью spaCy)
# (содержимое файла plain_0003.cache, обработанное с помощью spaCy)
```

### `split_file_by_size_and_newline`

```python
def split_file_by_size_and_newline(input_filename, output_dir, chunk_size_bytes=1024*1024): # 1MB
    """Splits a file into chunks of approximately chunk_size_bytes, splitting only at newline characters.

    Args:
        input_filename: Path to the input file.
        output_prefix: Prefix for the output files (e.g., 'output_part_').
        chunk_size_bytes: Desired size of each chunk in bytes.
    """
```

**Назначение**:
Функция `split_file_by_size_and_newline` разделяет входной файл на части (chunks) заданного размера, разделяя файл только по символам новой строки.

**Как работает функция**:

1.  Определяет префикс для выходных файлов на основе имени входного файла и выходной директории.
2.  Открывает входной файл для чтения в кодировке UTF-8.
3.  Инициализирует переменные: `chunk_num` для отслеживания номера текущего чанка, `current_chunk` для хранения содержимого текущего чанка и `current_chunk_size` для отслеживания размера текущего чанка в байтах.
4.  Читает файл построчно.
5.  Для каждой строки:
    *   Добавляет строку в `current_chunk`.
    *   Добавляет длину строки в байтах к `current_chunk_size`.
    *   Если `current_chunk_size` превышает `chunk_size_bytes`, проверяет, является ли `current_chunk` полным с помощью функции `is_complete`.
    *   Если `current_chunk` полный или `current_chunk_size` превышает `chunk_size_bytes * 2`, создает новый выходной файл с именем, содержащим префикс и номер чанка, записывает `current_chunk` в файл и очищает `current_chunk` и `current_chunk_size`.
6.  После завершения чтения файла, создает выходной файл для последнего чанка (если `current_chunk` не пустой) и записывает `current_chunk` в файл.

**Примеры**:

Предположим, у нас есть файл `example.txt` с содержимым:

```
This is the first line.
This is the second line.
This is the third line.
```

```python
input_filename = "example.txt"
output_dir = "/path/to/output"
split_file_by_size_and_newline(input_filename, output_dir, chunk_size_bytes=50)
```

### `get_filename`

```python
async def get_filename(response: ClientResponse) -> str:
    """
    Пытается извлечь имя файла из ответа aiohttp.

    Args:
        response: Объект ClientResponse aiohttp.

    Returns:
        Имя файла в виде строки или None, если не удалось определить.
    """
```

**Назначение**:
Функция `get_filename` пытается извлечь имя файла из HTTP-ответа, используя заголовок `Content-Disposition` или URL.

**Как работает функция**:

1.  Извлекает значение заголовка `Content-Disposition` из ответа. Если заголовок присутствует, пытается извлечь имя файла из него. Если имя файла найдено, очищает его с помощью функции `secure_filename` и возвращает.
2.  Если заголовок `Content-Disposition` отсутствует или не содержит имени файла, функция извлекает значение заголовка `Content-Type` и URL из ответа.
3.  Если `Content-Type` и URL присутствуют, функция вызывает функцию `get_file_extension` для определения расширения файла.
4.  Если расширение файла определено, функция формирует имя файла на основе домена, пути и хеша URL.
5.  Если не удалось определить имя файла, функция возвращает `None`.

**Примеры**:

```python
# Пример 1: Извлечение имени файла из заголовка Content-Disposition
response = MockClientResponse(headers={"Content-Disposition": "attachment; filename=example.pdf"})
filename = await get_filename(response)  # filename будет "example.pdf"

# Пример 2: Формирование имени файла из URL и Content-Type
response = MockClientResponse(
    headers={"Content-Type": "application/pdf"},
    url="https://example.com/files/document.pdf"
)
filename = await get_filename(response)  # filename будет "example.com+files_document+<hash>.pdf"
```

### `get_file_extension`

```python
async def get_file_extension(response: ClientResponse):
    """
    Пытается определить расширение файла из ответа aiohttp.

    Args:
        response: Объект ClientResponse aiohttp.

    Returns:
        Расширение файла (например, ".html", ".json", ".pdf", ".zip", ".md", ".txt") в виде строки
        или None, если не удалось определить.
    """
```

**Назначение**:
Функция `get_file_extension` пытается определить расширение файла из HTTP-ответа, используя заголовок `Content-Type` или URL.

**Как работает функция**:

1.  Извлекает значение заголовка `Content-Type` из ответа. Если заголовок присутствует, проверяет, содержит ли он информацию о типе файла (HTML, JSON, PDF, ZIP, text/plain, markdown). Если тип файла определен, возвращает соответствующее расширение.
2.  Если заголовок `Content-Type` отсутствует или не содержит информации о типе файла, функция извлекает URL из ответа и пытается получить расширение файла из URL.
3.  Если не удалось определить расширение файла, функция возвращает `None`.

**Примеры**:

```python
# Пример 1: Определение расширения из Content-Type
response = MockClientResponse(headers={"Content-Type": "application/pdf"})
extension = await get_file_extension(response)  # extension будет ".pdf"

# Пример 2: Определение расширения из URL
response = MockClientResponse(url="https://example.com/files/document.pdf")
extension = await get_file_extension(response)  # extension будет ".pdf"
```

### `read_links`

```python
def read_links(html: str, base: str) -> set[str]:
    """
    Извлекает ссылки из HTML-кода.

    Args:
        html (str): HTML-код для анализа.
        base (str): Базовый URL для объединения относительных ссылок.

    Returns:
        set[str]: Множество URL-адресов.
    """
```

**Назначение**:
Функция `read_links` извлекает все ссылки из HTML-кода, объединяет относительные ссылки с базовым URL и возвращает множество URL-адресов.

**Как работает функция**:

1.  Использует `BeautifulSoup` для разбора HTML-кода.
2.  Пытается найти основной контент, используя селекторы CSS.
3.  Извлекает все ссылки из элементов `<a>`, проверяя, чтобы атрибут `rel` не содержал значение `nofollow`.
4.  Объединяет относительные ссылки с базовым URL с помощью `urllib.parse.urljoin`.
5.  Возвращает множество уникальных URL-адресов.

**Примеры**:

```python
html = """
<html>
<body>
    <div class="main-content">
        <a href="https://example.com/page1">Page 1</a>
        <a href="/page2">Page 2</a>
        <a href="https://example.com/page3" rel="nofollow">Page 3</a>
    </div>
</body>
</html>
"""
base_url = "https://example.com"
links = read_links(html, base_url)
# links будет {"https://example.com/page1", "https://example.com/page2"}
```

### `download_urls`

```python
async def download_urls(
    bucket_dir: Path,
    urls: list[str],
    max_depth: int = 0,
    loading_urls: set[str] = set(),
    lock: asyncio.Lock = None,
    delay: int = 3,
    new_urls: list[str] = list(),
    group_size: int = 5,
    timeout: int = 10,
    proxy: Optional[str] = None
) -> AsyncIterator[str]:
    """
    Асинхронно скачивает файлы по URL-адресам.

    Args:
        bucket_dir (Path): Путь к директории bucket.
        urls (list[str]): Список URL-адресов для скачивания.
        max_depth (int): Максимальная глубина рекурсивного скачивания HTML-страниц.
        loading_urls (set[str]): Множество URL-адресов, которые уже находятся в процессе скачивания.
        lock (asyncio.Lock): Блокировка для синхронизации доступа к общим ресурсам.
        delay (int): Задержка в секундах между запросами.
        new_urls (list[str]): Список новых URL-адресов, найденных на скачанных HTML-страницах.
        group_size (int): Количество URL-адресов для одновременного скачивания.
        timeout (int): Максимальное время ожидания ответа от сервера в секундах.
        proxy (Optional[str]): Прокси-сервер для использования при скачивании.

    Yields:
        str: Имена скачанных файлов.
    """
```

**Назначение**:
Функция `download_urls` асинхронно скачивает файлы по списку URL-адресов, сохраняет их в указанной директории и возвращает имена скачанных файлов.

**Как работает функция**:

1.  Создает асинхронную сессию `ClientSession` для выполнения HTTP-запросов.
2.  Определяет асинхронную функцию `download_url`, которая выполняет скачивание файла по одному URL-адресу.
3.  Функция `download_url` выполняет следующие действия:
    *   Выполняет GET-запрос к указанному URL-адресу.
    *   Извлекает имя файла из ответа с помощью функции `get_filename`.
    *   Проверяет, разрешено ли расширение файла с помощью функций `is_allowed_extension` и `supports_filename`.
    *   Если файл является HTML-страницей и `max_depth` больше 0, извлекает ссылки из HTML-кода с помощью функции `read_links` и добавляет их в список `new_urls` для дальнейшего скачивания.
    *   Сохраняет содержимое файла в указанной директории.
4.  Функция `download_urls` вызывает функцию `download_url` для каждого URL-адреса в списке `urls` и возвращает имена скачанных файлов.
5.  Если в процессе скачивания HTML-страниц были найдены новые URL-адреса, функция рекурсивно вызывает `download_urls` для скачивания этих URL-адресов.

**Примеры**:

```python
bucket_dir = Path("/path/to/bucket")
urls = ["https://example.com/file1.txt", "https://example.com/file2.pdf"]
async for filename in download_urls(bucket_dir, urls, max_depth=1):
    print(filename)
# Вывод:
# file1.txt
# file2.pdf
```

### `get_downloads_urls`

```python
def get_downloads_urls(bucket_dir: Path, delete_files: bool = False) -> Iterator[str]:
    """
    Получает список URL-адресов для скачивания из файла DOWNLOADS_FILE.

    Args:
        bucket_dir (Path): Путь к директории bucket.
        delete_files (bool): Если `True`, файл DOWNLOADS_FILE будет удален после прочтения.

    Yields:
        str: URL-адреса для скачивания.
    """
```

**Назначение**:
Функция `get_downloads_urls` извлекает список URL-адресов для скачивания из файла `DOWNLOADS_FILE` в формате JSON.

**Как работает функция**:

1.  Формирует путь к файлу `DOWNLOADS_FILE` в указанной директории `bucket_dir`.
2.  Проверяет существование файла.
3.  Если файл существует, открывает его, читает содержимое в формате JSON и возвращает список URL-адресов.
4.  Если `delete_files` равно `True`, удаляет файл `DOWNLOADS_FILE` после прочтения.

**Примеры**:

Предположим, что файл `DOWNLOADS_FILE` содержит следующий JSON:

```json
[
    {"url": "https://example.com/file1.txt"},
    {"urls": ["https://example.com/file2.pdf", "https://example.com/file3.jpg"]}
]
```

```python
bucket_dir = Path("/path/to/bucket")
for item in get_downloads_urls(bucket_dir, delete_files=True):
    print(item)
# Вывод:
# {'urls': ['https://example.com/file1.txt']}
# {'urls': ['https://example.com/file2.pdf', 'https://example.com/file3.jpg']}
```

### `read_and_download_urls`

```python
def read_and_download_urls(bucket_dir: Path, delete_files: bool = False, event_stream: bool = False) -> Iterator[str]:
    """
    Читает URL-адреса из файла загрузок и скачивает их.

    Args:
        bucket_dir (Path): Путь к директории bucket.
        delete_files (bool): Если `True`, файл загрузок будет удален после прочтения.
        event_stream (bool): Если `True`, генерирует события о процессе скачивания.

    Yields:
        str: События о процессе скачивания, если `event_stream` равно `True`.
    """
```

**Назначение**:
Функция `read_and_download_urls` читает список URL-адресов из файла загрузок, скачивает файлы по этим URL-адресам и сохраняет их имена в файле `FILE_LIST`.

**Как работает функция**:

1.  Получает список URL-адресов из файла загрузок с помощью функции `get_downloads_urls`.
2.  Открывает файл `FILE_LIST` для записи имен скачанных файлов.
3.  Для каждого URL-адреса:
    *   Скачивает файл с помощью функции `download_urls`.
    *   Записывает имя скачанного файла в файл `FILE_LIST`.
    *   Если `event_stream` равно `True`, генерирует события о процессе скачивания в формате JSON.

**Примеры**:

```python
bucket_dir = Path("/path/