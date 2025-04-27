# Модуль для тестирования экспорта артефактов и нормализации понятий 

## Обзор

Этот модуль содержит набор юнит-тестов для функций экспорта артефактов и нормализации понятий из модуля `tinytroupe`. Он проверяет корректность работы функций `ArtifactExporter` и `Normalizer`.

## Подробности

Этот модуль находится в  `hypotez/src/endpoints/tiny_troupe/tests/unit/test_extraction.py` и содержит несколько функций, которые тестируют функциональность экспорта артефактов в разных форматах (JSON, текст, docx) и нормализации понятий с помощью класса `Normalizer`.

## Классы

### `ArtifactExporter`

**Описание**: Класс `ArtifactExporter` используется для экспорта артефактов в разных форматах (JSON, текст, docx).

**Атрибуты**:

- `base_output_folder` (str): Базовая директория для экспорта артефактов.

**Методы**:

- `export(self, name: str, data: Any, content_type: str, content_format: str = None, target_format: str = "json") -> None`: Экспортирует артефакт в указанном формате.

#### Параметры:

- `name` (str): Имя артефакта.
- `data` (Any): Данные, которые необходимо экспортировать.
- `content_type` (str): Тип содержимого (например, 'record', 'text', 'Document').
- `content_format` (str, optional): Формат содержимого (например, 'markdown', 'json'). По умолчанию `None`.
- `target_format` (str, optional): Формат экспорта (например, 'json', 'txt', 'docx'). По умолчанию 'json'.

#### Примеры

```python
# Создание экземпляра класса ArtifactExporter
exporter = ArtifactExporter(base_output_folder=EXPORT_BASE_FOLDER)

# Экспорт данных в формате JSON
artifact_data = {"name": "John Doe", "age": 30, "occupation": "Engineer", "content": "This is a sample JSON data."}
exporter.export("test_artifact", artifact_data, content_type="record", target_format="json")

# Экспорт данных в формате текста
artifact_data = "This is a sample text."
exporter.export("test_artifact", artifact_data, content_type="text", target_format="txt")

# Экспорт данных в формате docx
artifact_data = """
# This is a sample markdown text
This is a **bold** text.
This is an *italic* text.
This is a [link](https://www.example.com).
"""
exporter.export("test_artifact", artifact_data, content_type="Document", content_format="markdown", target_format="docx")
```

### `Normalizer`

**Описание**: Класс `Normalizer` используется для нормализации набора понятий.

**Атрибуты**:

- `concepts` (list): Список понятий, которые необходимо нормализовать.
- `n` (int): Число элементов, которые необходимо нормализовать.
- `verbose` (bool): Определяет, нужно ли выводить информацию о процессе нормализации.
- `normalized_elements` (list): Список нормализованных элементов.
- `normalizing_map` (dict): Словарь, хранящий информацию о нормализованных элементах.

**Методы**:

- `normalize(self, concepts: list) -> list`: Нормализует список понятий и возвращает список нормализованных элементов.

#### Параметры:

- `concepts` (list): Список понятий, которые необходимо нормализовать.

#### Возвращает:

- `list`: Список нормализованных элементов.

#### Примеры

```python
# Создание экземпляра класса Normalizer
concepts = ['Antique Book Collection', 'Medical Research', 'Electrical safety', 'Reading', 'Technology', 'Entrepreneurship', 'Multimedia Teaching Tools', 'Photography', 
'Smart home technology', 'Gardening', 'Travel', 'Outdoors', 'Hiking', 'Yoga', 'Finance', 'Health and wellness', 'Sustainable Living', 'Barista Skills', 'Oral health education',
'Patient care', 'Professional Development', 'Project safety', 'Coffee', 'Literature', 'Continuous learning', 'Model trains', 'Education', 'Mental and Physical Balance', 'Kayaking',
'Social Justice', 'National Park Exploration', 'Outdoor activities', 'Dental technology', 'Teaching electrical skills', 'Volunteering', 'Cooking', 'Industry trends', 
'Energy-efficient systems', 'Mentoring', 'Empathetic communication', 'Medical Technology', 'Historical Research', 'Public Speaking', 'Museum Volunteering', 'Conflict Resolution']

normalizer = Normalizer(concepts, n=10, verbose=True)

# Нормализация списка понятий
normalized_concepts = normalizer.normalize(concepts)

# Вывод нормализованных понятий
print(f"Normalized concepts: {normalized_concepts}")
```

