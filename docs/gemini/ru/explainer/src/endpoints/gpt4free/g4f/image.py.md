### **Системные инструкции для обработки кода проекта `hypotez`**

=========================================================================================

Описание функциональности и правил для генерации, анализа и улучшения кода. Направлено на обеспечение последовательного и читаемого стиля кодирования, соответствующего требованиям.

---

### **Основные принципы**

#### **1. Общие указания**:
- Соблюдай четкий и понятный стиль кодирования.
- Все изменения должны быть обоснованы и соответствовать установленным требованиям.

#### **2. Комментарии**:
- Используй `#` для внутренних комментариев.
- Документация всех функций, методов и классов должна следовать такому формату: 
    ```python
        def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:
            """ 
            Args:
                param (str): Описание параметра `param`.
                param1 (Optional[str | dict | str], optional): Описание параметра `param1`. По умолчанию `None`.
    
            Returns:
                dict | None: Описание возвращаемого значения. Возвращает словарь или `None`.
    
            Raises:
                SomeError: Описание ситуации, в которой возникает исключение `SomeError`.

            Ехаmple:
                >>> function('param', 'param1')
                {'param': 'param1'}
            """
    ```
- Комментарии и документация должны быть четкими, лаконичными и точными.

#### **3. Форматирование кода**:
- Используй одинарные кавычки. `a:str = 'value'`, `print('Hello World!')`;
- Добавляй пробелы вокруг операторов. Например, `x = 5`;
- Все параметры должны быть аннотированы типами. `def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:`;
- Не используй `Union`. Вместо этого используй `|`.

#### **4. Логирование**:
- Для логгирования Всегда Используй модуль `logger` из `src.logger.logger`.
- Ошибки должны логироваться с использованием `logger.error`.
Пример:
    ```python
        try:
            ...
        except Exception as ex:
            logger.error('Error while processing data', ех, exc_info=True)
    ```
#### **5 Не используй `Union[]` в коде. Вместо него используй `|`
Например:
```python
x: str | int ...
```




---

### **Основные требования**:

#### **1. Формат ответов в Markdown**:
- Все ответы должны быть выполнены в формате **Markdown**.

#### **2. Формат комментариев**:
- Используй указанный стиль для комментариев и документации в коде.
- Пример:

```python
from typing import Generator, Optional, List
from pathlib import Path


def read_text_file(
    file_path: str | Path,
    as_list: bool = False,
    extensions: Optional[List[str]] = None,
    chunk_size: int = 8192,
) -> Generator[str, None, None] | str | None:
    """
    Считывает содержимое файла (или файлов из каталога) с использованием генератора для экономии памяти.

    Args:
        file_path (str | Path): Путь к файлу или каталогу.
        as_list (bool): Если `True`, возвращает генератор строк.
        extensions (Optional[List[str]]): Список расширений файлов для чтения из каталога.
        chunk_size (int): Размер чанков для чтения файла в байтах.

    Returns:
        Generator[str, None, None] | str | None: Генератор строк, объединенная строка или `None` в случае ошибки.

    Raises:
        Exception: Если возникает ошибка при чтении файла.

    Example:
        >>> from pathlib import Path
        >>> file_path = Path('example.txt')
        >>> content = read_text_file(file_path)
        >>> if content:
        ...    print(f'File content: {content[:100]}...')
        File content: Example text...
    """
    ...
```
- Всегда делай подробные объяснения в комментариях. Избегай расплывчатых терминов, 
- таких как *«получить»* или *«делать»*. Вместо этого используйте точные термины, такие как *«извлечь»*, *«проверить»*, *«выполнить»*.
- Вместо: *«получаем»*, *«возвращаем»*, *«преобразовываем»* используй имя объекта *«функция получае»*, *«переменная возвращает»*, *«код преобразовывает»* 
- Комментарии должны непосредственно предшествовать описываемому блоку кода и объяснять его назначение.

#### **3. Пробелы вокруг операторов присваивания**:
- Всегда добавляйте пробелы вокруг оператора `=`, чтобы повысить читаемость.
- Примеры:
  - **Неправильно**: `x=5`
  - **Правильно**: `x = 5`

