# Модуль тестирования ThinkingProcessor

## Обзор

Этот модуль содержит юнит-тесты для класса `ThinkingProcessor`, который используется для обработки текста с  "мыслительными" блоками,  ограниченными тегами `<think>` и `</think>`.  
 
## Классы

### `TestThinkingProcessor`

**Описание**: Класс юнит-тестов для `ThinkingProcessor`. 

**Наследует**: `unittest.TestCase` 

**Методы**:

- `test_non_thinking_chunk()`: Тестирует обработку обычного текста без "мыслительных" блоков.
- `test_thinking_start()`: Тестирует обработку текста с началом "мыслительного" блока.
- `test_thinking_end()`: Тестирует обработку текста с завершением "мыслительного" блока.
- `test_thinking_start_and_end()`: Тестирует обработку текста с началом и завершением "мыслительного" блока.
- `test_ongoing_thinking()`: Тестирует обработку текста, который находится внутри "мыслительного" блока.
- `test_chunk_with_text_after_think()`: Тестирует обработку текста с "мыслительным" блоком, который находится в середине текста.

## Функции

### `test_non_thinking_chunk()`

**Назначение**: Проверяет, что `ThinkingProcessor.process_thinking_chunk()` правильно обрабатывает обычный текст без "мыслительных" блоков.

**Параметры**: 
- `chunk` (str): Текст без "мыслительных" блоков.

**Возвращает**: 
- `None`

**Вызывает исключения**: 
- `AssertionError`: Если время обработки или результат обработки не соответствуют ожидаемым.

**Пример**:
```python
chunk = "This is a regular text."
expected_time, expected_result = 0, [chunk]
actual_time, actual_result = ThinkingProcessor.process_thinking_chunk(chunk)
self.assertEqual(actual_time, expected_time)
self.assertEqual(actual_result, expected_result)
```

### `test_thinking_start()`

**Назначение**: Проверяет, что `ThinkingProcessor.process_thinking_chunk()` правильно обрабатывает текст с началом "мыслительного" блока.

**Параметры**: 
- `chunk` (str): Текст с началом "мыслительного" блока.

**Возвращает**: 
- `None`

**Вызывает исключения**: 
- `AssertionError`: Если время обработки, результат обработки или состояние "мыслительного" блока не соответствуют ожидаемым.

**Пример**:
```python
chunk = "Hello <think>World"
expected_time = time.time()
expected_result = ["Hello ", Reasoning(status="🤔 Is thinking...", is_thinking="<think>"), Reasoning("World")]
actual_time, actual_result = ThinkingProcessor.process_thinking_chunk(chunk)
self.assertAlmostEqual(actual_time, expected_time, delta=1)
self.assertEqual(actual_result[0], expected_result[0])
self.assertEqual(actual_result[1], expected_result[1])
self.assertEqual(actual_result[2], expected_result[2])
```

### `test_thinking_end()`

**Назначение**: Проверяет, что `ThinkingProcessor.process_thinking_chunk()` правильно обрабатывает текст с завершением "мыслительного" блока.

**Параметры**: 
- `chunk` (str): Текст с завершением "мыслительного" блока.
- `start_time` (float): Время начала "мыслительного" блока.

**Возвращает**: 
- `None`

**Вызывает исключения**: 
- `AssertionError`: Если время обработки, результат обработки или состояние "мыслительного" блока не соответствуют ожидаемым.

**Пример**:
```python
start_time = time.time()
chunk = "token</think> content after"
expected_result = [Reasoning("token"), Reasoning(status="Finished", is_thinking="</think>"), " content after"]
actual_time, actual_result = ThinkingProcessor.process_thinking_chunk(chunk, start_time)
self.assertEqual(actual_time, 0)
self.assertEqual(actual_result[0], expected_result[0])
self.assertEqual(actual_result[1], expected_result[1])
self.assertEqual(actual_result[2], expected_result[2])
```

### `test_thinking_start_and_end()`

**Назначение**: Проверяет, что `ThinkingProcessor.process_thinking_chunk()` правильно обрабатывает текст с началом и завершением "мыслительного" блока.

**Параметры**: 
- `chunk` (str): Текст с началом и завершением "мыслительного" блока.
- `start_time` (float): Время начала "мыслительного" блока.

**Возвращает**: 
- `None`

**Вызывает исключения**: 
- `AssertionError`: Если время обработки, результат обработки или состояние "мыслительного" блока не соответствуют ожидаемым.

**Пример**:
```python
start_time = time.time()
chunk = "<think>token</think> content after"
expected_result = [Reasoning(status="🤔 Is thinking...", is_thinking="<think>"), Reasoning("token"), Reasoning(status="Finished", is_thinking="</think>"), " content after"]
actual_time, actual_result = ThinkingProcessor.process_thinking_chunk(chunk, start_time)
self.assertEqual(actual_time, 0)
self.assertEqual(actual_result[0], expected_result[0])
self.assertEqual(actual_result[1], expected_result[1])
self.assertEqual(actual_result[2], expected_result[2])
self.assertEqual(actual_result[3], expected_result[3])
```

### `test_ongoing_thinking()`

