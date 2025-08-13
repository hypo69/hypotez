**System Instruction: Translation Pipeline for Python Source Files**

**Goal:**
Automate the process of translating comments, docstrings, metadata, and any other Russian-language textual blocks in Python source files from the `src` directory into English, while preserving the code itself.

---

### **Workflow**

1. **Directories**

   * **Source directory:** `src`
   * **Destination directory:** `src_en`

2. **Step 1 — Scan Existing Destination**

   * Recursively traverse all subdirectories of `src_en` and record the relative paths of all existing `.py` files.
   * Store these paths for comparison in Step 3.

3. **Step 2 — Process Source Files**

   * Recursively traverse all subdirectories of `src`.
   * For each file ending with `.py`:

     1. Determine its relative path from `src`.
     2. Check if a file with the **same relative path** already exists in `src_en` (from Step 1).

        * If **exists** → skip and continue to the next file.
        * If **not exists** → proceed to Step 4.

4. **Step 3 — Translation Rules**

   * Input file encoding: UTF-8.
   * **Do not modify code syntax or structure.**
   * **Translate only:**

     * Inline comments (`# ...`) containing Russian text.
     * Docstrings (`"""..."""` or `'''...'''`) containing Russian text.
     * Special metadata headers, block comments, or structured text in Russian.
   * **Preserve:**

     * All variable names, function names, class names, and code logic.
     * All non-Russian text exactly as is.

5. **Step 4 — Save Translated File**

   * Create the corresponding directory path inside `src_en` (mirroring the structure of `src`).
   * Save the translated file to the new location, preserving the original filename.
   * Ensure file encoding remains UTF-8.

6. **Additional Requirements**

   * Maintain original indentation, spacing, and line breaks.
   * Keep all existing comments, but in English if they were Russian.
   * If a comment or docstring is partly in English and partly in Russian → translate only the Russian parts.

---

### **Example**

**Original file** (`src/module/example.py`):

```python
# Это тестовая функция
def add(a, b):
    """Суммирует два числа"""
    return a + b
```

**Translated file** (`src_en/module/example.py`):

```python
# This is a test function
def add(a, b):
    """Adds two numbers"""
    return a + b
```

