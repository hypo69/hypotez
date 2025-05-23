# Тесты для TinyTroupe: извлечение и нормализация

## Обзор

Этот файл содержит юнит-тесты для модуля `tinytroupe.extraction`. Тесты проверяют функциональность класса `ArtifactExporter` для экспорта артефактов в различных форматах (JSON, текст, DOCX), а также класс `Normalizer` для нормализации концептов.

## Тесты для класса `ArtifactExporter`

### `test_export_json(exporter)`

**Назначение**: Проверяет экспорт артефакта в формате JSON.

**Параметры**:

- `exporter`: Экземпляр класса `ArtifactExporter`.

**Как работает тест**:

1. Определяет данные артефакта в виде словаря.
2. Вызывает метод `export` класса `ArtifactExporter` для экспорта данных в формате JSON.
3. Проверяет существование экспортированного файла JSON.
4. Проверяет, соответствуют ли данные в экспортированном файле исходным данным.

**Примеры**:

```python
>>> exporter = ArtifactExporter(base_output_folder=EXPORT_BASE_FOLDER)
>>> test_export_json(exporter)
```

### `test_export_text(exporter)`

**Назначение**: Проверяет экспорт артефакта в формате текста.

**Параметры**:

- `exporter`: Экземпляр класса `ArtifactExporter`.

**Как работает тест**:

1. Определяет данные артефакта в виде строки.
2. Вызывает метод `export` класса `ArtifactExporter` для экспорта данных в формате TXT.
3. Проверяет существование экспортированного файла TXT.
4. Проверяет, соответствуют ли данные в экспортированном файле исходным данным.

**Примеры**:

```python
>>> exporter = ArtifactExporter(base_output_folder=EXPORT_BASE_FOLDER)
>>> test_export_text(exporter)
```

### `test_export_docx(exporter)`

**Назначение**: Проверяет экспорт артефакта в формате DOCX.

**Параметры**:

- `exporter`: Экземпляр класса `ArtifactExporter`.

**Как работает тест**:

1. Определяет данные артефакта в виде строки, содержащей форматированный текст Markdown.
2. Вызывает метод `export` класса `ArtifactExporter` для экспорта данных в формате DOCX.
3. Проверяет существование экспортированного файла DOCX.
4. Проверяет, содержит ли экспортированный файл DOCX некоторые из исходных данных.
5. Проверяет, не содержит ли экспортированный файл DOCX разметку Markdown.

**Примеры**:

```python
>>> exporter = ArtifactExporter(base_output_folder=EXPORT_BASE_FOLDER)
>>> test_export_docx(exporter)
```

## Тесты для класса `Normalizer`

### `test_normalizer()`

**Назначение**: Проверяет функциональность класса `Normalizer` для нормализации концептов.

**Параметры**:

- `concepts`: Список концептов для нормализации.
- `n`: Количество нормализованных элементов.

**Как работает тест**:

1. Определяет список концептов для нормализации.
2. Создает экземпляр класса `Normalizer`.
3. Проверяет, что количество нормализованных элементов равно заданному значению.
4. Генерирует несколько случайных подмножеств из исходного списка концептов.
5. Для каждого подмножества:
    - Вызывает метод `normalize` класса `Normalizer` для нормализации концептов.
    - Проверяет, что нормализованный концепт не равен `None`.
    - Проверяет, что длина нормализованного концепта равна длине исходного концепта.
    - Проверяет, что все элементы из нормализованного концепта находятся в ключах нормализующего словаря.
    - Проверяет, что размер кеша увеличился после нормализации нового концепта.
    - Проверяет, что размер кеша не уменьшился после нормализации нового концепта.

**Примеры**:

```python
>>> concepts = ['Antique Book Collection', 'Medical Research', ...]
>>> test_normalizer(concepts, n=10)
```