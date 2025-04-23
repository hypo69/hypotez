# Модуль для проверки генерации прайслиста

## Обзор

Модуль предназначен для создания отчетов на основе данных, полученных из AI-моделей. Он использует класс `ReportGenerator` для создания HTML и PDF отчетов на разных языках.

## Подробнее

Модуль включает в себя создание отчетов на иврите (`he`) и русском (`ru`) языках, используя данные из словарей `response_he_dict` и `response_ru_dict` соответственно. HTML и PDF файлы сохраняются в каталоге `test_directory`.

## Переменные модуля

- `report_generator`: Экземпляр класса `ReportGenerator`, используемый для создания отчетов.
- `html_file_he`: Объект `Path`, представляющий путь к HTML файлу на иврите.
- `pdf_file_he`: Объект `Path`, представляющий путь к PDF файлу на иврите.
- `html_file_ru`: Объект `Path`, представляющий путь к HTML файлу на русском языке.
- `pdf_file_ru`: Объект `Path`, представляющий путь к PDF файлу на русском языке.

## Функции

### `ReportGenerator.create_report`

```python
def create_report(data: dict, lang: str, html_file: Path, pdf_file: Path) -> None:
    """Создает HTML и PDF отчет на основе предоставленных данных.

    Args:
        data (dict): Словарь с данными для отчета.
        lang (str): Язык отчета (`he` для иврита, `ru` для русского).
        html_file (Path): Путь для сохранения HTML файла.
        pdf_file (Path): Путь для сохранения PDF файла.

    Returns:
        None

    Raises:
        Exception: Если возникает ошибка при создании отчета.

    Example:
        >>> report_generator = ReportGenerator()
        >>> data = {'ключ': 'значение'}
        >>> lang = 'ru'
        >>> html_file = Path('ru.html')
        >>> pdf_file = Path('ru.pdf')
        >>> report_generator.create_report(data, lang, html_file, pdf_file)
    """
    ...
```

**Назначение**: Создает HTML и PDF отчет на основе предоставленных данных.

**Параметры**:
- `data` (dict): Словарь с данными для отчета.
- `lang` (str): Язык отчета (`he` для иврита, `ru` для русского).
- `html_file` (Path): Путь для сохранения HTML файла.
- `pdf_file` (Path): Путь для сохранения PDF файла.

**Возвращает**:
- `None`: Функция ничего не возвращает.

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при создании отчета.

**Как работает функция**:
- Функция принимает данные, язык и пути для сохранения HTML и PDF файлов.
- Затем она вызывает метод `create_report` у объекта `report_generator` для создания отчетов.
- Если возникает ошибка, она логируется с использованием `logger.error`.

**Примеры**:
```python
report_generator = ReportGenerator()
data = {'ключ': 'значение'}
lang = 'ru'
html_file = Path('ru.html')
pdf_file = Path('ru.pdf')
report_generator.create_report(data, lang, html_file, pdf_file)
```

## Использование в коде

```python
report_generator.create_report(response_he_dict['he'], 'he', html_file_he, pdf_file_he)
report_generator.create_report(response_ru_dict['ru'], 'ru', html_file_ru, pdf_file_ru)
```

В данном коде функция `create_report` вызывается дважды:
1. Для создания отчета на иврите (`he`) с использованием данных из `response_he_dict['he']`. HTML файл сохраняется по пути `html_file_he`, PDF файл - по пути `pdf_file_he`.
2. Для создания отчета на русском (`ru`) с использованием данных из `response_ru_dict['ru']`. HTML файл сохраняется по пути `html_file_ru`, PDF файл - по пути `pdf_file_ru`.