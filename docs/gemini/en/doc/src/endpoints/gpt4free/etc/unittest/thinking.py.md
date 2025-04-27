# Module for testing thinking processing
## Overview
This module contains unit tests for the `ThinkingProcessor` class, which is used to process text chunks containing the `<think>` tag, indicating a thinking process. The tests cover various scenarios of how the class handles these chunks, including:
- Processing a regular text chunk without `<think>`.
- Handling the start of a thinking process.
- Handling the end of a thinking process.
- Handling both the start and end of a thinking process within the same chunk.
- Handling ongoing thinking processes.
- Handling chunks with text after the `<think>` tag.

## Details
The `TestThinkingProcessor` class contains unit tests for the `process_thinking_chunk` method of the `ThinkingProcessor` class. 
The tests are designed to verify that the method correctly identifies and handles the `<think>` tag, and returns the expected results. 
The tests also check the timing information associated with the thinking process.
## Classes
### `TestThinkingProcessor`
**Description**: This class is responsible for unit testing the `ThinkingProcessor` class.
**Inherits**: `unittest.TestCase`
**Attributes**: None
**Methods**:
- `test_non_thinking_chunk()`: Tests the processing of a regular text chunk without `<think>`.
- `test_thinking_start()`: Tests the processing of a chunk that marks the start of a thinking process.
- `test_thinking_end()`: Tests the processing of a chunk that marks the end of a thinking process.
- `test_thinking_start_and_end()`: Tests the processing of a chunk that contains both the start and end of a thinking process.
- `test_ongoing_thinking()`: Tests the handling of ongoing thinking processes.
- `test_chunk_with_text_after_think()`: Tests the processing of chunks with text after the `<think>` tag.
## Functions
### `test_non_thinking_chunk()`
**Purpose**: Тестирует обработку обычного текстового блока без `<think>`.
**Parameters**: None
**Returns**: None
**Raises Exceptions**: None
**Examples**:
```python
    def test_non_thinking_chunk(self):
        chunk = "This is a regular text."
        expected_time, expected_result = 0, [chunk]
        actual_time, actual_result = ThinkingProcessor.process_thinking_chunk(chunk)
        self.assertEqual(actual_time, expected_time)
        self.assertEqual(actual_result, expected_result)
```

### `test_thinking_start()`
**Purpose**: Тестирует обработку блока, который отмечает начало процесса размышления.
**Parameters**: None
**Returns**: None
**Raises Exceptions**: None
**Examples**:
```python
    def test_thinking_start(self):
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
**Purpose**: Тестирует обработку блока, который отмечает завершение процесса размышления.
**Parameters**: None
**Returns**: None
**Raises Exceptions**: None
**Examples**:
```python
    def test_thinking_end(self):
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
**Purpose**: Тестирует обработку блока, который содержит как начало, так и конец процесса размышления.
**Parameters**: None
**Returns**: None
**Raises Exceptions**: None
**Examples**:
```python
    def test_thinking_start_and_end(self):
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
**Purpose**: Тестирует обработку продолжающегося процесса размышления.
**Parameters**: None
**Returns**: None
**Raises Exceptions**: None
**Examples**:
```python
    def test_ongoing_thinking(self):
        start_time = time.time()
        chunk = "Still thinking..."
        expected_result = [Reasoning("Still thinking...")]
        actual_time, actual_result = ThinkingProcessor.process_thinking_chunk(chunk, start_time)
        self.assertEqual(actual_time, start_time)
        self.assertEqual(actual_result, expected_result)
```

### `test_chunk_with_text_after_think()`
**Purpose**: Тестирует обработку блока с текстом после тега `<think>`.
**Parameters**: None
**Returns**: None
**Raises Exceptions**: None
**Examples**:
```python
    def test_chunk_with_text_after_think(self):
        chunk = "Start <think>Middle</think>End"
        expected_time = 0
        expected_result = ["Start ", Reasoning(status="🤔 Is thinking...", is_thinking="<think>"), Reasoning("Middle"), Reasoning(status="Finished", is_thinking="</think>"), "End"]
        actual_time, actual_result = ThinkingProcessor.process_thinking_chunk(chunk)
        self.assertEqual(actual_time, expected_time)
        self.assertEqual(actual_result, expected_result)