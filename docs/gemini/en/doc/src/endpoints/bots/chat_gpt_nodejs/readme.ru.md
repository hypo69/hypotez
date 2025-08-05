# INSTRUCTION

The code provided below is part of the `hypotez` project. The task is to create developer documentation in `Markdown` format for each input Python file.
The documentation must meet the following requirements:

1. **Documentation Format**:
   - Use standard `Markdown (.md)`.
   - Each file should start with a title and a brief description of its contents.

   Documentation examples: Example of a module file header:

        """
        Module for working with the programmer's assistant
        =================================================

        The module contains the class :class:`CodeAssistant`, which is used to interact with various AI models
        (e.g., Google Gemini and OpenAI) and perform code processing tasks.

        Usage example
        ----------------------

        >>>assistant = CodeAssistant(role='code_checker', lang='ru', model=['gemini'])
        >>>assistant.process_files()
        """

   - For all classes and functions, use the following comment format:
     ```python
     class MyClass:
         """Description of the class's purpose
         Inherits: 
            If the class inherits from another, provide a description of the inheritance.

         Attributes:
            param1 (str): Description of the class's parameters (attributes)

         Methods:
            function_1(): Description of the purpose of the class's functions/methods
        """
     
         def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:
             """ Function performs some action... <Here, You write what the function does> 
             Args:
                 param (str): Description of the `param` parameter.
                 param1 (Optional[str | dict | str], optional): Description of the `param1` parameter. Defaults to `None`.

             Returns:
                 dict | None: Description of the return value. Returns a dictionary or `None`.

             Raises:
                 SomeError: Description of the situation in which the `SomeError` exception occurs.
                ...
                <DO NOT output the function body. Only docstring>
             """
             def inner_function():
                """ Inner function. Function performs some action... <Here, You write what the function does> 
                    Args:
                        param (str): Description of the `param` parameter.
                        param1 (Optional[str | dict | str], optional): Description of the `param1` parameter. Defaults to `None`.

                    Returns:
                        dict | None: Description of the return value. Returns a dictionary or `None`.

                    Raises:
                        SomeError: Description of the situation in which the `SomeError` exception occurs.

                    ...
                  
                      DO NOT OUTPUT THE FUNCTION CODE. ONLY DOCSTR

                    """
         ```
     - All comments in the function and docstring must be in Russian in UTF-8 format
     - If there are internal functions inside the function under consideration, consider each of them in detail separately.

   - Use `ex` instead of `e` in exception handling blocks.
   - For logging, use `logger` from my `src.logger` module. For example:
     ```python
     from src.logger import logger
     logger.info('Some information message')
     ...
     except SomeError as ex:
         logger.error('Some error message', ex, exc_info = True), where the error is passed as the second argument. exc_info determines whether or not to output service information.
    ```

    _ If the code uses a web driver, know how to use it.
    Inherit Driver, Chrome, Firexox, Playwright
    Then define it like this
    # Creating a driver instance (example with Chrome)
    driver = Drivewr(Chrome)
    The Driver and Chrome, Firexox, Playwright modules already contain all selenium settings.
    The main command that is used in the code: `driver.execute_locator(l:dict)`
    It returns the value of the web element by locator.

   - All comments and docstrings must be in Russian in UTF-8 format. If there are English docstrings in the code, translate them to Russian.

2. **Table of Contents (TOC)**:
   - At the beginning of each documentation file, add a section with a table of contents and links to functions and methods within the code.
   - The table of contents structure should include links to all major sections of the module's documentation.

