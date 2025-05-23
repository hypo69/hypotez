# Модуль examples.py

## Обзор

Модуль содержит примеры использования библиотеки `tinytroupe` для создания и определения характеристик виртуальных личностей (агентов). Каждый пример демонстрирует создание персонажа с уникальными атрибутами, такими как возраст, национальность, профессия, интересы и навыки.

## Подробней

Модуль демонстрирует, как можно создать разнообразных персонажей, используя класс `TinyPerson` из библиотеки `tinytroupe`. Примеры включают архитектора, специалиста по данным, врача и лингвиста. Для каждого персонажа определены различные характеристики, такие как личностные качества, профессиональные и личные интересы, навыки и отношения с другими персонажами. Это позволяет создавать детальные и правдоподобные виртуальные личности, которые могут быть использованы в различных приложениях, таких как игры, симуляции и интерактивные истории.

## Функции

### `create_oscar_the_architect`

**Назначение**: Создает и определяет характеристики виртуальной личности по имени Оскар, который является архитектором.

**Параметры**:
- Нет параметров.

**Возвращает**:
- `oscar` (TinyPerson): Объект класса `TinyPerson`, представляющий Оскара-архитектора с определенными атрибутами.

**Как работает функция**:

1. **Создание персонажа**: Создается экземпляр класса `TinyPerson` с именем "Oscar".
2. **Определение атрибутов**: Определяются основные атрибуты Оскара, такие как возраст, национальность и профессия.
3. **Описание рутины**: Добавляется описание ежедневной рутины Оскара.
4. **Описание профессии**: Предоставляется подробное описание работы Оскара в компании "Awesome Inc." в качестве архитектора.
5. **Определение черт личности**: Определяются несколько черт личности Оскара.
6. **Определение профессиональных интересов**: Указываются профессиональные интересы Оскара.
7. **Определение личных интересов**: Указываются личные интересы Оскара.
8. **Определение навыков**: Перечисляются навыки, которыми владеет Оскар.
9. **Определение отношений**: Описываются отношения Оскара с другими персонажами.

**Примеры**:

```python
oscar = create_oscar_the_architect()
print(oscar.name)  # Вывод: Oscar
print(oscar.age)  # Вывод: 30
print(oscar.occupation)  # Вывод: Architect
```

### `create_lisa_the_data_scientist`

**Назначение**: Создает и определяет характеристики виртуальной личности по имени Лиза, которая является специалистом по данным.

**Параметры**:
- Нет параметров.

**Возвращает**:
- `lisa` (TinyPerson): Объект класса `TinyPerson`, представляющий Лизу-специалиста по данным с определенными атрибутами.

**Как работает функция**:

1. **Создание персонажа**: Создается экземпляр класса `TinyPerson` с именем "Lisa".
2. **Определение атрибутов**: Определяются основные атрибуты Лизы, такие как возраст, национальность и профессия.
3. **Описание рутины**: Добавляется описание ежедневной рутины Лизы.
4. **Описание профессии**: Предоставляется подробное описание работы Лизы в Microsoft в качестве специалиста по данным.
5. **Определение черт личности**: Определяются несколько черт личности Лизы.
6. **Определение профессиональных интересов**: Указываются профессиональные интересы Лизы.
7. **Определение личных интересов**: Указываются личные интересы Лизы.
8. **Определение навыков**: Перечисляются навыки, которыми владеет Лиза.
9. **Определение отношений**: Описываются отношения Лизы с другими персонажами.

**Примеры**:

```python
lisa = create_lisa_the_data_scientist()
print(lisa.name)  # Вывод: Lisa
print(lisa.age)  # Вывод: 28
print(lisa.occupation)  # Вывод: Data Scientist
```

### `create_marcos_the_physician`

**Назначение**: Создает и определяет характеристики виртуальной личности по имени Маркос, который является врачом.

**Параметры**:
- Нет параметров.

**Возвращает**:
- `marcos` (TinyPerson): Объект класса `TinyPerson`, представляющий Маркоса-врача с определенными атрибутами.

**Как работает функция**:

1. **Создание персонажа**: Создается экземпляр класса `TinyPerson` с именем "Marcos".
2. **Определение атрибутов**: Определяются основные атрибуты Маркоса, такие как возраст, национальность и профессия.
3. **Описание рутины**: Добавляется описание ежедневной рутины Маркоса.
4. **Описание профессии**: Предоставляется подробное описание работы Маркоса в качестве врача в регионе Сан-Паулу.
5. **Определение черт личности**: Определяются несколько черт личности Маркоса.
6. **Определение профессиональных интересов**: Указываются профессиональные интересы Маркоса.
7. **Определение личных интересов**: Указываются личные интересы Маркоса.
8. **Определение навыков**: Перечисляются навыки, которыми владеет Маркос.
9. **Определение отношений**: Описываются отношения Маркоса с другими персонажами.

**Примеры**:

```python
marcos = create_marcos_the_physician()
print(marcos.name)  # Вывод: Marcos
print(marcos.age)  # Вывод: 35
print(marcos.occupation)  # Вывод: Physician
```

### `create_lila_the_linguist`

**Назначение**: Создает и определяет характеристики виртуальной личности по имени Лила, которая является лингвистом.

**Параметры**:
- Нет параметров.

**Возвращает**:
- `lila` (TinyPerson): Объект класса `TinyPerson`, представляющий Лилу-лингвиста с определенными атрибутами.

**Как работает функция**:

1. **Создание персонажа**: Создается экземпляр класса `TinyPerson` с именем "Lila".
2. **Определение атрибутов**: Определяются основные атрибуты Лилы, такие как возраст, национальность и профессия.
3. **Описание рутины**: Добавляется описание ежедневной рутины Лилы.
4. **Описание профессии**: Предоставляется подробное описание работы Лилы в качестве лингвиста-фрилансера.
5. **Определение черт личности**: Определяются несколько черт личности Лилы.
6. **Определение профессиональных интересов**: Указываются профессиональные интересы Лилы.
7. **Определение личных интересов**: Указываются личные интересы Лилы.
8. **Определение навыков**: Перечисляются навыки, которыми владеет Лила.
9. **Определение отношений**: Описываются отношения Лилы с другими персонажами.

**Примеры**:

```python
lila = create_lila_the_linguist()
print(lila.name)  # Вывод: Lila
print(lila.age)  # Вывод: 28
print(lila.occupation)  # Вывод: Linguist