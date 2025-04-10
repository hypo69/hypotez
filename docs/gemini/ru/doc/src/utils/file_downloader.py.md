# Модуль для скачивания файлов

## Обзор

Модуль содержит функцию `download_file`, которая позволяет скачивать файлы по указанному URL-адресу и сохранять их на диск.

## Подробней

Этот модуль предоставляет простой способ загрузки файлов из интернета. Функция `download_file` отправляет HTTP-запрос и сохраняет содержимое ответа в файл, обеспечивая обработку ошибок и поддержку больших файлов за счет скачивания по частям.

## Функции

### `download_file`

**Назначение**: Скачивает файл по указанному URL и сохраняет его в указанное место на диске.

```python
def download_file(url, destination):
    """
    Скачивает файл по указанному URL и сохраняет его на диск.

    Args:
        url (str): URL файла для скачивания.
        destination (str): Путь для сохранения скачанного файла.

    Returns:
        None

    Raises:
        requests.exceptions.RequestException: Если возникает ошибка при выполнении HTTP-запроса.
        IOError: Если возникает ошибка при записи файла на диск.

    Example:
        >>> file_url = 'https://example.com/path/to/file.txt'
        >>> save_as = 'downloaded_file.txt'
        >>> download_file(file_url, save_as)
        Файл успешно загружен!
    """
```

**Параметры**:
- `url` (str): URL-адрес файла, который необходимо скачать.
- `destination` (str): Путь к файлу, в который будет сохранено содержимое скачанного файла.

**Возвращает**:
- `None`

**Как работает функция**:
1. Функция отправляет GET-запрос на указанный URL с параметром `stream=True`, что позволяет скачивать файл частями.
2. Проверяет, успешен ли запрос (код ответа 200). Если нет, выводит сообщение об ошибке.
3. Если запрос успешен, открывает файл в бинарном режиме для записи.
4. Скачивает файл по частям (размером 1024 байта) и записывает каждую часть в файл.
5. Выводит сообщение об успешной загрузке.

**Примеры**:
```python
file_url = 'https://example.com/path/to/file.txt'
save_as = 'downloaded_file.txt'
download_file(file_url, save_as)
```
В этом примере функция `download_file` используется для скачивания файла с URL-адреса `https://example.com/path/to/file.txt` и сохранения его под именем `downloaded_file.txt`.

```python
file_url = 'https://example.com/path/to/another_file.txt'
save_as = '/tmp/another_file.txt'
download_file(file_url, save_as)
```
В этом примере функция `download_file` используется для скачивания файла с URL-адреса `https://example.com/path/to/another_file.txt` и сохранения его под именем `/tmp/another_file.txt`.

```python
try:
    file_url = 'https://nonexistent-website.com/file.txt'
    save_as = 'test_file.txt'
    download_file(file_url, save_as)
except requests.exceptions.RequestException as ex:
    print(f"Произошла ошибка при скачивании файла: {ex}")
```
В этом примере показана обработка исключения, которое может возникнуть при попытке скачать файл с несуществующего URL.