3. **Documentation Formatting**:
   - Use Markdown syntax for all headings, lists, and links.
   - For documenting classes, functions, and methods, include structured sections with descriptions, parameter details, return values, and exceptions raised. Example:

    ## Classes

    ### `class_name`
    Description of the class's purpose
        **Inherits** 
            If the class inherits from another, provide a description of the inheritance.

         **Attributes**:
            param1 (str): Description of the class's parameters (attributes)

         **Methods**:
            function_1(): Description of the purpose of the class's functions/methods


     ## Functions

     ### `function_name`

     **Purpose**: Purpose of the function.


     **Parameters**:
     - `param` (str): Description of the `param` parameter.
     - `param1` (Optional[str | dict | str], optional): Description of the `param1` parameter. Defaults to `None`.

     **Returns**:
     - `dict | None`: Description of the return value.

     **Raises**:
     - `SomeError`: Description of the situation in which the `SomeError` exception occurs.

     If there are internal functions inside the function, consider each of them separately.
     **Internal functions**: If there are any

     

     **How the function works**:
     - Explain the function's purpose in detail. Make a detailed description of what actions and transformations occur in the function body.


     **Examples**:
     - Create several examples of calling the function with different parameters that are passed to the function.
     
     
4. **Section Headings**:
   - Use first-level (`#`), second-level (`##`), third-level (`###`), and fourth-level (`####`) headings sequentially throughout the file.

5. **Example File**:

   # Module Name

   ## Overview

   A brief description of the module's purpose.

   ## More details

   A more detailed description. Explain how and why this code is used in the project.
   Analyze the code previously provided to you.

   ## Classes

   ### `ClassName`

   **Description**: Description of the class.
   **Inherits**:
   **Attributes**:
   **Parameters**:

    **Working principle**:
        Explain how the class works. If the class is complex, make a detailed code analysis.

   Document EVERY function or method. Explain the purpose of each variable.
   - All comments and docstrings must be in Russian in UTF-8 format. If the text in the original code is in English, translate them to Russian.

   **Methods**: # if there are methods
   - `method_name`: Brief description of the method.
   - `method_name`: Brief description of the method.
   **Parameters**: # if there are parameters
   - `param` (str): Description of the `param` parameter.
   - `param1` (Optional[str | dict | str], optional): Description of the `param1` parameter. Defaults to `None`.
   **Examples**
   - Examples of defining the class and working with the class.


   ## Class Methods

   ### `function_name`

   ```python
   def my_func(param1:str, param2:Optional[int] = 0) -> bool:
       """ Function performs some action... <Here, You write what the function does> 
       Args:
           param1 (str): Description of the `param1` parameter.
           param2 (Optional[int], optional): Description of the `param2` parameter. Defaults to 0.
       Returns:
           bool: Description of the return value. Returns `True` or `False`.

        Raises:
             Execution Error

        Example:
            Examples of calls with the full range of parameters that can be passed to the function.

       """
       - Do not output the function code. Only documentation and examples of calling the function;
       - All comments and docstrings must be in Russian in UTF-8 format
   ```


   ## Class Parameters
   - `param` (str): More detailed Description of the `param` parameter.
   - `param1` (Optional[str | dict | str], optional): More detailed Description of the `param1` parameter. Defaults to `None`.

 

   **Examples**: # All possible variations of examples of calling the function with different parameters

   -------------------------------------------------------------------------------------
   

## Your behavior when analyzing the code:
- inside the code, you may encounter an expression between `<` ``>``. For example: <instruction for the gemini model: Loading product descriptions into PrestaShop.>, <next, if any>. These are stubs where you insert the relevant value.
- always look at the system instruction for processing the `hypotez` project code;
- analyze the file's location in the project. This will help you understand its purpose and relationship to other files. You will find the file location in the very first line of code, starting with `## \\file /...`;
- memorize the provided code and analyze its connection with other parts of the project;
- In this instruction, do not suggest code improvements. Strictly follow point 5. **Example file** when composing the answer.

# END OF INSTRUCTION
```

# `readme.ru.md`

## Обзор

Этот файл содержит информацию о реализации чат-бота ChatGPT с использованием Node.js.
В нем также содержится ссылка на статью на Habr, где описывается этот процесс.

## Подробнее

Этот файл предназначен для предоставления базовой информации о реализации чат-бота ChatGPT с использованием Node.js. Он указывает на ресурс (статью на Habr), где можно найти более подробное описание и инструкции по реализации.
Анализ кода показывает, что цель файла - служить отправной точкой для разработчиков, желающих создать подобного чат-бота.

## Ссылка на статью

[Реализация ChatGPT бота средствами nodejs](https://habr.com/ru/companies/selectel/articles/731692/)