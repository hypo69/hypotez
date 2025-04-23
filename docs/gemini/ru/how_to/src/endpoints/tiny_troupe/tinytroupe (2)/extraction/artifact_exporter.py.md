### **Как использовать блок кода `ArtifactExporter`**
=========================================================================================

Описание
-------------------------
Класс `ArtifactExporter` предназначен для экспорта артефактов (данных) из элементов `TinyTroupe` в различные форматы файлов, такие как JSON, TXT и DOCX. Это полезно, например, для создания синтетических данных из симуляций.

Шаги выполнения
-------------------------
1. **Инициализация `ArtifactExporter`**:
   - Создается экземпляр класса `ArtifactExporter` с указанием базовой папки для вывода файлов.
2. **Вызов метода `export`**:
   - Метод `export` принимает имя артефакта, данные для экспорта (словарь или строку), тип контента, формат контента (например, 'md', 'csv') и целевой формат (например, 'json', 'txt', 'docx').
   - Внутри метода происходит дедупликация (удаление лишних отступов) данных, очистка имени артефакта от недопустимых символов.
   - Вызывается метод `_compose_filepath` для формирования полного пути к файлу.
   - В зависимости от целевого формата вызывается соответствующий метод экспорта (`_export_as_json`, `_export_as_txt`, `_export_as_docx`).
3. **Метод `_compose_filepath`**:
   - Формирует путь к файлу на основе базовой папки, типа контента, имени артефакта и расширения файла.
   - Создает промежуточные директории, если они не существуют.
4. **Методы экспорта (`_export_as_json`, `_export_as_txt`, `_export_as_docx`)**:
   - Записывают данные в файл в соответствующем формате.
   - `_export_as_json` сохраняет словарь в формате JSON.
   - `_export_as_txt` записывает строку в текстовый файл.
   - `_export_as_docx` преобразует данные в формат DOCX с использованием библиотеки `pypandoc`.

Пример использования
-------------------------

```python
    from tinytroupe.extraction.artifact_exporter import ArtifactExporter

    # 1. Создание экземпляра класса ArtifactExporter
    base_output_folder = "output_folder"
    exporter = ArtifactExporter(base_output_folder)

    # 2. Пример данных для экспорта
    artifact_name = "example_artifact"
    artifact_data = {
        "content": "This is an example artifact.",
        "metadata": {"type": "example"}
    }
    content_type = "text"
    content_format = "md"
    target_format = "docx"

    # 3. Экспорт данных в файл
    exporter.export(artifact_name, artifact_data, content_type, content_format, target_format, verbose=True)