# Модуль для работы с XML-файлами

## Обзор

Модуль `src.utils.xml` предоставляет функции для работы с XML-файлами, включая очистку от пустых элементов и форматирование вывода.

## Подробней

Модуль используется для:

- Очистки XML-строк от пустых элементов (например, тегов без содержимого).
- Форматирования XML-строк с использованием отступов для улучшения читаемости.
- Сохранения отформатированного XML-контента в файл.

## Функции

### `clean_empty_cdata`

**Назначение**: Очищает XML-строку от пустых элементов CDATA и ненужных пробелов.

**Параметры**:

- `xml_string` (str): Необработанный XML-контент.

**Возвращает**:

- `str`: Очищенный и отформатированный XML-контент.

**Пример**:

```python
xml_data = """<root><item>Value</item><item attr="test"></item></root>"""
cleaned_xml = clean_empty_cdata(xml_data)
print(cleaned_xml)
```

**Как работает**:

1. Парсит входную XML-строку с помощью `xml.etree.ElementTree.fromstring`.
2. Использует рекурсивную функцию `remove_empty_elements` для удаления пустых элементов из дерева XML.
3. Преобразует отформатированный XML-контент обратно в строку с помощью `xml.etree.ElementTree.tostring`.
4. Удаляет ненужные пробелы с помощью регулярного выражения `re.sub`.
5. Возвращает очищенный XML-контент.

### `save_xml`

**Назначение**: Сохраняет очищенный XML-контент из строки в файл с использованием отступов.

**Параметры**:

- `xml_string` (str): XML-контент в виде строки.
- `file_path` (str): Путь к выходному файлу.

**Возвращает**:

- `None`

**Пример**:

```python
xml_data = """<root><item>Value</item><item attr="test">Another</item></root>"""
save_xml(xml_data, "output.xml")
```

**Как работает**:

1. Очищает XML-контент с помощью `clean_empty_cdata`.
2. Парсит XML-строку с помощью `xml.etree.ElementTree.fromstring`.
3. Преобразует XML-контент в строку с отступами с помощью `minidom.parseString` и `toprettyxml`.
4. Записывает отформатированный XML-контент в файл с помощью `open` и `write`.

## Примеры

```python
# Пример 1: Очистка XML от пустых элементов и форматирование
xml_data = """<root><item>Value</item><item attr="test"></item></root>"""
cleaned_xml = clean_empty_cdata(xml_data)
print(cleaned_xml)

# Пример 2: Сохранение очищенного XML-контента в файл
xml_data = """<root><item>Value</item><item attr="test">Another</item></root>"""
save_xml(xml_data, "output.xml")
```