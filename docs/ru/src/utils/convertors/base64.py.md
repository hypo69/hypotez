# Модуль для конвертации Base64 контента во временный файл
## Обзор

Модуль `base64.py` предоставляет функции для работы с кодировкой Base64. Он позволяет декодировать Base64 контент и сохранять его во временный файл. Это может быть полезно, когда необходимо работать с данными, закодированными в Base64 формате, например, при обработке изображений или других бинарных файлов, полученных через сеть.

## Подробней

Данный модуль содержит функции для преобразования данных из формата Base64 во временные файлы и обратно. Это упрощает работу с данными, передаваемыми в закодированном виде, позволяя временно сохранять их на диске для дальнейшей обработки. Модуль использует стандартные библиотеки Python, такие как `base64`, `tempfile` и `os`, чтобы обеспечить эффективное и безопасное выполнение операций.
Пример использования: модуль используется, когда необходимо декодировать содержимое атрибута `src` тега `img` на веб-странице, которое представлено в формате base64. Далее модуль воссоздает картинку во временном файле

## Функции

### `base64_to_tmpfile`

```python
def base64_to_tmpfile(content: str, file_name: str) -> str:
    """
    Convert Base64 encoded content to a temporary file.

    This function decodes the Base64 encoded content and writes it to a temporary file with the same extension as the provided file name. 
    The path to the temporary file is returned.

    Args:
        content (str): Base64 encoded content to be decoded and written to the file.
        file_name (str): Name of the file used to extract the file extension for the temporary file.

    Returns:
        str: Path to the temporary file.

    Example:
        >>> base64_content = "SGVsbG8gd29ybGQh"  # Base64 encoded content "Hello world!"
        >>> file_name = "example.txt"
        >>> tmp_file_path = base64_to_tmpfile(base64_content, file_name)
        >>> print(f"Temporary file created at: {tmp_file_path}")
        Temporary file created at: /tmp/tmpfile.txt
    """
    ...
```

**Назначение**: Преобразует Base64 закодированный контент во временный файл.

**Параметры**:

-   `content` (str): Base64 закодированный контент для декодирования и записи в файл.
-   `file_name` (str): Имя файла, используемое для извлечения расширения файла для временного файла.

**Возвращает**:

-   `str`: Путь к временному файлу.

**Как работает функция**:

1.  **Извлечение расширения файла**: Извлекается расширение файла из предоставленного имени файла.
2.  **Создание временного файла**: Создается временный файл с использованием модуля `tempfile`. Файл создается с расширением, полученным из имени файла, и по умолчанию удаляется при закрытии.
3.  **Декодирование и запись контента**: Base64 контент декодируется с использованием `base64.b64decode(content)`, и результат записывается во временный файл.
4.  **Сохранение пути к файлу**: Путь к созданному временному файлу сохраняется в переменной `path`.
5.  **Возврат пути**: Функция возвращает путь к временному файлу.

```
Извлечение расширения файла
      |
      ↓
Создание временного файла
      |
      ↓
Декодирование и запись контента
      |
      ↓
    Возврат пути к файлу
```

**Примеры**:

```python
>>> base64_content = "SGVsbG8gd29ybGQh"  # Base64 encoded content "Hello world!"
>>> file_name = "example.txt"
>>> tmp_file_path = base64_to_tmpfile(base64_content, file_name)
>>> print(f"Temporary file created at: {tmp_file_path}")
Temporary file created at: /tmp/tmpfile.txt
```

### `base64encode`

```python
def base64encode(image_path):
    # Function to encode the image
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
```

**Назначение**: Кодирует изображение в формат Base64.

**Параметры**:

-   `image_path` (str): Путь к файлу изображения.

**Возвращает**:

-   `str`: Base64 закодированное представление изображения.

**Как работает функция**:

1.  **Открытие файла изображения**: Открывает файл изображения по указанному пути в двоичном режиме для чтения.
2.  **Чтение содержимого файла**: Считывает все содержимое файла изображения.
3.  **Кодирование в Base64**: Кодирует содержимое файла изображения в формат Base64.
4.  **Декодирование в UTF-8**: Декодирует Base64 закодированное содержимое в строку UTF-8.
5.  **Возврат закодированной строки**: Возвращает Base64 закодированную строку.

```
   Открытие файла изображения
      |
      ↓
Чтение содержимого файла
      |
      ↓
   Кодирование в Base64
      |
      ↓
  Декодирование в UTF-8
      |
      ↓
Возврат закодированной строки
```

**Примеры**:

```python
>>> image_path = "example.png"
>>> encoded_string = base64encode(image_path)
>>> print(f"Base64 encoded string: {encoded_string[:100]}...")
Base64 encoded string: iVBORw0KGgoAAAANSUhEUgAA...