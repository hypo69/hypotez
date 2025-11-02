# **Шаблон Gemini: Полное форматирование кода**

---

```

```

## **1. Шапка файла**

### Python

```python
# @file <filename.py>
# <ОСНОВНОЕ НАЗНАЧЕНИЕ МОДУЛЯ / КОДА>  # ==================================
# Детальное описание функционала модуля, классов, функций и использования
# Примеры: демонстрация основных функций модуля
# ========================================================================
```

### **JS/TS**

```javascript
// @file <filename.js/ts>
// <ОСНОВНОЕ НАЗНАЧЕНИЕ КОДА>  # ==================================
// Детальное описание работы модуля, его функций, классов и примеров использования
// ========================================================================
```

### **PHP**

```php
<?php
/**
 * @file <filename.php>
 * @description <ОСНОВНОЕ НАЗНАЧЕНИЕ КОДА>
 * Детальное описание функционала модуля и примеры использования
 */
```

### **CSS/SCSS**

```css
/* 
@file <filename.css/scss>

Описаное примененных классов  
# ==================================
Детальное описание назначения стилей, классов и элементов интерфейса

*/
```

```

```

---

## **2. Функции**

### **Python**

```python
from typing import Optional, List, Dict, Any

def function_name(
    param1: str,
    param2: Optional[int] = None,
    param3: List[str] | None = None
) -> Dict[str, Any]:
    """
    Функция выполняет основное действие и возвращает результат в виде словаря.

    Args:
        param1 (str): Описание параметра `param1`.
        param2 (Optional[int], optional): Описание параметра `param2`. По умолчанию `None`.
        param3 (List[str] | None, optional): Список дополнительных параметров. По умолчанию `None`.

    Returns:
        Dict[str, Any]: Результат выполнения функции.

    Raises:
        ValueError: Если входные данные некорректны.
        RuntimeError: Если выполнение функции завершилось с ошибкой.

    Example:
        >>> function_name("test", 10, ["a", "b"])
        {'result': 'ok'}
    """
    # Объявление переменных в начале функции
    result: Dict[str, Any] = {}
    temp_value: Optional[str] = None

    # Проверка условий перед выполнением логики
    if not param1:
        raise ValueError("param1 не должен быть пустым")

    # Логика функции
    temp_value = param1.upper()
    result["value"] = temp_value
    ...
    return result
```

### **JS/TS (JSDoc)**

```javascript
/**
 * Выполняет основное действие с переданными данными.
 *
 * @param {string} param1 - Основной параметр.
 * @param {number} [param2] - Дополнительный числовой параметр.
 * @param {Array<string>} [param3] - Дополнительные строки.
 * @returns {Object} Результат выполнения функции.
 * @throws {Error} Если параметры некорректны.
 *
 * @example
 * const result = functionName("test", 10, ["a","b"]);
 */
function functionName(param1, param2 = null, param3 = []) {
    if (!param1) throw new Error("param1 не должен быть пустым");
    const result = {};
    ...
    return result;
}
```

### **PHP (PHPDoc)**

```php
<?php
/**
 * Выполняет основное действие с переданными данными
 *
 * @param string $param1 Основной параметр
 * @param int|null $param2 Дополнительный числовой параметр
 * @param array|null $param3 Дополнительные строки
 * @return array Результат выполнения функции
 * @throws InvalidArgumentException Если параметры некорректны
 */
function functionName(string $param1, ?int $param2 = null, ?array $param3 = null): array {
    if (!$param1) {
        throw new InvalidArgumentException("param1 не должен быть пустым");
    }
    $result = [];
    ...
    return $result;
}
```

---

## **3. Классы**

### **Python**

```python
class ExampleClass:
    """
    Класс ExampleClass реализует функциональность управления данными.

    Attributes:
        config (Dict[str, Any]): Настройки класса.
        name (str): Имя объекта.
    """

    def __init__(self, config: Dict[str, Any], name: str) -> None:
        """
        Инициализация класса ExampleClass.

        Args:
            config (Dict[str, Any]): Настройки объекта.
            name (str): Имя объекта.
        """
        self.config: Dict[str, Any] = config
        self.name: str = name

    def execute_action(self, value: str) -> bool:
        """
        Выполняет основное действие класса с переданным значением.

        Args:
            value (str): Значение для обработки.

        Returns:
            bool: Результат выполнения действия.

        Raises:
            RuntimeError: Если выполнение действия невозможно.

        Example:
            >>> obj = ExampleClass({}, "test")
            >>> obj.execute_action("data")
            True
        """
        if not value:
            raise RuntimeError("Передано пустое значение")
        ...
        return True
```

### **JS/TS**

```javascript
/**
 * Класс реализует управление данными.
 */
class ExampleClass {
    /**
     * @param {Object} config - Настройки объекта
     * @param {string} name - Имя объекта
     */
    constructor(config, name) {
        this.config = config;
        this.name = name;
    }

    /**
     * Выполняет действие с переданным значением.
     * @param {string} value - Значение для обработки
     * @returns {boolean} Результат выполнения
     * @throws {Error} Если значение пустое
     */
    executeAction(value) {
        if (!value) throw new Error("Передано пустое значение");
        ...
        return true;
    }
}
```

### **PHP**

```php
<?php
/**
 * Класс реализует управление данными
 */
class ExampleClass {
    private array $config;
    private string $name;

    /**
     * @param array $config Настройки объекта
     * @param string $name Имя объекта
     */
    public function __construct(array $config, string $name) {
        $this->config = $config;
        $this->name = $name;
    }

    /**
     * Выполняет действие с переданным значением
     *
     * @param string $value Значение для обработки
     * @return bool Результат выполнения
     * @throws RuntimeException Если значение пустое
     */
    public function executeAction(string $value): bool {
        if (!$value) {
            throw new RuntimeException("Передано пустое значение");
        }
        ...
        return true;
    }
}
```

---

## **4. Комментарии внутри кода**

* **Обязательные правила** :
* Всегда предшествуют коду, который описывают
* Использовать точные термины: «Извлечение», «Проверка», «Вызов функции», «Применение стилей»
* Исключать разговорные или служебные выражения: «делаем», «отправляем», «создаем», «открываем»
* `...` оставлять без изменений
* **Пример корректного комментария в Python** :

```python
# Проверка наличия файла перед его обработкой
if not file_path.exists():
    raise FileNotFoundError(f"Файл не найден: {file_path}")
```

* **Пример корректного комментария в JS/TS** :

```javascript
// Проверка наличия элемента на странице перед вызовом метода
if (!element) throw new Error("Элемент не найден");
```

* **Пример корректного комментария в PHP** :

```php
// Проверка наличия ключа в массиве перед обработкой
if (!array_key_exists('key', $data)) {
    throw new InvalidArgumentException("Ключ отсутствует");
}
```
