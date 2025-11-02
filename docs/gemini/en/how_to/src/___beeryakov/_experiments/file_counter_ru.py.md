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
This code block recursively counts lines, classes, and functions in files within a specified directory and its subdirectories. It excludes binary files, files within the "__pycache__" and "firefox_profiles" folders, and the "__init__.py" file.

Execution Steps
-------------------------
1. **Iterate Through Directory**: The `count_lines_in_files` function iterates through all files and subdirectories within the given directory.
2. **Check File Type**: For each item, it checks if it's a file or a directory.
3. **Count Lines in Text Files**: If it's a text file, the code opens the file and counts the number of lines. It also calls the `count_classes_and_functions` function to count classes and functions within the file.
4. **Recursive Call for Subdirectories**: If it's a directory, the `count_lines_in_files` function is recursively called to count lines, classes, and functions in the subdirectory.
5. **Count Classes and Functions**: The `count_classes_and_functions` function opens the specified file and iterates through each line. If a line starts with the "class" keyword, it increments the `total_classes` counter. If a line starts with the "def" keyword, it increments the `total_functions` counter.
6. **Binary File Check**: The `is_binary` function checks if a file is binary by reading the first 512 bytes and checking if it contains a null byte (b'\0').

Usage Example
-------------------------

```python
    src_directory = 'src'
    print(f"Подсчет строк, классов и функций в файлах в директории: {src_directory}")
    total_lines, total_classes, total_functions = count_lines_in_files(src_directory)
    print(f"Всего строк в текстовых файлах в \'{src_directory}\': {total_lines}")
    print(f"Всего классов: {total_classes}")
    print(f"Всего функций: {total_functions}")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".