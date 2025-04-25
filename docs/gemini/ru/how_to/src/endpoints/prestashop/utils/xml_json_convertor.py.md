## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода предоставляет функцию `presta_fields_to_xml`, которая преобразует словарь с данными Prestashop в XML-строку с фиксированным корневым элементом "prestashop". 

Шаги выполнения
-------------------------
1. **Функция `presta_fields_to_xml` принимает словарь `presta_fields_dict` в качестве аргумента.** Этот словарь должен содержать данные Prestashop без ключа "prestashop". 
2. **Функция определяет корневой элемент "prestashop" и создает дочерний элемент с именем первого ключа в словаре `presta_fields_dict` (например, "product", "category").**
3. **Функция `build_xml_element` рекурсивно строит XML-элементы из данных словаря `presta_fields_dict`.** Она обрабатывает атрибуты, текстовые значения и вложенные словари и списки.
4. **После построения XML-дерева функция преобразует его в строку с кодировкой UTF-8.**

Пример использования
-------------------------

```python
# Пример JSON 
"""
json_data = {
    "product": {
        "name": {
            "language": [
                {
                    "@id": "1",
                    "#text": "Test Product"
                },
                {
                    "@id": "2",
                    "#text": "Test Product"
                },
                {
                    "@id": "3",
                    "#text": "Test Product"
                }
            ]
        },
        "price": "10.00",
        "id_tax_rules_group": "13",
        "id_category_default": "2"
    }
}

xml_output = presta_fields_to_xml(json_data)
print(xml_output)
"""
```

В этом примере `json_data` содержит словарь с информацией о товаре. Функция `presta_fields_to_xml` преобразует этот словарь в XML-строку с корневым элементом "prestashop".

**Результат:**

```xml
<prestashop>
  <product>
    <name>
      <language id="1">Test Product</language>
      <language id="2">Test Product</language>
      <language id="3">Test Product</language>
    </name>
    <price>10.00</price>
    <id_tax_rules_group>13</id_tax_rules_group>
    <id_category_default>2</id_category_default>
  </product>
</prestashop>
```