## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Блок кода запускает набор юнит-тестов для модуля `gpt4free`.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: 
   - Импортирует модуль `unittest` для запуска юнит-тестов.
   - Импортирует модуль `g4f.debug` для отладки.
   - Импортирует все подмодули из директории `unittest`, включая `asyncio`, `backend`, `main`, `model`, `client`, `image_client`, `include`, `retry_provider`, `thinking`, `web_search`, `models`.

2. **Отключение проверки версии**:
   - Выключает проверку версии модуля `g4f` с помощью `g4f.debug.version_check = False`.

3. **Запуск юнит-тестов**:
   - Выполняет команду `unittest.main()`, которая запускает все тесты, найденные в импортированных подмодулях.

Пример использования
-------------------------
```python
    import unittest

    import g4f.debug

    g4f.debug.version_check = False

    from .asyncio import *
    from .backend import *
    from .main import *
    from .model import *
    from .client import *
    from .image_client import *
    from .include import *
    from .retry_provider import *
    from .thinking import *
    from .web_search import *
    from .models import *

    unittest.main()
```

Этот код запускает все юнит-тесты, написанные для модуля `gpt4free`. Тесты проверяют правильность работы различных функций и классов, обеспечивая стабильность и надежность кода.