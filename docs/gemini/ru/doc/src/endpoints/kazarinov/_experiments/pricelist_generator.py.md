# Модуль pricelist_generator

## Обзор

Модуль `pricelist_generator`  представляет собой экспериментальный код для генерации PDF-отчета.  Он использует данные из JSON-файла и создает HTML-файл, который затем преобразуется в PDF.

## Подробности

Этот модуль использует данные из JSON-файла, который расположен в каталоге `kazarinov/mexironim`. Данные загружаются с помощью функции `j_loads`, а затем передаются в класс `ReportGenerator` для создания HTML-файла. Затем HTML-файл преобразуется в PDF с помощью библиотеки `pdfkit`.

## Классы

### `ReportGenerator`

**Описание**:  Класс `ReportGenerator` используется для генерации HTML-отчета из данных JSON.

**Атрибуты**:

- `path_to_template`: Путь к HTML-шаблону для отчета.

**Методы**:

- `create_report`: Создает HTML-файл с данными JSON.

## Функции

### `main`

**Назначение**:  Главная функция модуля.

**Параметры**:

- `data`: Данные в формате JSON, которые используются для генерации отчета.
- `html_file`: Путь к HTML-файлу, который будет создан.
- `pdf_file`: Путь к PDF-файлу, который будет создан.

**Возвращает**:

- None

**Как работает функция**:

- Загружает данные из JSON-файла.
- Создает HTML-файл с помощью класса `ReportGenerator`.
- Преобразует HTML-файл в PDF.

**Примеры**:

```python
from pathlib import Path
import header
from src import gs

from src.endpoints.kazarinov.react import ReportGenerator
from src.utils.jjson import j_loads, j_loads_ns, j_dumps

base_path = gs.path.external_data / 'kazarinov' / 'mexironim' / '24_11_24_05_29_40_543'
data:dict = j_loads(base_path / '202410262326_he.json')
html_file:Path = base_path / '202410262326_he.html' 
pdf_file:Path = base_path / '202410262326_he.pdf' 
r = ReportGenerator()
r.create_report(data, html_file, pdf_file)
```

## Внутренние функции

### `create_report`

**Назначение**:  Функция создания HTML-отчета из данных JSON.

**Параметры**:

- `data`: Данные в формате JSON, которые используются для генерации отчета.
- `html_file`: Путь к HTML-файлу, который будет создан.
- `pdf_file`: Путь к PDF-файлу, который будет создан.

**Возвращает**:

- None

**Как работает функция**:

- Считывает HTML-шаблон.
- Заменяет в шаблоне  метки с данными из JSON.
- Сохраняет полученный HTML-файл.
- Преобразует HTML-файл в PDF.

**Примеры**:

```python
from pathlib import Path
import header
from src import gs

from src.endpoints.kazarinov.react import ReportGenerator
from src.utils.jjson import j_loads, j_loads_ns, j_dumps

base_path = gs.path.external_data / 'kazarinov' / 'mexironim' / '24_11_24_05_29_40_543'
data:dict = j_loads(base_path / '202410262326_he.json')
html_file:Path = base_path / '202410262326_he.html' 
pdf_file:Path = base_path / '202410262326_he.pdf' 
r = ReportGenerator()
r.create_report(data, html_file, pdf_file)