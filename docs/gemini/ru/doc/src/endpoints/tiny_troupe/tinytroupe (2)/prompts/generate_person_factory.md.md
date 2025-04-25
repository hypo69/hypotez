# Модуль для генерации описаний персон 

## Обзор

Этот файл предоставляет набор контекстов для генерации описаний персонажей, используя информацию о демографических характеристиках, физических особенностях, поведении, убеждениях и т. д. 

## Подробней

Этот файл содержит код, который создает множество контекстов, которые могут быть использованы для генерации описаний персон. Идея состоит в том, чтобы получить широкий контекст, содержащий некоторые детали о персонажах, которых мы хотим сгенерировать, например, демографические параметры, физические характеристики, поведение, убеждения и т. д., а затем создать множество других контекстов, более специфичных, но полученных из более общего контекста.

## Функции

### `generate_person_contexts`

**Назначение**: 
- Функция создает множество контекстов для генерации описаний персонажей.

**Параметры**:
- `context`: (str) -  Описание желаемых персонажей. Включает демографические характеристики, физические особенности, поведение, убеждения и т. д.

**Возвращает**:
- `list`: Список контекстов, каждый из которых представляет собой строку, которую можно использовать для генерации описания персонажа. 

**Как работает функция**:
- Функция анализирует предоставленный контекст и генерирует множество более специфических контекстов, используя информацию о демографических характеристиках, физических особенностях, поведении, убеждениях и т. д. 
- Каждый контекст представляет собой строку, содержащую более конкретную информацию о персонаже.

**Примеры**:

```python
# Входной контекст
context = "Please, generate 3 person(s) description(s) based on the following broad context: Latin American, age between 20 and 40 years old, economic status can vary between poor and rich, it can be religious or not, it can be married or not, it can have children or not, it can be a professional or not, it can be a worker or not"

# Вывод функции
result = generate_person_contexts(context)
print(result)

# Вывод:
# ["Mexican person that has formed as lawyer but now works in other are, is single, like sports and movies", "Create a Brazilian person that is a doctor, like pets and the nature and love heavy metal.", "Create a Colombian person that is a lawyer, like to read and drink coffee and is married with 2 children."]

```

**Пример использования**:

```python
# Входной контекст
context = "Please, generate 3 person(s) description(s) based on the following broad context:  American, age between 20 and 40 years old, economic status can vary between poor and rich, it can be religious or not, it can be married or not, it can have children or not, it can be a professional or not, it can be a worker or not"

# Вызов функции
result = generate_person_contexts(context)

# Печать результата
print(result)
```

## Примеры

```python
# Входной контекст
context = "Please, generate 3 person(s) description(s) based on the following broad context:  American, age between 20 and 40 years old, economic status can vary between poor and rich, it can be religious or not, it can be married or not, it can have children or not, it can be a professional or not, it can be a worker or not"

# Вызов функции
result = generate_person_contexts(context)

# Печать результата
print(result)

# Ожидаемый результат:
# ["American person that works as a lawyer, is married and has 2 children", "American person that is a doctor, lives in a small town and is religious", "American person that is a worker, is single and enjoys playing video games"]
```
```python
# Входной контекст
context = "Please, generate 3 person(s) description(s) based on the following broad context:  European, age between 20 and 40 years old, economic status can vary between poor and rich, it can be religious or not, it can be married or not, it can have children or not, it can be a professional or not, it can be a worker or not"

# Вызов функции
result = generate_person_contexts(context)

# Печать результата
print(result)

# Ожидаемый результат:
# ["European person that works as an engineer, is single and enjoys traveling", "European person that is a teacher, lives in a big city and is religious", "European person that is a worker, is married and has one child"]
```
```python
# Входной контекст
context = "Please, generate 3 person(s) description(s) based on the following broad context:  Asian, age between 20 and 40 years old, economic status can vary between poor and rich, it can be religious or not, it can be married or not, it can have children or not, it can be a professional or not, it can be a worker or not"

# Вызов функции
result = generate_person_contexts(context)

# Печать результата
print(result)

# Ожидаемый результат:
# ["Asian person that works as a doctor, is married and has one child", "Asian person that is a teacher, lives in a small town and is religious", "Asian person that is a worker, is single and enjoys playing sports"]