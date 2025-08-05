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
The code block defines a pytest test that executes Jupyter notebooks and checks for exceptions. It iterates through all notebooks in a specified folder, runs each notebook using the `ExecutePreprocessor` from `nbconvert`, and checks for any errors. If a notebook executes successfully, it saves a copy of the executed notebook with a ".executed.local.ipynb" suffix.

Execution Steps
-------------------------
1. **Import necessary libraries**: The code starts by importing necessary libraries, including `os`, `nbformat`, `nbconvert.preprocessors`, `pytest`, and `conftest`.
2. **Set up the environment**: It sets up the environment by adding the project's paths to `sys.path` to ensure the proper package import.
3. **Define variables**: The code defines variables like `NOTEBOOK_FOLDER`, `TIMEOUT`, and `KERNEL_NAME` for specifying the folder containing notebooks, execution timeout, and the kernel to use.
4. **Define the `get_notebooks` function**: This function retrieves all Jupyter notebook files from a given folder. It uses `os.listdir` to list files in the folder, filters them based on their extension (`.ipynb`), and excludes notebooks with ".executed." and ".local." in their names.
5. **Define the `test_notebook_execution` function**: This function is decorated with `@pytest.mark.parametrize` to execute the test for each notebook found in `NOTEBOOK_FOLDER`.
6. **Conditional execution**: The code checks if `conftest.test_examples` is True, which indicates whether to execute notebooks during testing.
7. **Execute the notebook**: If `conftest.test_examples` is True, the code opens the notebook, reads it as a `nbformat` object, executes it using `ExecutePreprocessor`, and catches any exceptions.
8. **Save the executed notebook**: After execution, the code saves a copy of the executed notebook with a ".executed.local.ipynb" suffix.
9. **Logging**: The code prints messages indicating the execution status of each notebook.

Usage Example
-------------------------

```python
    import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import pytest

import sys
sys.path.insert(0, '../../tinytroupe/') # ensures that the package is imported from the parent directory, not the Python installation
sys.path.insert(0, '../../') # ensures that the package is imported from the parent directory, not the Python installation
sys.path.insert(0, '..') # ensures that the package is imported from the parent directory, not the Python installation

import conftest

# Set the folder containing the notebooks
NOTEBOOK_FOLDER = os.path.join(os.path.dirname(__file__), "../../examples/")  # Update this path

# Set a timeout for long-running notebooks
TIMEOUT = 600

KERNEL_NAME = "python3" #"py310"


def get_notebooks(folder):
    """Retrieve all Jupyter notebook files from the specified folder."""
    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.endswith(".ipynb") and not ".executed." in f and not ".local." in f
    ]

@pytest.mark.parametrize("notebook_path", get_notebooks(NOTEBOOK_FOLDER))
def test_notebook_execution(notebook_path):
    """Execute a Jupyter notebook and assert that no exceptions occur."""

    if conftest.test_examples:
        with open(notebook_path, "r", encoding="utf-8") as nb_file:
            notebook = nbformat.read(nb_file, as_version=4)
            print(f"Executing notebook: {notebook_path} with kernel: {KERNEL_NAME}")
            ep = ExecutePreprocessor(timeout=TIMEOUT, kernel_name=KERNEL_NAME)

            try:
                ep.preprocess(notebook, {'metadata': {'path': NOTEBOOK_FOLDER}})
                print(f"Notebook {notebook_path} executed successfully.")

            except Exception as e:
                pytest.fail(f"Notebook {notebook_path} raised an exception: {e}")
            
            finally:
                # save a copy of the executed notebook
                output_path = notebook_path.replace(".ipynb", ".executed.local.ipynb")
                with open(output_path, "w", encoding="utf-8") as out_file:
                    nbformat.write(notebook, out_file)
                
                print(f"Executed notebook saved as: {output_path}")
    else:
        print(f"Skipping notebooks executions for {notebook_path}.")

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".