#### **4. Использование `j_loads` или `j_loads_ns`**:
- Для чтения JSON или конфигурационных файлов замените стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns`.
- Пример:

```python
# Неправильно:
with open('config.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Правильно:
data = j_loads('config.json')
```

#### **5. Сохранение комментариев**:
- Все существующие комментарии, начинающиеся с `#`, должны быть сохранены без изменений в разделе «Улучшенный код».
- Если комментарий кажется устаревшим или неясным, не изменяйте его. Вместо этого отметьте его в разделе «Изменения».

#### **6. Обработка `...` в коде**:
- Оставляйте `...` как указатели в коде без изменений.
- Не документируйте строки с `...`.
```

#### **7. Аннотации**
Для всех переменных должны быть определены аннотации типа. 
Для всех функций все входные и выходные параметры аннотириваны
Для все параметров должны быть аннотации типа.


### **8. webdriver**
В коде используется webdriver. Он импртируется из модуля `webdriver` проекта `hypotez`
```python
from src.webdirver import Driver, Chrome, Firefox, Playwright, ...
driver = Driver(Firefox)

Пoсле чего может использоваться как

close_banner = {
  "attribute": null,
  "by": "XPATH",
  "selector": "//button[@id = 'closeXButton']",
  "if_list": "first",
  "use_mouse": false,
  "mandatory": false,
  "timeout": 0,
  "timeout_for_event": "presence_of_element_located",
  "event": "click()",
  "locator_description": "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
}

result = driver.execute_locator(close_banner)
```

### Анализ кода `hypotez/src/endpoints/gpt4free/g4f/image.py`

#### 1. Блок-схема

```mermaid
graph TD
    A[Начало] --> B{Проверка наличия "pillow"}
    B -- Нет --> C[Выброс MissingRequirementsError: установите "pillow"]
    B -- Да --> D{image является str и начинается с "data:"?}
    D -- Да --> E[Вызов is_data_uri_an_image(image)]
    E --> F[Вызов extract_data_uri(image)]
    D -- Нет --> G{image является SVG?}
    G -- Да --> H{Проверка наличия "cairosvg"}
    H -- Нет --> I[Выброс MissingRequirementsError: установите "cairosvg"]
    H -- Да --> J{image является bytes?}
    J -- Нет --> K[Чтение image]
    K --> L[cairosvg.svg2png(image, write_to=buffer)]
    J -- Да --> L[cairosvg.svg2png(image, write_to=buffer)]
    G -- Нет --> M{image является bytes?}
    M -- Да --> N[Вызов is_accepted_format(image)]
    N --> O[open_image(BytesIO(image))]
    M -- Нет --> P{image является PIL.Image.Image?}
    P -- Нет --> Q[image = open_image(image); image.load()]
    Q --> R[Возврат image]
    P -- Да --> R[Возврат image]
    L --> S[Возврат open_image(buffer)]
    F --> T[Вызов extract_data_uri(image)] --> U[Возврат open_image(BytesIO(T))]
    O --> R
    U --> R
```

#### 2. Диаграмма

```mermaid
graph TD
    subgraph PIL (Pillow)
        open_image[open as open_image]
        new_image[new as new_image]
        FLIP_LEFT_RIGHT
        ROTATE_180
        ROTATE_270
        ROTATE_90
    end

    subgraph Standard Libraries
        os
        re
        io
        base64
        urllib_parse[urllib.parse]
        BytesIO[io.BytesIO]
        Path[pathlib.Path]
    end

    subgraph Local Modules
        typing[.typing]
        errors[.errors]
        requests_aiohttp[.requests.aiohttp]
    end

    subgraph cairosvg
        cairosvg
    end

    Start --> PIL
    Start --> Standard Libraries
    Start --> Local Modules
    
    LocalModules --> typing
    LocalModules --> errors
    LocalModules --> requests_aiohttp
    
    errors --> MissingRequirementsError
    requests_aiohttp --> get_connector
```

**Объяснение зависимостей:**

-   **PIL (Pillow)**: Используется для работы с изображениями, включая открытие, создание, изменение размера и преобразование. Зависимости включают `open as open_image`, `new as new_image`, `FLIP_LEFT_RIGHT`, `ROTATE_180`, `ROTATE_270`, `ROTATE_90`.

-   **Standard Libraries**:
    -   `os`: Предоставляет функции для взаимодействия с операционной системой.
    -   `re`: Используется для работы с регулярными выражениями, например, для проверки формата data URI.
    -   `io`: Предоставляет инструменты для работы с потоками ввода-вывода данных.
    -   `base64`: Используется для кодирования и декодирования данных в формате Base64, особенно для data URI.
    -   `urllib.parse`: Используется для работы с URL, например, для кодирования специальных символов.
    -   `pathlib.Path`: Используется для представления путей к файлам и директориям в объектно-ориентированном стиле.
    -   `io.BytesIO`: Используется для работы с бинарными данными в памяти как с файлами.

-   **Local Modules**:
    -   `.typing`: Определяет типы данных, используемые в модуле, такие как `ImageType`, `Union`, `Image`, `Optional`, `Cookies`.
    -   `.errors`: Содержит определения пользовательских исключений, таких как `MissingRequirementsError`.
    -   `.requests.aiohttp`: Содержит функции для выполнения асинхронных HTTP-запросов.

-   **cairosvg**: Используется для преобразования SVG-изображений в PNG-формат.

#### 3. Объяснение

**Импорты:**

-   `from __future__ import annotations`: Позволяет использовать аннотации типов, которые ссылаются на класс, который еще не определен.
-   `import os`: Используется для работы с операционной системой, например, для проверки существования файлов.
-   `import re`: Используется для работы с регулярными выражениями, например, для проверки формата data URI.
-   `import io`: Предоставляет инструменты для работы с потоками ввода-вывода данных.
-   `import base64`: Используется для кодирования и декодирования данных в формате Base64, особенно для data URI.
-   `from urllib.parse import quote_plus`: Используется для кодирования специальных символов в URL.
-   `from io import BytesIO`: Используется для работы с бинарными данными в памяти как с файлами.
-   `from pathlib import Path`: Используется для представления путей к файлам и директориям в объектно-ориентированном стиле.
-   `from PIL.Image import open as open_image, new as new_image`: Импортирует функции для открытия и создания изображений из библиотеки Pillow.
-   `from PIL.Image import FLIP_LEFT_RIGHT, ROTATE_180, ROTATE_270, ROTATE_90`: Импортирует константы для поворота и отражения изображений.
-   `from .typing import ImageType, Union, Image, Optional, Cookies`: Импортирует типы данных, используемые в модуле.
-   `from .errors import MissingRequirementsError`: Импортирует класс исключения, который выбрасывается, если отсутствуют необходимые зависимости.
-   `from .requests.aiohttp import get_connector`: Импортирует функцию для получения коннектора для асинхронных HTTP-запросов.

**Переменные:**

-   `ALLOWED_EXTENSIONS: set[str] = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}`: Определяет множество допустимых расширений файлов изображений.
-   `EXTENSIONS_MAP: dict[str, str] = {"image/png": "png", "image/jpeg": "jpg", "image/gif": "gif", "image/webp": "webp"}`: Сопоставляет MIME-типы изображений с их расширениями.
-   `images_dir = "./generated_images"`: Определяет директорию для сгенерированных изображений.

**Функции:**

-   `to_image(image: ImageType, is_svg: bool = False) -> Image`: Преобразует входное изображение в объект PIL Image.

    -   `image` (`ImageType`): Входное изображение, которое может быть строкой (путь к файлу или data URI), байтами или объектом PIL Image.
    -   `is_svg` (`bool`): Флаг, указывающий, является ли изображение SVG.
    -   Возвращает объект `Image` из библиотеки PIL.
    -   Пример:

    ```python
    image = to_image("image.png")
    ```

-   `is_allowed_extension(filename: str) -> bool`: Проверяет, имеет ли заданное имя файла допустимое расширение.

    -   `filename` (`str`): Имя файла для проверки.
    -   Возвращает `True`, если расширение допустимо, `False` в противном случае.
    -   Пример:

    ```python
    is_allowed_extension("image.png")  # True
    is_allowed_extension("image.txt")  # False
    ```

-   `is_data_uri_an_image(data_uri: str) -> None`: Проверяет, представляет ли заданный data URI изображение.

    -   `data_uri` (`str`): Data URI для проверки.
    -   Выбрасывает `ValueError`, если data URI недействителен или формат изображения не разрешен.
    -   Пример:

    ```python
    is_data_uri_an_image("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w+G4eRKRogwWAQSGQAQFAAJOQQVwMCYlAAAAAElFTkSuQmCC")
    ```

-   `is_accepted_format(binary_data: bytes) -> str`: Проверяет, представляет ли заданный двоичный код изображение с принятым форматом.

    -   `binary_data` (`bytes`): Двоичные данные для проверки.
    -   Возвращает MIME-тип изображения, если формат принят.
    -   Выбрасывает `ValueError`, если формат изображения не разрешен.
    -   Пример:

    ```python
    with open("image.png", "rb") as f:
        binary_data = f.read()
    is_accepted_format(binary_data)  # "image/png"
    ```

-   `extract_data_uri(data_uri: str) -> bytes`: Извлекает двоичные данные из заданного data URI.

    -   `data_uri` (`str`): Data URI.
    -   Возвращает извлеченные двоичные данные.
    -   Пример:

    ```python
    data_uri = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w+G4eRKRogwWAQSGQAQFAAJOQQVwMCYlAAAAAElFTkSuQmCC"
    extract_data_uri(data_uri)  # b'\x89PNG\r\n...'
    ```

-   `get_orientation(image: Image) -> int`: Получает ориентацию заданного изображения.

    -   `image` (`Image`): Изображение.
    -   Возвращает значение ориентации.
    -   Пример:

    ```python
    image = open_image("image.jpg")
    get_orientation(image)  # 1
    ```

-   `process_image(image: Image, new_width: int, new_height: int) -> Image`: Обрабатывает заданное изображение, корректируя его ориентацию и изменяя его размер.

    -   `image` (`Image`): Изображение для обработки.
    -   `new_width` (`int`): Новая ширина изображения.
    -   `new_height` (`int`): Новая высота изображения.
    -   Возвращает обработанное изображение.
    -   Пример:

    ```python
    image = open_image("image.jpg")
    processed_image = process_image(image, 100, 100)
    ```

-   `to_bytes(image: ImageType) -> bytes`: Преобразует заданное изображение в байты.

    -   `image` (`ImageType`): Изображение для преобразования.
    -   Возвращает изображение в виде байтов.
    -   Пример:

    ```python
    image = open_image("image.png")
    image_bytes = to_bytes(image)
    ```

-   `to_data_uri(image: ImageType) -> str`: Преобразует заданное изображение в data URI.

    -   `image` (`ImageType`): Изображение для преобразования.
    -   Возвращает изображение в виде data URI.
    -   Пример:

    ```python
    image = open_image("image.png")
    data_uri = to_data_uri(image)
    ```

**Классы:**

-   `ImageDataResponse`: Представляет ответ с данными изображения.
    -   `__init__(self, images: Union[str, list], alt: str)`: Конструктор класса.
        -   `images` (`Union[str, list]`): Изображения в виде строки или списка строк.
        -   `alt` (`str`): Альтернативный текст для изображений.
    -   `get_list(self) -> list[str]`: Возвращает список изображений.
-   `ImageRequest`: Представляет запрос изображения.
    -   `__init__(self, options: dict = {})`: Конструктор класса.
        -   `options` (`dict`): Опции запроса.
    -   `get(self, key: str)`: Возвращает значение опции по ключу.

**Потенциальные ошибки и области для улучшения:**

-   Необходимо добавить обработку исключений для случаев, когда PIL не может открыть изображение.
-   Стоит добавить логирование для отладки и мониторинга.

**Взаимосвязи с другими частями проекта:**

-   Этот модуль используется для обработки изображений, которые могут быть получены из различных источников, таких как файлы, data URI или HTTP-запросы.
-   Он используется в конечных точках GPT4Free для обработки изображений, сгенерированных моделью.