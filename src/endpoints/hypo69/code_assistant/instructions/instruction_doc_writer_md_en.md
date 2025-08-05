
# INSTRUCTION

The code provided below is part of the `hypotez` project. Task: Create developer documentation in `Markdown` format for each input Python file.
The documentation must meet the following requirements:

1.  **Documentation Format**:
    -   Use the `Markdown (.md)` standard.
    -   Each file must start with a header and a brief description of its content.

    Documentation examples: Example of a module file header:

        """
        Module for working with the programmer's assistant
        =================================================

        The module contains the :class:`CodeAssistant` class, which is used for interacting with various AI models
        (e.g., Google Gemini and OpenAI) and performing code processing tasks.

        Usage Example
        ----------------------

        >>> assistant = CodeAssistant(role='code_checker', lang='ru', model=['gemini'])
        >>> assistant.process_files()
        """

    -   For all classes and functions, use the following comment format:
        ```python
        class MyClass:
            """Description of the class's purpose
            Inherits:
               If the class inherits from another - provide a description of the inheritance

            Attributes:
               param1 (str): Description of parameters (attributes) of the class

            Methods:
               function_1(): Description of the purpose of the class's functions/methods
           """

            def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:
                """ Function performs some action... <Here you write what the function specifically does>
                Args:
                    param (str): Description of the `param` parameter.
                    param1 (Optional[str | dict | str], optional): Description of the `param1` parameter. Defaults to `None`.

                Returns:
                    dict | None: Description of the return value. Returns a dictionary or `None`.

                Raises:
                    SomeError: Description of the situation where the `SomeError` exception is raised.
                   ...
                   <DO NOT output the function body. Only the docstring>
                """
                def inner_function():
                   """ Inner function performs some action... <Here you write what the function specifically does>
                       Args:
                           param (str): Description of the `param` parameter.
                           param1 (Optional[str | dict | str], optional): Description of the `param1` parameter. Defaults to `None`.

                       Returns:
                           dict | None: Description of the return value. Returns a dictionary or `None`.

                       Raises:
                           SomeError: Description of the situation where the `SomeError` exception is raised.

                       ...

                         DO NOT OUTPUT FUNCTION CODE. ONLY DOCSTRING

                       """
            ```
        -   All comments in the function and docstrings must be in Russian in UTF-8 format.
        -   If there are inner functions within the function being considered, describe each of them in detail separately.

    -   Use `ex` instead of `e` in exception handling blocks.
    -   For logging, use `logger` from my `src.logger` module. For example:
        ```python
        from src.logger import logger
        logger.info('Some information message')
        ...
        except SomeError as ex:
            logger.error('Some error message', ex, exc_info = True) # where the error is passed as the second argument. exc_info determines whether to output trace information.
       ```


    _ If webdriver is used in the code, know how to use it
      inherit Driver, Chrome, Firefox, Playwright
      Then define it like this
      # Creating a driver instance (example with Chrome)
      driver = Driver(Chrome)
      The Driver, Chrome, Firefox, Playwright modules already contain all Selenium settings.
      The main command used in the code is: `driver.execute_locator(l:dict)`
      It returns the value of the web element by locator.


    -   All comments and docstrings must be in Russian in UTF-8 format. If the docstring in the code is in English, translate it to Russian.

2.  **Table of Contents (TOC)**:
    -   At the beginning of each documentation file, add a section with a table of contents and links to functions and methods within the code.
    -   The TOC structure must include links to all main sections of the module's documentation.

3.  **Documentation Formatting**:
    -   Use Markdown syntax for all headers, lists, and links.
    -   For documenting classes, functions, and methods, include structured sections with descriptions, parameter details, return values, and raised exceptions. Example:

    ## Classes

    ### `class_name`
    Description of the class's purpose
        **Inherits**:
            If the class inherits from another - provide a description of the inheritance

         **Attributes**:
            param1 (str): Description of parameters (attributes) of the class

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

     **Raises Exceptions**:
     - `SomeError`: Description of the situation where the `SomeError` exception is raised.

     If there are inner functions within the function, discuss each of them separately.
     **Inner Functions**: If any


     **How the Function Works**:
     - Explain the function's purpose in detail. Provide a detailed description of the transformation actions that occur within the function body.


     **Examples**:
     - Create several examples of calling the function with different parameters passed to it.


4.  **Section Headers**:
    -   Use first-level (`#`), second-level (`##`), third-level (`###`), and fourth-level (`####`) headers consistently throughout the file.

5.  **Example File**:

   # Module Name

   ## Overview

   Brief description of the module's purpose.

   ## Details

   More detailed description. Explain how and why this code is used in the project.
   Analyze the code previously provided to you.

   ## Classes

   ### `ClassName`

   **Description**: Description of the class.
   **Inherits**:
   **Attributes**:
   **Parameters**:

    **Principle of Operation**:
        Explain the class's operation. If the class is complex, provide a detailed code breakdown.

   Create documentation for EACH function or method. Explain the purpose of each variable.
   - All comments and docstrings must be in Russian in UTF-8 format. If the original code text is in English, translate it to Russian.

   **Methods**: # if there are methods
   - `method_name`: Brief description of the method.
   - `method_name`: Brief description of the method.
   **Parameters**: # if there are parameters
   - `param` (str): Description of the `param` parameter.
   - `param1` (Optional[str | dict | str], optional): Description of the `param1` parameter. Defaults to `None`.
   **Examples**
   - Examples of class definition and working with the class.


   ## Class Methods

   ### `function_name`

   ```python
   def my_func(param1:str, param2:Optional[int] = 0) -> bool:
       """ Function performs some action... <Here you write what the function specifically does>
       Args:
           param1 (str): Description of the `param1` parameter.
           param2 (Optional[int], optional): Description of the `param2` parameter. Defaults to 0.
       Returns:
           bool: Description of the return value. Returns `True` or `False`.

        Raises:
             Execution error

        Example:
            Examples of calls with the full spectrum of parameters that can be passed to the function.

       """
       - Do not return the function code. Only the documentation and examples of function calls;
       - All comments and docstrings must be in Russian in UTF-8 format.
   ```



   ## Parameter Details
   - `param` (str): More detailed description of the `param` parameter.
   - `param1` (Optional[str | dict | str], optional): More detailed description of the `param1` parameter. Defaults to `None`.



   **Examples**: # All possible variations of function call examples with different parameters

   -------------------------------------------------------------------------------------



## Your Behavior During Code Analysis:
- Inside the code, you might encounter expressions between `<` `>`. For example: `<instruction for gemini model:Loading product descriptions into PrestaShop.>, <next, if available>. These are placeholders where you insert the relevant value.
- Always refer to the system instructions for processing code in the `hypotez` project (the first set of instructions you translated);
- Analyze the file's location within the project. This helps understand its purpose and relationship with other files. You will find the file location in the very first line of code starting with `## \file /...`;
- Memorize the provided code and analyze its connection with other parts of the project;
- In these instructions, do not suggest code improvements. Strictly follow point 5. **Example File** when composing the response.

# END OF INSTRUCTION
