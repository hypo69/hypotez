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
This code snippet implements a simple script for translating comments in a Python project. It first attempts to detect the language of a file's contents based on character encoding. If the file is detected as UTF-8, it assumes the comments are in Russian and prints them to the console.

Execution Steps
-------------------------
1. **Detect Language**: The `detect_language` function uses the `chardet` library to determine the character encoding of a given file. If the encoding is detected as UTF-8, it returns "utf-8", otherwise it returns `None`.
2. **Copy and Print Russian Text**: The `copy_and_print_russian_text` function iterates through all files in the source directory (`src_dir`) and copies them to the destination directory (`dest_dir`). For each file, it calls `detect_language` to determine the encoding. If the encoding is UTF-8, it opens the file in read mode with UTF-8 encoding and prints the file's contents to the console, indicating that it's assumed to be Russian text.
3. **Main Function**: The `main` function defines the source and destination directories, then calls the `copy_and_print_russian_text` function to perform the copying and printing.

Usage Example
-------------------------

```python
    # Путь к исходной папке
    src_folder = 'src'

    # Путь к папке, в которую будем копировать файлы
    dest_folder = 'src_en'

    # Вызываем функцию для копирования и вывода текста на русском языке
    copy_and_print_russian_text(src_folder, dest_folder)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".