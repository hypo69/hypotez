## Как использовать модуль `src.utils.xml`

=========================================================================================

### Описание

-------------------------

Модуль `src.utils.xml` предоставляет функции для очистки и форматирования XML-данных.

### Шаги выполнения

-------------------------

1. **Очистка пустых секций CDATA и ненужных пробелов**: Функция `clean_empty_cdata` принимает строку XML-кода, удаляет пустые секции CDATA и оптимизирует пробелы.
2. **Сохранение отформатированного XML в файл**: Функция `save_xml` принимает строку XML-кода и путь к выходному файлу. Она очищает XML от пустых элементов, форматирует его с отступами и записывает результат в файл.

### Пример использования

-------------------------

```python
    # Пример использования
    xml_data = """<root><item>Value</item><item attr="test">Another</item></root>"""
    save_xml(xml_data, "output.xml")
```

В этом примере:

1. Создается строка `xml_data`, содержащая простой XML-код.
2. Используется функция `save_xml` для сохранения `xml_data` в файл "output.xml".
3. Файл "output.xml" будет содержать отформатированный XML-код с правильными отступами и без пустых секций CDATA.