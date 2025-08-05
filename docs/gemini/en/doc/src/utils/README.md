# Tiny Utils

|                                                                                       |                                                                             |                                                                                |
| :------------------------------------------------------------------------------------ | :-------------------------------------------------------------------------- | :----------------------------------------------------------------------------- |
| [Root ↑](https://github.com/hypo69/hypotez/blob/master/README.MD)                   | src                                                                         | [Русский](https://github.com/hypo69/hypotez/blob/master/src/utils/readme.ru.md) |
|                                                                                       | [src](https://github.com/hypo69/hypotez/blob/master/src/README.MD)          |                                                                                |
|                                                                                       |                                                                             |                                                                                |

**Tiny Utils** - это библиотека утилит, предоставляющая набор легковесных вспомогательных функций для различных распространенных задач. Эта библиотека включает в себя утилиты для преобразования форматов данных, манипулирования текстом и файлами, строковых операций, форматирования даты и времени, обработки изображений и многого другого. Она организована в несколько модулей для легкого доступа к определенным функциональным возможностям.

## Table of Contents

- [Tiny Utils](#tiny-utils)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Modules Overview](#modules-overview)
  - [Module Descriptions](#module-descriptions)
    - [Convertors](#convertors)
      - [Files:](#files)
    - [String Utilities](#string-utilities)
    - [File Operations](#file-operations)
    - [Date-Time Utilities](#date-time-utilities)
    - [FTP Utilities](#ftp-utilities)
    - [Image Utilities](#image-utilities)
    - [PDF Utilities](#pdf-utilities)
    - [Printer Utilities](#printer-utilities)
  - [Usage Examples](#usage-examples)
    - [Convert Text to PNG Image](#convert-text-to-png-image)
    - [Convert XML to Dictionary](#convert-xml-to-dictionary)
    - [Parse and Manipulate JSON](#parse-and-manipulate-json)
  - [Contributing](#contributing)
  - [License](#license)

## Installation

Чтобы использовать **Tiny Utils**, клонируйте репозиторий и установите все необходимые зависимости, указанные в файле `requirements.txt`.

```bash
git clone https://github.com/hypo69/tiny-utils.git
cd tiny_utils
pip install -r requirements.txt
```

## Modules Overview

Эта библиотека содержит несколько подмодулей, каждый из которых обрабатывает определенную задачу:

- **Convertors**: Модули для преобразования форматов данных, таких как текст в изображение, webp в png, JSON, XML, кодировка Base64 и многое другое.
- **String Utilities**: Инструменты для расширенного манипулирования строками.
- **File Operations**: Функции для обработки файлов и манипулирования ими.
- **Date-Time Utilities**: Инструменты для форматирования даты и времени.
- **FTP Utilities**: Функции для обработки файлов FTP.
- **Image Utilities**: Базовые функции обработки изображений.
- **PDF Utilities**: Манипулирование файлами PDF и преобразование.
- **Printer Utilities**: Функции для отправки данных на принтер.

## Module Descriptions

### Convertors

Модуль `convertors` содержит утилиты для преобразования данных между форматами. Эти модули могут обрабатывать различные типы данных, от CSV до JSON и от текста до изображений.

#### Files:

- **text2png.py**: Преобразует текстовые данные в файл изображения PNG.
- **tts.py**: Преобразует текст в речь и сохраняет его в виде аудиофайла.
- **webp2png.py**: Преобразует изображения из формата WebP в формат PNG.
- **xls.py**: Обрабатывает преобразования и манипуляции с файлами XLS.
- **xml2dict.py**: Преобразует данные XML в словарь Python.
- **base64.py**: Кодирует или декодирует данные с использованием кодировки Base64.
- **csv.py**: Предоставляет инструменты для анализа и манипулирования CSV.
- **dict.py**: Утилиты для обработки словарей Python.
- **html.py**: Преобразует содержимое HTML в различные форматы.
- **json.py**: Утилиты для анализа и манипулирования JSON.
- **md2dict.py**: Преобразует содержимое Markdown в словарь.
- **ns.py**: Специализированные утилиты для преобразования пространств имен.

### String Utilities

Модуль `string` включает в себя расширенные функции для манипулирования строками, предлагая инструменты для улучшения базовых операций со строками Python.

### File Operations

Модуль `file.py` включает в себя утилиты для обработки файлов, предоставляя функции для чтения, записи, копирования, удаления и перемещения файлов с дополнительными параметрами для обработки ошибок и совместимости форматов файлов.

### Date-Time Utilities

Модуль `date_time.py` предоставляет различные утилиты даты и времени, позволяющие пользователям анализировать, форматировать и манипулировать значениями даты и времени для обеспечения согласованного форматирования и преобразований.

### FTP Utilities

Модуль `ftp.py` включает в себя функции для обработки операций FTP, таких как подключение к серверам, загрузка, скачивание и управление файлами через FTP.

### Image Utilities

Модуль `image.py` предоставляет базовые инструменты для манипулирования изображениями, такие как изменение размера, обрезка, преобразование форматов и применение фильтров.

### PDF Utilities

Модуль `pdf.py` предлагает утилиты для обработки PDF, включая преобразование файлов PDF, объединение, разделение и извлечение текста.

### Printer Utilities

Модуль `printer.py` включает в себя функции для отправки файлов или отформатированных данных на принтер, поддерживая параметры конфигурации заданий печати.

## Usage Examples

Вот несколько примеров использования, демонстрирующих, как работать с библиотекой **Tiny Utils**.

### Convert Text to PNG Image

```python
from tiny_utils.convertors import text2png

text = "Hello, World!"
output_path = "output_image.png"
text2png.convert(text, output_path)
```

### Convert XML to Dictionary

```python
from tiny_utils.convertors import xml2dict

xml_data = "<root><item>Hello</item></root>"
dictionary = xml2dict.convert(xml_data)
print(dictionary)
```

### Parse and Manipulate JSON

```python
from tiny_utils.convertors import json

json_data = '{"name": "John", "age": 30}'
parsed_data = json.parse(json_data)
print(parsed_data)
```

Для получения дополнительных примеров и подробной документации посетите

[Tiny Utils Wiki](https://github.com/hypo69/tiny-utils/wiki).

## Contributing

Вклад приветствуется! Пожалуйста, сделайте форк репозитория и отправьте запрос на внесение изменений. Не забудьте обновить документацию для любых новых функций или изменений.

## License

Этот проект лицензирован в соответствии с лицензией MIT. См. файл [LICENSE](./LICENSE) для получения дополнительной информации.