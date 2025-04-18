# Документация модуля exceptions.py

## Обзор

Модуль `exceptions.py` содержит определения пользовательских исключений, используемых в модуле `mega` для обработки специфических ошибок, возникающих при взаимодействии с Mega API.

## Подробней

Этот модуль предоставляет классы исключений, которые наследуются от базового класса `MegaException`. Эти исключения позволяют более точно обрабатывать ошибки, возникающие при работе с Mega API, такие как неверный пароль или ошибки в запросах. Использование пользовательских исключений улучшает читаемость и поддерживаемость кода, позволяя конкретно идентифицировать и обрабатывать различные типы ошибок.

## Классы

### `MegaException`

**Описание**: Базовый класс для всех исключений, специфичных для модуля `mega`.

**Как работает класс**: Этот класс служит родительским для всех остальных исключений, определенных в модуле. Он наследуется от стандартного класса `Exception` и не содержит дополнительной логики. Его основная цель - предоставить общий тип исключений для модуля `mega`.

### `MegaIncorrectPasswordExcetion`

**Описание**: Исключение, которое выбрасывается, когда предоставлен неверный пароль или email.

**Как работает класс**: Этот класс наследуется от `MegaException` и используется для сигнализации о том, что введен неверный пароль или email при попытке аутентификации в Mega API.

### `MegaRequestException`

**Описание**: Исключение, которое выбрасывается при возникновении ошибки в запросе к Mega API.

**Как работает класс**: Этот класс наследуется от `MegaException` и используется для сигнализации об ошибках, возникающих при выполнении запросов к Mega API.