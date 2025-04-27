# Исключения для Mega API 

## Обзор

Модуль `exceptions.py` предоставляет набор исключений, используемых для обработки ошибок, возникающих во время взаимодействия с Mega API.

## Детали

Этот модуль используется для выявления различных ошибок, которые могут возникнуть при работе с API Mega. Он обеспечивает структуру для обработки исключений, что позволяет разработчику эффективно реагировать на возникшие проблемы.

## Классы

### `class MegaException`

**Описание**: Базовый класс для всех исключений, связанных с Mega API.

**Методы**: 
 - `__init__(self, message: str = "")`: Инициализирует экземпляр класса `MegaException`. 

**Принцип действия**: Этот класс служит основой для всех остальных исключений в данном модуле. Он используется для обработки любых общих ошибок, возникающих при взаимодействии с Mega API. 

**Примеры**: 

```python
    try:
        # Код, который может вызвать исключение MegaException
        ...
    except MegaException as ex:
        logger.error(f"Произошла ошибка MegaException: {ex}", ex, exc_info=True)
```

### `class MegaIncorrectPasswordExcetion`

**Описание**: Исключение, которое возникает, если был введен неверный пароль или адрес электронной почты.

**Методы**:
 - `__init__(self, message: str = "")`: Инициализирует экземпляр класса `MegaIncorrectPasswordExcetion`. 

**Принцип действия**:  Это исключение сигнализирует о том, что предоставленный пароль или адрес электронной почты неверны. 

**Примеры**: 

```python
    try:
        # Код, который может вызвать исключение MegaIncorrectPasswordExcetion
        ...
    except MegaIncorrectPasswordExcetion as ex:
        logger.error(f"Произошла ошибка MegaIncorrectPasswordExcetion: {ex}", ex, exc_info=True)
```

### `class MegaRequestException`

**Описание**: Исключение, которое возникает, если в запросе была ошибка.

**Методы**:
 - `__init__(self, message: str = "")`: Инициализирует экземпляр класса `MegaRequestException`. 

**Принцип действия**:  Это исключение указывает на наличие ошибки в запросе, отправленном на API Mega. 

**Примеры**: 

```python
    try:
        # Код, который может вызвать исключение MegaRequestException
        ...
    except MegaRequestException as ex:
        logger.error(f"Произошла ошибка MegaRequestException: {ex}", ex, exc_info=True)
```