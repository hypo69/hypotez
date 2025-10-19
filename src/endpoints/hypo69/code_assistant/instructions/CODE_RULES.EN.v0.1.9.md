

# **Gemini Template: Full Code Formatting (English)**

---

## **1. File Header**

### **Python**

```python
# @file <filename.py>
# <MAIN PURPOSE OF THE MODULE / CODE>  # ==================================
# Detailed description of module functionality, classes, functions, and usage
# Examples: demonstration of main module functions
# ========================================================================
```

### **JS/TS**

```javascript
// @file <filename.js/ts>
// <MAIN PURPOSE OF THE CODE>  # ==================================
// Detailed description of module functionality, classes, functions, and usage
// ========================================================================
```

### **PHP**

```php
<?php
/**
 * @file <filename.php>
 * @description <MAIN PURPOSE OF THE CODE>
 * Detailed description of module functionality and usage examples
 */
```

### **CSS/SCSS**

```css
/* 
@file <filename.css/scss>
<MAIN PURPOSE OF THE CODE>  # ==================================
Detailed description of purpose of styles, classes, and UI elements
*/
```

---

## **2. Functions**

### **Python**

```python
from typing import Optional, List, Dict, Any

def function_name(
    param1: str,
    param2: Optional[int] = None,
    param3: List[str] | None = None
) -> Dict[str, Any]:
    """
    Function performs main action and returns result as a dictionary.

    Args:
        param1 (str): Description of `param1`.
        param2 (Optional[int], optional): Description of `param2`. Defaults to `None`.
        param3 (List[str] | None, optional): List of additional parameters. Defaults to `None`.

    Returns:
        Dict[str, Any]: Result of function execution.

    Raises:
        ValueError: If input data is invalid.
        RuntimeError: If function execution fails.

    Example:
        >>> function_name("test", 10, ["a", "b"])
        {'result': 'ok'}
    """
    # Declare variables at the beginning
    result: Dict[str, Any] = {}
    temp_value: Optional[str] = None

    # Precondition check
    if not param1:
        raise ValueError("param1 must not be empty")

    # Function logic
    temp_value = param1.upper()
    result["value"] = temp_value
    ...
    return result
```

### **JS/TS (JSDoc)**

```javascript
/**
 * Performs main action with provided data.
 *
 * @param {string} param1 - Main parameter.
 * @param {number} [param2] - Optional numeric parameter.
 * @param {Array<string>} [param3] - Optional array of strings.
 * @returns {Object} Result of execution.
 * @throws {Error} If parameters are invalid.
 *
 * @example
 * const result = functionName("test", 10, ["a","b"]);
 */
function functionName(param1, param2 = null, param3 = []) {
    if (!param1) throw new Error("param1 must not be empty");
    const result = {};
    ...
    return result;
}
```

### **PHP (PHPDoc)**

```php
<?php
/**
 * Performs main action with provided data.
 *
 * @param string $param1 Main parameter
 * @param int|null $param2 Optional numeric parameter
 * @param array|null $param3 Optional array of strings
 * @return array Result of function execution
 * @throws InvalidArgumentException If parameters are invalid
 */
function functionName(string $param1, ?int $param2 = null, ?array $param3 = null): array {
    if (!$param1) {
        throw new InvalidArgumentException("param1 must not be empty");
    }
    $result = [];
    ...
    return $result;
}
```

---

## **3. Classes**

### **Python**

```python
class ExampleClass:
    """
    ExampleClass implements data management functionality.

    Attributes:
        config (Dict[str, Any]): Class configuration.
        name (str): Object name.
    """

    def __init__(self, config: Dict[str, Any], name: str) -> None:
        """
        Initialize ExampleClass instance.

        Args:
            config (Dict[str, Any]): Object settings.
            name (str): Object name.
        """
        self.config: Dict[str, Any] = config
        self.name: str = name

    def execute_action(self, value: str) -> bool:
        """
        Performs main class action with the provided value.

        Args:
            value (str): Value for processing.

        Returns:
            bool: Execution result.

        Raises:
            RuntimeError: If action cannot be executed.

        Example:
            >>> obj = ExampleClass({}, "test")
            >>> obj.execute_action("data")
            True
        """
        if not value:
            raise RuntimeError("Empty value provided")
        ...
        return True
```

### **JS/TS**

```javascript
/**
 * Class implements data management functionality.
 */
class ExampleClass {
    /**
     * @param {Object} config - Object configuration
     * @param {string} name - Object name
     */
    constructor(config, name) {
        this.config = config;
        this.name = name;
    }

    /**
     * Executes action with provided value.
     * @param {string} value - Value to process
     * @returns {boolean} Result of execution
     * @throws {Error} If value is empty
     */
    executeAction(value) {
        if (!value) throw new Error("Empty value provided");
        ...
        return true;
    }
}
```

### **PHP**

```php
<?php
/**
 * Class implements data management functionality
 */
class ExampleClass {
    private array $config;
    private string $name;

    /**
     * @param array $config Object configuration
     * @param string $name Object name
     */
    public function __construct(array $config, string $name) {
        $this->config = $config;
        $this->name = $name;
    }

    /**
     * Executes action with provided value
     *
     * @param string $value Value to process
     * @return bool Result of execution
     * @throws RuntimeException If value is empty
     */
    public function executeAction(string $value): bool {
        if (!$value) {
            throw new RuntimeException("Empty value provided");
        }
        ...
        return true;
    }
}
```

---

## **4. Inline Comments**

* **Rules** :
* Precede the code they describe
* Use precise terms: “Extraction”, “Validation”, “Function call”, “Apply styles”
* Avoid conversational or procedural expressions: “do”, “send”, “create”, “open”
* Leave `...` unchanged

 **Python example** :

```python
# Validate file existence before processing
if not file_path.exists():
    raise FileNotFoundError(f"File not found: {file_path}")
```

 **JS/TS example** :

```javascript
// Validate element exists before method call
if (!element) throw new Error("Element not found");
```

 **PHP example** :

```php
// Check if key exists in array before processing
if (!array_key_exists('key', $data)) {
    throw new InvalidArgumentException("Key is missing");
}
```
