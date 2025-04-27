## Как использовать класс ArtifactExporter
=========================================================================================

Описание
-------------------------
Класс `ArtifactExporter` предназначен для экспорта артефактов из элементов TinyTroupe. Артефакт представляет собой файл с данными, полученными из симуляции TinyTroupe. Класс позволяет экспортировать различные типы данных в различные форматы.

Шаги выполнения
-------------------------
1. **Создание экземпляра класса:** Создайте экземпляр класса `ArtifactExporter`, передав ему базовый путь для сохранения экспортируемых файлов.
2. **Вызов метода `export`:** Вызовите метод `export` для экспорта артефакта. Передайте в качестве аргументов:
    - `artifact_name`: Имя артефакта.
    - `artifact_data`: Данные, которые нужно экспортировать. 
        - Если `artifact_data` - это словарь, он будет сохранен как JSON.
        - Если `artifact_data` - это строка, она будет сохранена как есть.
    - `content_type`: Тип содержимого артефакта.
    - `content_format`: Формат содержимого артефакта (например, md, csv, etc).
    - `target_format`: Формат, в который нужно экспортировать артефакт (например, json, txt, docx, etc).
    - `verbose`: Флаг, определяющий, нужно ли выводить сообщения о ходе выполнения.

Пример использования
-------------------------

```python
from tinytroupe.extraction import ArtifactExporter

# Создаем экземпляр класса ArtifactExporter
exporter = ArtifactExporter(base_output_folder="artifacts")

# Экспортируем данные в JSON файл
artifact_data = {
    "content": "Это пример текста для экспорта.",
    "meta": {"author": "John Doe"}
}
exporter.export(
    artifact_name="my_artifact",
    artifact_data=artifact_data,
    content_type="text",
    target_format="json"
)

# Экспортируем данные в текстовый файл
artifact_data = "Это текст для экспорта."
exporter.export(
    artifact_name="my_text_artifact",
    artifact_data=artifact_data,
    content_type="text",
    target_format="txt"
)

# Экспортируем данные в DOCX файл
artifact_data = "# Заголовок документа\n\nЭто пример текста в Markdown формате."
exporter.export(
    artifact_name="my_docx_artifact",
    artifact_data=artifact_data,
    content_type="text",
    content_format="md",
    target_format="docx"
)
```