## Функции

### `test_export_json(exporter)`

**Цель**: Проверяет корректность экспорта артефакта в формате JSON.

**Параметры**:

- `exporter` (`ArtifactExporter`): Экземпляр класса `ArtifactExporter`.

**Возвращает**:

- `None`

**Пример**:

```python
# Создание экземпляра класса ArtifactExporter
exporter = ArtifactExporter(base_output_folder=EXPORT_BASE_FOLDER)

# Вызов тестовой функции
test_export_json(exporter)
```

### `test_export_text(exporter)`

**Цель**: Проверяет корректность экспорта артефакта в формате текста.

**Параметры**:

- `exporter` (`ArtifactExporter`): Экземпляр класса `ArtifactExporter`.

**Возвращает**:

- `None`

**Пример**:

```python
# Создание экземпляра класса ArtifactExporter
exporter = ArtifactExporter(base_output_folder=EXPORT_BASE_FOLDER)

# Вызов тестовой функции
test_export_text(exporter)
```

### `test_export_docx(exporter)`

**Цель**: Проверяет корректность экспорта артефакта в формате docx.

**Параметры**:

- `exporter` (`ArtifactExporter`): Экземпляр класса `ArtifactExporter`.

**Возвращает**:

- `None`

**Пример**:

```python
# Создание экземпляра класса ArtifactExporter
exporter = ArtifactExporter(base_output_folder=EXPORT_BASE_FOLDER)

# Вызов тестовой функции
test_export_docx(exporter)
```

### `test_normalizer()`

**Цель**: Проверяет корректность работы класса `Normalizer`.

**Параметры**:

- `None`

**Возвращает**:

- `None`

**Пример**:

```python
# Вызов тестовой функции
test_normalizer()
```

## Внутренние функции

### `inner_function()`

**Описание**: Не используется в этом модуле.

## Примеры

Примеры использования функций и классов в этом модуле показаны выше в описании каждого из них.

## Дополнительная информация

- Все тесты в этом модуле используют стандартную библиотеку `pytest` для тестирования кода.
- Модуль использует `logger` из `src.logger` для ведения журнала событий.
- Все тесты проводятся на тестовых данных, определенных в этом модуле.
- Перед запуском тестов необходимо убедиться, что каталог для экспорта артефактов (`EXPORT_BASE_FOLDER`) доступен для записи.

## Улучшенный код

