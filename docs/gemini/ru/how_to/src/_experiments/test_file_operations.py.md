### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода предназначен для тестирования основных операций с файлами: создания, записи, чтения и удаления. Он создает файл, записывает в него данные, затем считывает и проверяет содержимое. После этого добавляет новую строку в файл и снова проверяет его содержимое. В завершение файл удаляется.

Шаги выполнения
-------------------------
1. **Определение пути к файлу**: Задается имя файла `test_file.txt`, с которым будут производиться операции.
2. **Создание и запись в файл**: Открывается файл в режиме записи (`"w"`), и в него записывается строка "Hello, World!".
3. **Чтение содержимого файла**: Открывается файл в режиме чтения (`"r"`), считывается его содержимое и проверяется, соответствует ли оно ожидаемому значению "Hello, World!". Если содержимое не совпадает, тест завершается с ошибкой.
4. **Добавление новой строки в файл**: Открывается файл в режиме добавления (`"a"`), и в него добавляется строка "\nAppended Line".
5. **Проверка добавленного содержимого**: Файл снова открывается в режиме чтения, считываются все строки, и проверяется, что вторая строка (после добавления) соответствует ожидаемому значению "Appended Line". Если строка не совпадает, тест завершается с ошибкой.
6. **Удаление файла**: После выполнения всех операций (или в случае возникновения ошибки) проверяется, существует ли файл. Если файл существует, он удаляется. Если файл не найден, выводится соответствующее сообщение.

Пример использования
-------------------------

```python
import os

def test_file_operations():
    """Test for basic file operations: create, read, write, and delete."""

    # Step 1: Define the file path
    filename = "test_file.txt"

    try:
        # Step 2: Create and write to the file
        with open(filename, "w") as f:
            f.write("Hello, World!")

        # Step 3: Read the content from the file
        with open(filename, "r") as f:
            content = f.read()
            assert content == "Hello, World!", f"Unexpected content: {content}"

        # Step 4: Append new content to the file
        with open(filename, "a") as f:
            f.write("\nAppended Line")

        # Step 5: Verify the appended content
        with open(filename, "r") as f:
            lines = f.readlines()
            assert lines[1].strip() == "Appended Line", f"Unexpected line: {lines[1].strip()}"

        print("All tests passed!")

    except AssertionError as e:
        print(f"Test failed: {e}")

    finally:
        # Step 6: Delete the file
        if os.path.exists(filename):
            os.remove(filename)
            print(f"File '{filename}' удален.")
        else:
            print(f"Файл '{filename}' не найден для удаления.")

# Запуск теста
test_file_operations()
...