**Назначение**: Проверяет, что `ThinkingProcessor.process_thinking_chunk()` правильно обрабатывает текст, который находится внутри "мыслительного" блока.

**Параметры**: 
- `chunk` (str): Текст внутри "мыслительного" блока.
- `start_time` (float): Время начала "мыслительного" блока.

**Возвращает**: 
- `None`

**Вызывает исключения**: 
- `AssertionError`: Если время обработки или результат обработки не соответствуют ожидаемым.

**Пример**:
```python
start_time = time.time()
chunk = "Still thinking..."
expected_result = [Reasoning("Still thinking...")]
actual_time, actual_result = ThinkingProcessor.process_thinking_chunk(chunk, start_time)
self.assertEqual(actual_time, start_time)
self.assertEqual(actual_result, expected_result)
```

### `test_chunk_with_text_after_think()`

**Назначение**: Проверяет, что `ThinkingProcessor.process_thinking_chunk()` правильно обрабатывает текст с "мыслительным" блоком, который находится в середине текста.

**Параметры**: 
- `chunk` (str): Текст с "мыслительным" блоком, который находится в середине текста.

**Возвращает**: 
- `None`

**Вызывает исключения**: 
- `AssertionError`: Если время обработки или результат обработки не соответствуют ожидаемым.

**Пример**:
```python
chunk = "Start <think>Middle</think>End"
expected_time = 0
expected_result = ["Start ", Reasoning(status="🤔 Is thinking...", is_thinking="<think>"), Reasoning("Middle"), Reasoning(status="Finished", is_thinking="</think>"), "End"]
actual_time, actual_result = ThinkingProcessor.process_thinking_chunk(chunk)
self.assertEqual(actual_time, expected_time)
self.assertEqual(actual_result, expected_result)
```

## Параметры класса

- `chunk` (str): Текст, который обрабатывается `ThinkingProcessor`.
- `start_time` (float): Время начала "мыслительного" блока, если он есть.

## Примеры

- **Пример 1**: Обработка обычного текста без "мыслительных" блоков.
```python
chunk = "This is a regular text."
actual_time, actual_result = ThinkingProcessor.process_thinking_chunk(chunk)
print(f"Time: {actual_time}, Result: {actual_result}") 
```

- **Пример 2**: Обработка текста с началом и завершением "мыслительного" блока.
```python
chunk = "<think>token</think> content after"
start_time = time.time()
actual_time, actual_result = ThinkingProcessor.process_thinking_chunk(chunk, start_time)
print(f"Time: {actual_time}, Result: {actual_result}") 
```

- **Пример 3**: Обработка текста, который находится внутри "мыслительного" блока.
```python
chunk = "Still thinking..."
start_time = time.time()
actual_time, actual_result = ThinkingProcessor.process_thinking_chunk(chunk, start_time)
print(f"Time: {actual_time}, Result: {actual_result}")
```

- **Пример 4**: Обработка текста с "мыслительным" блоком, который находится в середине текста.
```python
chunk = "Start <think>Middle</think>End"
actual_time, actual_result = ThinkingProcessor.process_thinking_chunk(chunk)
print(f"Time: {actual_time}, Result: {actual_result}")
```

## Внутренние функции

### `process_thinking_chunk()`

**Назначение**: Основная функция класса `ThinkingProcessor`, которая обрабатывает отдельный блок текста. 
- Извлекает начало и конец "мыслительных" блоков, 
- Отслеживает время работы "мыслительных" блоков, 
- Формирует список элементов, которые будут переданы в модель. 
- Делит текст на отдельные "мыслительные" блоки.
- Преобразует текст в список с "мыслительными" блоками.
- Определяет время обработки "мыслительного" блока.

**Параметры**: 
- `chunk` (str): Текст, который обрабатывается.
- `start_time` (float): Время начала "мыслительного" блока, если он есть.

**Возвращает**: 
- `tuple`: (Время обработки, список элементов).

**Вызывает исключения**: 
- `None`

**Пример**:
```python
chunk = "Start <think>Middle</think>End"
actual_time, actual_result = ThinkingProcessor.process_thinking_chunk(chunk)
print(f"Time: {actual_time}, Result: {actual_result}")
```

### `get_thinking_status()`

**Назначение**: Определяет статус "мыслительного" блока: начался, закончился или продолжается.

**Параметры**: 
- `chunk` (str): Часть текста, которую необходимо проверить.

**Возвращает**: 
- `str`: Статус "мыслительного" блока: "🤔 Is thinking...", "Finished", "" (пустая строка, если "мыслительный" блок не найден).

**Вызывает исключения**: 
- `None`

**Пример**:
```python
chunk = "<think>"
status = ThinkingProcessor.get_thinking_status(chunk)
print(f"Status: {status}") 
```

### `get_thinking_time()`

**Назначение**: Вычисляет время обработки "мыслительного" блока.

**Параметры**: 
- `start_time` (float): Время начала "мыслительного" блока.

**Возвращает**: 
- `float`: Время обработки "мыслительного" блока.

**Вызывает исключения**: 
- `None`

**Пример**:
```python
start_time = time.time()
thinking_time = ThinkingProcessor.get_thinking_time(start_time)
print(f"Thinking Time: {thinking_time}")