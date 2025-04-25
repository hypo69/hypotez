## Как использовать класс `ArtifactExporter` для экспорта артефактов
=========================================================================================

Описание
-------------------------
Класс `ArtifactExporter` позволяет экспортировать артефакты в различных форматах (JSON, текстовый файл, DOCX). 

Шаги выполнения
-------------------------
1. **Создай экземпляр класса `ArtifactExporter`**: 
    - Задай базовый каталог для экспорта (`base_output_folder`).
2. **Вызови метод `export`**:
    - Передай имя артефакта (`name`).
    - Передай данные артефакта (`data`).
    - Задай тип контента (`content_type`).
    - Задай формат контента (`content_format`, если применимо).
    - Задай целевой формат (`target_format`).
3. **Проверь экспорт**:
    - Проверь наличие экспортированного файла в соответствующем каталоге.
    - Проверь содержимое файла, чтобы убедиться, что данные экспортированы корректно.

Пример использования
-------------------------

```python
from tinytroupe.extraction import ArtifactExporter

# Создаем экземпляр класса ArtifactExporter
exporter = ArtifactExporter(base_output_folder="path/to/output/folder")

# Экспортируем данные в формате JSON
artifact_data = {"name": "John Doe", "age": 30}
exporter.export("test_artifact", artifact_data, content_type="record", target_format="json")

# Экспортируем текст в формате TXT
artifact_data = "This is a sample text."
exporter.export("test_artifact", artifact_data, content_type="text", target_format="txt")

# Экспортируем Markdown в формате DOCX
artifact_data = """
# This is a sample markdown text
This is a **bold** text.
This is an *italic* text.
This is a [link](https://www.example.com).
"""
exporter.export("test_artifact", artifact_data, content_type="Document", content_format="markdown", target_format="docx")
```

## Как использовать класс `Normalizer` для нормализации концепций
=========================================================================================

Описание
-------------------------
Класс `Normalizer` нормализует концепции (например, названия тем или областей знаний) до заданного количества уникальных элементов.

Шаги выполнения
-------------------------
1. **Создай экземпляр класса `Normalizer`**:
    - Передай список концепций (`concepts`).
    - Задай количество уникальных элементов для нормализации (`n`).
2. **Вызови метод `normalize`**:
    - Передай список концепций для нормализации.
3. **Получи результат**:
    - Метод `normalize` возвращает список нормализованных концепций.

Пример использования
-------------------------

```python
from tinytroupe.extraction import Normalizer

# Создаем список концепций
concepts = [
    'Antique Book Collection', 'Medical Research', 'Electrical safety', 'Reading', 'Technology',
    'Entrepreneurship', 'Multimedia Teaching Tools', 'Photography', 'Smart home technology',
    'Gardening', 'Travel', 'Outdoors', 'Hiking', 'Yoga', 'Finance', 'Health and wellness',
    'Sustainable Living', 'Barista Skills', 'Oral health education', 'Patient care',
    'Professional Development', 'Project safety', 'Coffee', 'Literature', 'Continuous learning',
    'Model trains', 'Education', 'Mental and Physical Balance', 'Kayaking', 'Social Justice',
    'National Park Exploration', 'Outdoor activities', 'Dental technology', 'Teaching electrical skills',
    'Volunteering', 'Cooking', 'Industry trends', 'Energy-efficient systems', 'Mentoring',
    'Empathetic communication', 'Medical Technology', 'Historical Research', 'Public Speaking',
    'Museum Volunteering', 'Conflict Resolution'
]

# Создаем экземпляр класса Normalizer
normalizer = Normalizer(concepts, n=10, verbose=True)

# Нормализуем список концепций
normalized_concepts = normalizer.normalize(concepts)

# Выводим нормализованные концепции
print(f"Normalized concepts: {normalized_concepts}")
```