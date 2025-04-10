# Модуль для экспериментов с созданием PDF-отчета
## Обзор

Модуль `pricelist_generator.py` предназначен для экспериментов с созданием PDF-отчетов. В данном модуле используется класс `ReportGenerator` для генерации отчета на основе предоставленных данных в формате JSON.

## Подробней

Модуль `pricelist_generator.py` используется для генерации PDF отчетов на основе данных, полученных в формате JSON. Он использует класс `ReportGenerator` из модуля `src.endpoints.kazarinov.react` для создания отчета и сохранения его в HTML и PDF форматы. Расположение файла в проекте указывает на то, что это часть экспериментов, связанных с генерацией отчетов.

## Функции

### `ReportGenerator.create_report`

```python
def create_report(data: dict, html_file: Path, pdf_file: Path):
    """ Функция создает отчет в формате HTML и PDF на основе предоставленных данных.
    Args:
        data (dict): Словарь с данными для отчета.
        html_file (Path): Путь для сохранения HTML файла.
        pdf_file (Path): Путь для сохранения PDF файла.
    Raises:
        Exception: Если возникает ошибка при создании отчета.
    """
    ...
```

**Назначение**: Функция `create_report` создает отчет в форматах HTML и PDF на основе предоставленных данных.

**Параметры**:

- `data` (dict): Словарь, содержащий данные для отчета.
- `html_file` (Path): Путь к файлу, в который будет сохранен HTML-отчет.
- `pdf_file` (Path): Путь к файлу, в который будет сохранен PDF-отчет.

**Возвращает**:

- Ничего (None).

**Вызывает исключения**:

- `Exception`: Возникает, если в процессе создания отчета происходит ошибка.

**Как работает функция**:

1. Функция принимает словарь `data`, а также пути для сохранения HTML и PDF файлов.
2. Использует внутренние методы класса `ReportGenerator` для генерации HTML и PDF файлов на основе предоставленных данных.
3. Сохраняет HTML файл по указанному пути `html_file`.
4. Сохраняет PDF файл по указанному пути `pdf_file`.

**Примеры**:

```python
from pathlib import Path
from src.endpoints.kazarinov.react import ReportGenerator

# Пример использования
base_path = Path('./data')  # Укажите актуальный путь к директории с данными
data = {'ключ': 'значение'}  # Пример данных для отчета
html_file = base_path / 'report.html'
pdf_file = base_path / 'report.pdf'

r = ReportGenerator()
r.create_report(data, html_file, pdf_file)
```

## Переменные

- `base_path` (Path): Путь к директории с данными. Определен как `gs.path.external_data / 'kazarinov' / 'mexironim' / '24_11_24_05_29_40_543'`.
- `data` (dict): Данные для отчета, загруженные из JSON-файла. Определены как `j_loads(base_path / '202410262326_he.json')`.
- `html_file` (Path): Путь к HTML файлу отчета. Определен как `base_path / '202410262326_he.html'`.
- `pdf_file` (Path): Путь к PDF файлу отчета. Определен как `base_path / '202410262326_he.pdf'`.
- `r` (ReportGenerator): Инстанс класса `ReportGenerator`, используемый для создания отчета.