# Модуль исключений для работы с Mega.nz в Google Drive
## Обзор

Модуль содержит определения пользовательских исключений, используемых при работе с сервисом Mega.nz в Google Drive. Эти исключения позволяют обрабатывать специфические ошибки, которые могут возникнуть в процессе взаимодействия с Mega.nz, такие как неверный пароль или ошибки при выполнении запросов.

## Подробнее

Этот модуль предоставляет набор исключений для обработки ошибок, связанных с интеграцией Mega.nz и Google Drive. Исключения позволяют более точно определять причины сбоев и предпринимать соответствующие действия для их устранения.

## Классы

### `MegaException`

**Описание**: Базовый класс для всех исключений, связанных с Mega.

**Наследует**: `Exception`

**Атрибуты**: Отсутствуют

**Методы**: Отсутствуют

**Принцип работы**:
Класс `MegaException` служит базовым классом для всех пользовательских исключений, определенных в этом модуле. Он наследует класс `Exception` из стандартной библиотеки Python и не добавляет никакой дополнительной функциональности.

### `MegaIncorrectPasswordExcetion`

**Описание**: Исключение, которое выбрасывается, когда введен неверный пароль или email.

**Наследует**: `MegaException`

**Атрибуты**: Отсутствуют

**Методы**: Отсутствуют

**Принцип работы**:
Класс `MegaIncorrectPasswordExcetion` наследуется от `MegaException` и предназначен для обработки ситуаций, когда пользователь вводит неверные учетные данные (пароль или email) при попытке доступа к сервису Mega.

### `MegaRequestException`

**Описание**: Исключение, которое выбрасывается при возникновении ошибки в запросе к Mega.

**Наследует**: `MegaException`

**Атрибуты**: Отсутствуют

**Методы**: Отсутствуют

**Принцип работы**:
Класс `MegaRequestException` наследуется от `MegaException` и используется для обработки ошибок, которые могут возникнуть при выполнении запросов к сервису Mega. Это может быть связано с проблемами сети, неверными параметрами запроса или другими факторами.