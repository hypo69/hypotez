## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода реализует юнит-тесты для функций, отвечающих за получение cookies и работу с запросами в модуле `g4f`.

Шаги выполнения
-------------------------
1. **Инициализация тестового класса:** Создается класс `TestImport`, наследующий от `unittest.TestCase`, для запуска юнит-тестов.
2. **Тест `test_get_cookies`:**
    -  Импортируются две функции: `get_cookies_alias` и `get_cookies`.
    -  Проверяется, что эти функции являются одной и той же (синонимы) с помощью `self.assertEqual`. 
3. **Тест `test_requests`:**
    -  Импортируется класс `StreamSession` из модуля `g4f.requests`.
    -  Проверяется, что `StreamSession` является классом, используя `self.assertIsInstance(StreamSession, type)`.
4. **Запуск тестов:**  Если код выполняется напрямую (не импортируется как модуль), запускаются все тесты с помощью `unittest.main()`.

Пример использования
-------------------------

```python
import unittest

class TestImport(unittest.TestCase):

    def test_get_cookies(self):
        from g4f import get_cookies as get_cookies_alias
        from g4f.cookies import get_cookies
        self.assertEqual(get_cookies_alias, get_cookies)

    def test_requests(self):
        from g4f.requests import StreamSession
        self.assertIsInstance(StreamSession, type)

if __name__ == '__main__':
    unittest.main()
```

Этот код демонстрирует, как добавить юнит-тесты для проверки функциональности модуля `g4f`.