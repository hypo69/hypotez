Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода создает отчеты в формате HTML и PDF на двух языках (иврит и русский) на основе данных, полученных из словарей `response_he_dict` и `response_ru_dict`. Он использует класс `ReportGenerator` для генерации отчетов и сохраняет их в указанных файлах.

Шаги выполнения
-------------------------
1. **Инициализация `ReportGenerator`**: Создается экземпляр класса `ReportGenerator`, который отвечает за генерацию отчетов.
2. **Определение путей к файлам**: Указываются пути для сохранения HTML и PDF файлов для каждого языка.
3. **Создание отчета на иврите**:
   - Извлекаются данные для иврита из словаря `response_he_dict['he']`.
   - Вызывается метод `create_report` объекта `report_generator` с данными, языком ('he'), путем к HTML файлу (`html_file_he`) и путем к PDF файлу (`pdf_file_he`).
4. **Создание отчета на русском**:
   - Извлекаются данные для русского языка из словаря `response_ru_dict['ru']`.
   - Вызывается метод `create_report` объекта `report_generator` с данными, языком ('ru'), путем к HTML файлу (`html_file_ru`) и путем к PDF файлу (`pdf_file_ru`).

Пример использования
-------------------------

```python
from pathlib import Path

from src.endpoints.kazarinov.pricelist_generator import ReportGenerator

# Предположим, что test_directory, response_he_dict, response_ru_dict уже определены

report_generator = ReportGenerator()
html_file_he: Path = test_directory / 'he.html'
pdf_file_he: Path = test_directory / 'he.pdf'
html_file_ru: Path = test_directory / 'ru.html'
pdf_file_ru: Path = test_directory / 'ru.pdf'

# response_he_dict и response_ru_dict должны содержать данные для отчетов
# Например:
# response_he_dict = {'he': {'product1': 'data1', 'product2': 'data2'}}
# response_ru_dict = {'ru': {'product1': 'data1', 'product2': 'data2'}}

report_generator.create_report(response_he_dict['he'], 'he', html_file_he, pdf_file_he)
report_generator.create_report(response_ru_dict['ru'], 'ru', html_file_ru, pdf_file_ru)
```