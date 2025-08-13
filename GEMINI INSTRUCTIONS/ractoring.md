Your task is to edit the Python files in the project.


1. Recursively go through all files with the `.py` extension in the `src` directory.
Analyze the code in the file and remember it to understand the overall logic of the project. Use the knowledge gained when working with other files in the project.
   - For each file, check if there is a file with the same name and relative path in the `src_en` directory.
   If such a file already exists, skip it.
1. Translate all docstrings, comments, and notes into English.
   - Use machine translation, but make sure the translation is correct and understandable.
   - If there are already comments in English in the code, do not change them.
   - If there are lines in Russian in the code, translate them into English.
   - Do not change the code, only comments and docstrings.
3. If there is no docstring in some part of the code, add it in reStructuredText format.
   - If it is a function, class, or method, add a docstring describing the parameters and return value.
   - If it is a module, add a module docstring describing the module.
2. In each file, check for the presence of a shebang line (e.g., `#!/usr/bin/env python3`).
If it is absent, add the following at the beginning of the file:
```python
## \file /src/<path>/<to>/<file_name>.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3.13
```
3.  Check for the presence of a module docstring (the first docstring in the file).
4. Immediately after the shebang (or at the beginning of the file if the shebang is absent), insert the following header:

    """
    .. module:: <module>
        :platform: Windows, Unix
        :synopsis: <module description>

    <module header>
    ================

    <Module description in 2–4 sentences>

    Example:
    ```python
        from src.<...> import ...
        ...
    ```

    :author: hypo69
    :license: Proprietary. All rights reserved.
    :version: 1.0.0
    :location: <relative path to the file from src/>
    """

5. Get the values of `<module>`, `<module description>`, and `<relative path>` based on the file's path and name:
    - `<module>`: the file's path from `src/`, divided by dots (e.g., `src.utils.file`)
    - `<module description>`: if there is already a module docstring in the code — use its first line. If not — leave a placeholder `TODO: add module description`.
    - `<relative path>`: the path to the file from `src/`, for example `utils/file.py`
6. Before you start inserting - analyze the code in the file. ONLY AFTER analyzing the code, collect the insert with the relevant header, description (synopsis), and examples

7. If there is already a module docstring (the first docstring in the file), form it according to the rules above.

8. Do not change the rest of the code and do not format it.

9. Save the modified file in the `src_en` directory with the same hierarchy as the original file. For example, if the original file is located at `src/utils/io.py`, the saved file should be at `src_en/utils/io.py`.

Example:

For File : `src/utils/io.py`

Insert:

    """
    .. module:: src.utils.io
        :platform: Windows, Unix
        :synopsis: Utilities for working with JSON and text

    Reading, writing, and serializing JSON files with logging and error handling.
    ===============================================================================

    This module provides functions for working with JSON and text files, 
    including reading, writing, and serializing with logging and error handling.

    Example:
    ```python
        from src.utils.io import j_loads, save_text_file
    ```

    :author: hypo69
    :license: Proprietary. All rights reserved.
    :version: 1.0.0
    :location: utils/io.py
    """
            
            
Вот полный перевод твоего текста на английский язык:

---

### ✅ Final Header Template

````python
## \file /src/<path>/<to>/<file_name>.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.<module_path>
    :platform: Windows, Unix
    :synopsis: <Short description>

<Detailed description of the module>
=========================================================================================

This module provides functions for working with text files: saving, reading, searching,
and handling large files using generators for memory efficiency.

Example usage
-------------

```python
    from src.<...> import ...
    ...
```

:author: hypo69  
:license: Proprietary. All rights reserved.  
:version: 1.0.0  
:location: src/<module_path>.py  
"""
````

---

### 📌 Field Descriptions:

| Field         | Purpose                                                       |
| ------------- | ------------------------------------------------------------- |
| `.. module::` | For documentation generators and IDE navigation               |
| `:platform:`  | Platform compatibility (Windows, Unix, etc.)                  |
| `:synopsis:`  | Short summary, shown in documentation overviews               |
| `:author:`    | Author of the file or module                                  |
| `:license:`   | License type (Proprietary in this case)                       |
| `:version:`   | Current version of the file or module                         |
| `:location:`  | Relative path to the file within the `src/` project directory |

---

### ✅ Example for `src/utils/file.py`:

````python
## \file /src/utils/file.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.utils.file
    :platform: Windows, Unix
    :synopsis: Text file utilities

Utilities for reading, writing, and processing text files.
=========================================================================================

This module includes functions to work with text files: saving, reading, searching,
and handling large files using generators.

Example usage
-------------

```python
    from pathlib import Path
    from src.utils.file import read_text_file, save_text_file

    content = read_text_file(Path("input.txt"))
    if content:
        print(content[:100])

    save_text_file(Path("output.txt"), "new text")
````

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/utils/file.py
"""

````

Use **Google style docstrings**  
---

### ✅ Google-Style Syntax Overview:

```python
"""
Short function summary.

Optional detailed explanation of what the function does.

Args:
    param1 (str): Description of the first parameter.
    param2 (int, optional): Description of the second parameter. Defaults to 42.

Returns:
    bool: Description of the return value.

Raises:
    ValueError: If param1 is invalid.

Notes:
    Additional notes about the function, if necessary.

"""
````

---

### 🧩 Example

```python
def save_text_file(
    data: str | list[str] | dict,
    file_path: str | Path,
    mode: str = 'w'
) -> bool:
    """
    Saves data to a text file.

    Args:
        data (str | list[str] | dict): Data to write — a string, list of strings, or a dictionary.
        file_path (str | Path): Path to the file.
        mode (str, optional): Write mode ('w' for overwrite, 'a' for append). Defaults to 'w'.

    Returns:
        bool: True if the file was saved successfully, False otherwise.

    Raises:
        Exception: If an error occurs during file writing.
    """
```

---

### ✅ Features of Google-Style Docstrings:

| Feature           | Description                                                              |
| ----------------- | ------------------------------------------------------------------------ |
| Clear sections    | Uses `Args:`, `Returns:`, `Raises:` etc.                                 |
| Simplicity        | No verbose syntax like `:param:`, `:type:`                               |
| IDE compatibility | Fully supported in PyCharm, VSCode, pylint, mypy, etc.                   |
| Tooling support   | Compatible with `docformatter`, `mkdocstrings`, `blackdoc`, `pdoc`, etc. |

---

### ❗ Comparison: Google-Style vs Sphinx-Style

| Google-Style         | Sphinx-Style                            |
| -------------------- | --------------------------------------- |
| `Args:`              | `:param <name>: <description>`          |
| `Returns:`           | `:return: <description>`                |
| Types in parentheses | Types via `:type:` directive            |
| More human-readable  | More formalized for strict Sphinx usage |

---
