**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use This Code Block
=========================================================================================

Description
-------------------------
This code block tests the `ThinkingProcessor` class, which is responsible for processing text chunks that contain thinking tags (`<think>`, `</think>`). The thinking tags indicate that the text within them requires special processing, such as sending it to a thinking engine for analysis.

Execution Steps
-------------------------
1. The code block defines a class `TestThinkingProcessor` that inherits from `unittest.TestCase`, the base class for all unit tests in Python.
2. It defines multiple test methods, each testing a specific scenario for processing text chunks with thinking tags:
    - `test_non_thinking_chunk`: Tests a regular text chunk without any thinking tags.
    - `test_thinking_start`: Tests a chunk with a thinking tag at the beginning.
    - `test_thinking_end`: Tests a chunk with a thinking tag at the end.
    - `test_thinking_start_and_end`: Tests a chunk with thinking tags at the beginning and end.
    - `test_ongoing_thinking`: Tests a chunk with ongoing thinking.
    - `test_chunk_with_text_after_think`: Tests a chunk with thinking tags in the middle of text.
3. Each test method:
    - Defines the input `chunk` to be processed.
    - Defines the expected result, including the processed text chunks and the start and end times of the thinking process.
    - Calls `ThinkingProcessor.process_thinking_chunk` to process the `chunk`.
    - Uses `self.assertEqual` or `self.assertAlmostEqual` to assert that the actual results match the expected results.

Usage Example
-------------------------

```python
    # Import necessary modules
    import unittest
    import time

    from g4f.tools.run_tools import ThinkingProcessor, Reasoning

    # Define a class for testing the ThinkingProcessor
    class TestThinkingProcessor(unittest.TestCase):

        # Test a text chunk without any thinking tags
        def test_non_thinking_chunk(self):
            chunk = "This is a regular text."
            expected_time, expected_result = 0, [chunk]
            actual_time, actual_result = ThinkingProcessor.process_thinking_chunk(chunk)
            self.assertEqual(actual_time, expected_time)
            self.assertEqual(actual_result, expected_result)

    # Create a test suite and run the tests
    suite = unittest.TestSuite()
    suite.addTest(TestThinkingProcessor('test_non_thinking_chunk'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".