```python
import pytest
import os
import json
import random

import logging
logger = logging.getLogger("tinytroupe")

import sys
sys.path.append('../../tinytroupe/')
sys.path.append('../../')
sys.path.append('..')

from testing_utils import *
from tinytroupe.extraction import ArtifactExporter, Normalizer
from tinytroupe import utils

@pytest.fixture
def exporter():
    return ArtifactExporter(base_output_folder=EXPORT_BASE_FOLDER)

def test_export_json(exporter):
    # Определяем данные для артефакта
    artifact_data = {
        "name": "John Doe",
        "age": 30,
        "occupation": "Engineer",
        "content": "This is a sample JSON data."
    }
    
    # Экспортируем данные для артефакта в формате JSON
    exporter.export("test_artifact", artifact_data, content_type="record", target_format="json")
    
    # Проверяем, что файл JSON был экспортирован правильно
    assert os.path.exists(f"{EXPORT_BASE_FOLDER}/record/test_artifact.json"), "Файл JSON должен быть экспортирован."

    # Проверяем, что файл содержит правильные данные
    with open(f"{EXPORT_BASE_FOLDER}/record/test_artifact.json", "r") as f:
        exported_data = json.load(f)
        assert exported_data == artifact_data, "Экспортированные данные JSON должны совпадать с исходными данными."

def test_export_text(exporter):
    # Определяем данные для артефакта
    artifact_data = "This is a sample text."
    
    # Экспортируем данные для артефакта в формате текста
    exporter.export("test_artifact", artifact_data, content_type="text", target_format="txt")
    
    # Проверяем, что текстовый файл был экспортирован правильно
    assert os.path.exists(f"{EXPORT_BASE_FOLDER}/text/test_artifact.txt"), "Текстовый файл должен быть экспортирован."

    # Проверяем, что файл содержит правильные данные
    with open(f"{EXPORT_BASE_FOLDER}/text/test_artifact.txt", "r") as f:
        exported_data = f.read()
        assert exported_data == artifact_data, "Экспортированные текстовые данные должны совпадать с исходными данными."

def test_export_docx(exporter):
    # Определяем данные для артефакта. Включаем форматирование Markdown для проверки его сохранения.
    artifact_data ="""
    # This is a sample markdown text
    This is a **bold** text.
    This is an *italic* text.
    This is a [link](https://www.example.com).
    """
    
    # Экспортируем данные для артефакта в файл docx
    exporter.export("test_artifact", artifact_data, content_type="Document", content_format="markdown", target_format="docx")
    
    # Проверяем, что файл docx был экспортирован правильно
    assert os.path.exists(f"{EXPORT_BASE_FOLDER}/Document/test_artifact.docx"), "Файл docx должен быть экспортирован."

    # Проверяем, что файл содержит правильные данные
    from docx import Document
    doc = Document(f"{EXPORT_BASE_FOLDER}/Document/test_artifact.docx")
    exported_data = ""
    for para in doc.paragraphs:
        exported_data += para.text

    assert "This is a sample markdown text" in exported_data, "Экспортированные данные docx должны содержать часть исходного контента."
    assert "#" not in exported_data, "Экспортированные данные docx не должны содержать Markdown."


def test_normalizer():
    # Определяем понятия для нормализации
    concepts = ['Antique Book Collection', 'Medical Research', 'Electrical safety', 'Reading', 'Technology', 'Entrepreneurship', 'Multimedia Teaching Tools', 'Photography', 
     'Smart home technology', 'Gardening', 'Travel', 'Outdoors', 'Hiking', 'Yoga', 'Finance', 'Health and wellness', 'Sustainable Living', 'Barista Skills', 'Oral health education',
     'Patient care', 'Professional Development', 'Project safety', 'Coffee', 'Literature', 'Continuous learning', 'Model trains', 'Education', 'Mental and Physical Balance', 'Kayaking',
     'Social Justice', 'National Park Exploration', 'Outdoor activities', 'Dental technology', 'Teaching electrical skills', 'Volunteering', 'Cooking', 'Industry trends', 
     'Energy-efficient systems', 'Mentoring', 'Empathetic communication', 'Medical Technology', 'Historical Research', 'Public Speaking', 'Museum Volunteering', 'Conflict Resolution']
    
    unique_concepts = list(set(concepts))

    normalizer = Normalizer(concepts, n=10, verbose=True)

    assert len(normalizer.normalized_elements) == 10, "Количество нормализованных элементов должно быть равно указанному значению."

    # Выбираем 5 случайных элементов из понятий с помощью стандартных методов Python
    random_concepts_buckets = [random.sample(concepts, 15), random.sample(concepts, 15), random.sample(concepts, 15), random.sample(concepts, 15), random.sample(concepts, 15)]

    assert len(normalizer.normalizing_map.keys()) == 0, "Карта нормализации должна быть пуста в начале."
    for bucket in random_concepts_buckets:
        init_cache_size = len(normalizer.normalizing_map.keys())
        
        normalized_concept = normalizer.normalize(bucket)
        assert normalized_concept is not None, "Нормализованное понятие не должно быть None."
        logger.debug(f"Нормализованное понятие: {bucket} -> {normalized_concept}")
        print(f"Нормализованное понятие: {bucket} -> {normalized_concept}")

        next_cache_size = len(normalizer.normalizing_map.keys())

        # Проверяем, что длины одинаковые
        assert len(normalized_concept) == len(bucket), "Нормализованное понятие должно иметь ту же длину, что и входное понятие."

        # Убеждаемся, что все элементы из нормализованных понятий находятся в ключах карты нормализации
        for element in bucket:
            assert element in normalizer.normalizing_map.keys(), f"{element} должен быть в ключах карты нормализации."

        assert next_cache_size > 0, "Размер кэша должен быть больше 0 после нормализации нового понятия."
        assert next_cache_size >= init_cache_size, "Размер кэша не должен уменьшаться после нормализации нового понятия."