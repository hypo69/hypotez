### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Функция `wget_dl` предназначена для скачивания файла по заданному URL-адресу с использованием утилиты `wget`. Функция пытается скачать файл, сохраняя его под именем, соответствующим последней части URL (имя файла). В случае успеха возвращает имя скачанного файла. В случае ошибки возвращает кортеж `("error", filename)`, где `filename` – имя файла, которое пытались скачать.

Шаги выполнения
-------------------------
1. **Инициализация:**
   - Функция `wget_dl(url)` принимает URL-адрес файла для скачивания в качестве аргумента.

2. **Попытка скачивания:**
   - Внутри блока `try` функция пытается выполнить следующие действия:
     - Выводит сообщение "Downloading Started" в консоль.
     - Извлекает имя файла из URL-адреса с использованием `os.path.basename(url)` и сохраняет его в переменной `filename`.
     - Выполняет команду `wget` через `subprocess.check_output` для скачивания файла. Команда `wget` использует опцию `--output-document` для сохранения файла под именем `filename`.

3. **Обработка результата скачивания:**
   - Если скачивание прошло успешно, функция выводит сообщение "Downloading Complete" и имя скачанного файла в консоль.
   - Возвращает имя скачанного файла `filename`.

4. **Обработка ошибок:**
   - Если во время скачивания возникает исключение, функция переходит в блок `except`.
   - Выводит сообщение об ошибке "DOWNLAOD ERROR :" и текст ошибки `e` в консоль.
   - Возвращает кортеж `("error", filename)`, где `filename` – имя файла, которое пытались скачать.

Пример использования
-------------------------

```python
import os
import subprocess

def wget_dl(url: str) -> str | tuple[str, str]:
    """
    Скачивает файл по заданному URL-адресу с использованием утилиты `wget`.

    Args:
        url (str): URL-адрес файла для скачивания.

    Returns:
        str | tuple[str, str]: Имя скачанного файла в случае успеха или кортеж ("error", filename) в случае ошибки.

    Raises:
        subprocess.CalledProcessError: Если команда `wget` завершается с ненулевым кодом возврата.
        Exception: В случае других ошибок при скачивании.

    Example:
        >>> url = "https://example.com/file.txt"
        >>> result = wget_dl(url)
        >>> if result == "error":
        ...     print("Ошибка при скачивании файла")
        ... else:
        ...     print(f"Файл успешно скачан: {result}")
    """
    try:
        print("Downloading Started")
        filename = os.path.basename(url)
        output = subprocess.check_output(
            f"wget --output-document '{filename}' '{url}'",
            stderr=subprocess.STDOUT,
            shell=True,
            encoding='utf-8'
        )

        print("Downloading Complete", filename)
        return filename
    except subprocess.CalledProcessError as e:
        print(f"DOWNLAOD ERROR: {e}")
        return "error", filename
    except Exception as e:
        print(f"DOWNLAOD ERROR: {e}")
        return "error", filename

# Пример вызова функции
url = "https://www.w3.org/TR/PNG/iso_8859-1.txt"
result = wget_dl(url)

if result[0] == "error":
    print("Произошла ошибка при скачивании файла.")
else:
    print(f"Файл '{result}' успешно скачан.")