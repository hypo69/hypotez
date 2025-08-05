## Как использовать блок кода для создания отчетов
=========================================================================================

Описание
-------------------------
Этот блок кода генерирует два HTML- и PDF-файла, содержащих прайс-лист в двух языковых версиях: на иврите и русском. 

Шаги выполнения
-------------------------
1. **Загружает необходимые модули**: Импортирует библиотеки `pathlib`, `header`, `gs`, `ReportGenerator`, `ask_model`, необходимые для работы с файлами, генерирования прайс-листа и работы с AI-моделями. 
2. **Инициализирует генератор отчетов**: Создает экземпляр класса `ReportGenerator`, который будет использоваться для генерации отчетов.
3. **Определяет пути к файлам**:  Задает пути к HTML- и PDF-файлам для ивритской и русской версии прайс-листа, используя `test_directory` как базовую директорию.
4. **Создает отчеты**: Вызывает метод `create_report` класса `ReportGenerator` дважды, передавая в него данные о прайс-листе, язык и пути к выходным файлам. 
    -  `response_he_dict['he']`: Данные прайс-листа на иврите.
    -  `response_ru_dict['ru']`: Данные прайс-листа на русском.
    -  `'he'`: Язык для ивритской версии.
    -  `'ru'`: Язык для русской версии.
    -  `html_file_he`: Путь к HTML-файлу для ивритской версии.
    -  `pdf_file_he`: Путь к PDF-файлу для ивритской версии.
    -  `html_file_ru`: Путь к HTML-файлу для русской версии.
    -  `pdf_file_ru`: Путь к PDF-файлу для русской версии.

Пример использования
-------------------------

```python
from pathlib import Path

from src import gs
from src.endpoints.kazarinov.pricelist_generator import ReportGenerator
from src.endpoints.kazarinov.scenarios._experiments.ask_model import *

test_directory = Path('/path/to/test/directory')  # Замените на ваш реальный путь

# Предполагаем, что response_he_dict и response_ru_dict уже определены
response_he_dict = {'he': ...}
response_ru_dict = {'ru': ...} 

report_generator = ReportGenerator()
html_file_he:Path = test_directory / 'he.html'
pdf_file_he:Path = test_directory / 'he.pdf'
html_file_ru:Path = test_directory / 'ru.html'
pdf_file_ru:Path = test_directory / 'ru.pdf'

report_generator.create_report(response_he_dict['he'], 'he', html_file_he, pdf_file_he)
report_generator.create_report(response_ru_dict['ru'], 'ru', html_file_ru, pdf_file_ru)
```