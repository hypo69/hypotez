# Модуль для скачивания файлов по URL с использованием wget
## Обзор

Модуль содержит функцию `wget_dl`, которая используется для скачивания файлов по URL с использованием утилиты `wget`. Функция обрабатывает исключения и возвращает имя скачанного файла или сообщение об ошибке.

## Подробней

Этот модуль предоставляет простой способ скачивания файлов из интернета с использованием команды `wget`. Он может быть полезен в тех случаях, когда необходимо автоматизировать скачивание файлов в рамках других процессов или скриптов. Модуль обрабатывает возможные ошибки при скачивании и возвращает информацию о результате операции.

## Функции

### `wget_dl`

```python
def wget_dl(url):
    """
    Скачивает файл по указанному URL с использованием утилиты wget.

    Args:
        url (str): URL файла для скачивания.

    Returns:
        str: Имя скачанного файла в случае успеха или "error" в случае ошибки.

    Raises:
        Exception: Если возникает ошибка при выполнении команды wget.

    Принцип работы:
    - Функция принимает URL файла для скачивания.
    - Извлекает имя файла из URL.
    - Формирует команду wget для скачивания файла с указанным именем.
    - Выполняет команду wget с помощью subprocess.check_output.
    - Возвращает имя скачанного файла в случае успеха.
    - В случае ошибки выводит сообщение об ошибке и возвращает "error".

    Примеры:
        >>> wget_dl('https://example.com/file.txt')
        Downloading Started
        Downloading Complete file.txt
        'file.txt'

        >>> wget_dl('https://example.com/error')
        Downloading Started
        DOWNLAOD ERROR : ...
        ('error', 'error')
    """
    try:
        print("Downloading Started")
        # i was facing some problem in filename That's Why i did this ,
        #  i will fix it later :(

        filename = os.path.basename(url)
        output = subprocess.check_output("wget \'--output-document\' \'{}\' \'{}\' ".format(filename , url), stderr=subprocess.STDOUT, shell=True)
        
        print("Downloading Complete",filename)
        return filename
    except Exception as ex:
        print("DOWNLAOD ERROR :",ex)
        return "error",filename
```
**Назначение**: Скачивает файл по указанному URL с использованием утилиты `wget`.

**Параметры**:
- `url` (str): URL файла для скачивания.

**Возвращает**:
- `str`: Имя скачанного файла в случае успеха или "error" в случае ошибки.

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при выполнении команды `wget`.

**Как работает функция**:
1. Выводит сообщение "Downloading Started" в консоль.
2. Извлекает имя файла из URL с помощью `os.path.basename(url)`.
3. Формирует команду `wget` для скачивания файла с указанным именем и URL.
4. Выполняет команду `wget` с помощью `subprocess.check_output`.
5. Если команда выполнена успешно, выводит сообщение "Downloading Complete" и имя файла в консоль.
6. Возвращает имя скачанного файла.
7. Если во время выполнения команды `wget` возникает исключение, выводит сообщение об ошибке в консоль.
8. Возвращает кортеж `("error", filename)`.

**Примеры**:

```python
# Пример успешного скачивания файла
url = 'https://example.com/file.txt'
result = wget_dl(url)
print(result)  # Вывод: file.txt

# Пример неудачного скачивания файла
url = 'https://example.com/error'
result = wget_dl(url)
print(result)  # Вывод: ('error', 'error')