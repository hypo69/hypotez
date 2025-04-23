### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код содержит набор тестов для проверки функциональности модулей `ArtifactExporter` и `Normalizer` из библиотеки `tinytroupe`. `ArtifactExporter` используется для экспорта данных в различных форматах (JSON, текст, DOCX), а `Normalizer` — для нормализации текстовых концепций. Тесты проверяют, что данные экспортируются и нормализуются корректно.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются модули `pytest`, `os`, `json`, `random`, `logging` и классы `ArtifactExporter`, `Normalizer` из `tinytroupe`, а также вспомогательные функции из `testing_utils`.
2. **Определение фикстуры `exporter`**: Фикстура `exporter` инициализирует экземпляр класса `ArtifactExporter` с базовой папкой для экспорта.
3. **Тест экспорта в JSON (`test_export_json`)**:
    - Определяются данные артефакта в формате словаря.
    - Вызывается метод `exporter.export` для экспорта данных в формате JSON.
    - Проверяется, что файл JSON был создан в ожидаемой директории.
    - Проверяется, что экспортированные данные соответствуют исходным.
4. **Тест экспорта в текст (`test_export_text`)**:
    - Определяются текстовые данные артефакта.
    - Вызывается метод `exporter.export` для экспорта данных в текстовый файл.
    - Проверяется, что текстовый файл был создан в ожидаемой директории.
    - Проверяется, что экспортированные данные соответствуют исходным.
5. **Тест экспорта в DOCX (`test_export_docx`)**:
    - Определяются данные артефакта в формате Markdown.
    - Вызывается метод `exporter.export` для экспорта данных в формат DOCX.
    - Проверяется, что файл DOCX был создан в ожидаемой директории.
    - Проверяется, что экспортированные данные содержат часть исходного контента, но без Markdown-разметки.
6. **Тест нормализации (`test_normalizer`)**:
    - Определяется список концепций для нормализации.
    - Инициализируется экземпляр класса `Normalizer` с заданным количеством нормализованных элементов.
    - Проверяется, что количество нормализованных элементов соответствует ожидаемому значению.
    - Создаются случайные наборы концепций.
    - Для каждого набора концепций вызывается метод `normalizer.normalize`.
    - Проверяется, что метод возвращает непустой результат.
    - Проверяется, что длина нормализованного списка совпадает с длиной исходного списка.
    - Проверяется, что все элементы исходного списка присутствуют в карте нормализации.
    - Проверяется, что размер кеша увеличивается после каждой нормализации.

Пример использования
-------------------------

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
    # Define the artifact data
    artifact_data = {
        "name": "John Doe",
        "age": 30,
        "occupation": "Engineer",
        "content": "This is a sample JSON data."
    }
    
    # Export the artifact data as JSON
    exporter.export("test_artifact", artifact_data, content_type="record", target_format="json")
    
    # Проверка, что JSON файл был экспортирован
    assert os.path.exists(f"{EXPORT_BASE_FOLDER}/record/test_artifact.json"), "The JSON file should have been exported."

    # Проверка, что данные соответствуют исходным
    with open(f"{EXPORT_BASE_FOLDER}/record/test_artifact.json", "r") as f:
        exported_data = json.load(f)
        assert exported_data == artifact_data, "The exported JSON data should match the original data."