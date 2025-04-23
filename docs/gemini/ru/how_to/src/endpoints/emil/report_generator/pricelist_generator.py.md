### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Блок кода содержит класс `ReportGenerator`, который используется для генерации HTML и PDF отчетов на основе данных из JSON. Он загружает данные, применяет их к шаблону HTML, сохраняет HTML в файл и затем конвертирует HTML в PDF.

Шаги выполнения
-------------------------
1. **Инициализация класса `ReportGenerator`**:
   - Создается экземпляр класса `ReportGenerator`, который инициализирует окружение Jinja2 для работы с шаблонами.

2. **Генерация HTML-контента**:
   - Метод `generate_html` принимает данные (`data`) и язык (`lang`) в качестве аргументов.
   - Определяется имя шаблона в зависимости от языка (русский или иврит).
   - Читается содержимое шаблона из файла.
   - Создается объект шаблона Jinja2 и выполняется рендеринг HTML-контента на основе переданных данных.

3. **Создание отчета**:
   - Метод `create_report` принимает данные (`data`), язык (`lang`), путь к HTML-файлу (`html_file`) и путь к PDF-файлу (`pdf_file`) в качестве аргументов.
   - Создается словарь `service_dict`, содержащий информацию о сервисе (название и описание) на нужном языке, а также случайное изображение.
   - `service_dict` добавляется в список `products` в переданных данных (`data`).
   - Генерируется HTML-контент с использованием метода `generate_html`.
   - HTML-контент записывается в файл.
   - Инициализируется класс `PDFUtils`.
   - HTML-контент преобразуется в PDF и сохраняется в файл. Если преобразование не удалось, логируется ошибка.

4. **Главная функция `main`**:
   - Функция `main` принимает название "мехирона" (`mexiron`) и язык (`lang`) в качестве аргументов.
   - Формируется путь к данным JSON, HTML-файлу и PDF-файлу.
   - Загружаются данные из JSON-файла.
   - Создается экземпляр класса `ReportGenerator`.
   - Запускается асинхронная операция создания отчета с использованием `asyncio.run`.

5. **Запуск при исполнении файла**:
   - Если скрипт запускается как главный, вызывается функция `main` с предопределенными значениями `mexiron` и `lang`.

Пример использования
-------------------------

```python
import asyncio
from pathlib import Path
from src.endpoints.emil.report_generator.pricelist_generator import ReportGenerator
from src.utils.jjson import j_loads
from src import gs

async def main():
    # Пример использования ReportGenerator
    mexiron: str = '24_12_01_03_18_24_269'
    lang: str = 'ru'
    base_path: Path = gs.path.external_storage / 'kazarinov' / 'mexironim' / mexiron
    data: dict = j_loads(base_path / f'{lang}.json')
    html_file: Path = base_path / f'{mexiron}_{lang}.html'
    pdf_file: Path = base_path / f'{mexiron}_{lang}.pdf'
    r = ReportGenerator()
    result = await r.create_report(data, lang, html_file, pdf_file)
    if result:
        print(f"Отчет успешно создан: {pdf_file}")
    else:
        print("Не удалось создать отчет.")

if __name__ == "__main__":
    asyncio.run(main())