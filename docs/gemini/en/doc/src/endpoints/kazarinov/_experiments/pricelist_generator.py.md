# Модуль src.endpoints.kazarinov._experiments.pricelist_generator

## Обзор

Модуль содержит код, который генерирует PDF-отчет из данных в формате JSON. Отчет создается на основе HTML-шаблона.

## Детали

Модуль использует модуль `ReportGenerator` для создания отчета. 

- `ReportGenerator` - класс, который отвечает за создание отчета. Он принимает данные в формате JSON, HTML-шаблон и путь к выходному PDF-файлу. 

- `j_loads` - функция для чтения JSON-файлов.
- `j_dumps` - функция для записи данных в JSON-формат.

##  Классы

### `ReportGenerator`
**Описание**:  Класс для создания отчета. 

**Методы**:

- `create_report`: Создает отчет из данных в формате JSON, HTML-шаблона и пути к выходному PDF-файлу.

## Функции

### `create_report`

**Purpose**:  Создает PDF-отчет на основе данных в формате JSON и HTML-шаблона.

**Parameters**:

- `data`: Данные в формате JSON.
- `html_file`: Путь к HTML-шаблону.
- `pdf_file`: Путь к выходному PDF-файлу.

**Returns**:

- `None`

**How the Function Works**:

1. Загружает данные из JSON-файла.
2. Создает HTML-шаблон из полученных данных.
3. Преобразует HTML-шаблон в PDF-файл.

**Examples**:

```python
from src.endpoints.kazarinov.react import ReportGenerator
from src.utils.jjson import j_loads, j_loads_ns, j_dumps

base_path = gs.path.external_data / 'kazarinov' / 'mexironim' / '24_11_24_05_29_40_543'
data:dict = j_loads(base_path / '202410262326_he.json')
html_file:Path = base_path / '202410262326_he.html'
pdf_file:Path = base_path / '202410262326_he.pdf'
r = ReportGenerator()
r.create_report(data, html_file, pdf_file)
```

## Parameter Details

- `data` (dict): Данные в формате JSON, которые будут использоваться для генерации отчета.

- `html_file` (Path): Путь к HTML-файлу, который используется как шаблон для генерации отчета.

- `pdf_file` (Path): Путь к PDF-файлу, в который будет сохранен сгенерированный отчет.

##  Examples

```python
from src.endpoints.kazarinov.react import ReportGenerator
from src.utils.jjson import j_loads, j_loads_ns, j_dumps

base_path = gs.path.external_data / 'kazarinov' / 'mexironim' / '24_11_24_05_29_40_543'
data:dict = j_loads(base_path / '202410262326_he.json')
html_file:Path = base_path / '202410262326_he.html'
pdf_file:Path = base_path / '202410262326_he.pdf'
r = ReportGenerator()
r.create_report(data, html_file, pdf_file)

```