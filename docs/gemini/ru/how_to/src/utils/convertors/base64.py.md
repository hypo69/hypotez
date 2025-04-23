### Как использовать блок кода `base64_to_tmpfile` и `base64encode`
=========================================================================================

Описание
-------------------------
Модуль предоставляет функции для кодирования и декодирования контента Base64, включая сохранение декодированного контента во временный файл и кодирование изображения в строку Base64.

Шаги выполнения
-------------------------
1. **Декодирование Base64 и запись во временный файл**:
   - Функция `base64_to_tmpfile` принимает закодированный контент Base64 и имя файла.
   - Функция извлекает расширение файла из имени файла.
   - Функция создает временный файл с тем же расширением.
   - Декодированный контент записывается во временный файл.
   - Функция возвращает путь к этому временному файлу.

2. **Кодирование изображения в Base64**:
    - Функция `base64encode` принимает путь к файлу изображения.
    - Функция открывает файл изображения в бинарном режиме для чтения.
    - Содержимое файла изображения кодируется в формат Base64.
    - Функция возвращает строку, представляющую собой Base64 представление изображения.

Пример использования
-------------------------

```python
import base64
import tempfile
import os

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
    _, ext = os.path.splitext(file_name)
    path = ''
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(base64.b64decode(content))
        path = tmp.name

    return path

def base64encode(image_path):
    """
    Encodes an image file to a Base64 string.

    This function opens the image file in binary read mode, encodes its content using Base64 encoding,
    and returns the Base64 encoded string.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: The Base64 encoded string of the image file.
    """
    # Function to encode the image
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Пример использования base64_to_tmpfile:
base64_content = "SGVsbG8gd29ybGQh"  # Base64 encoded content "Hello world!"
file_name = "example.txt"
tmp_file_path = base64_to_tmpfile(base64_content, file_name)
print(f"Temporary file created at: {tmp_file_path}")

# Пример использования base64encode:
image_path = 'path/to/your/image.jpg'
base64_string = base64encode(image_path)
print(f"Base64 string: {base64_string[:50]}...")  # Вывод первых 50 символов
```