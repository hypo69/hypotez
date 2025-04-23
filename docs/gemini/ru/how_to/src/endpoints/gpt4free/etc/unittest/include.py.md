### Как использовать этот блок кода

=========================================================================================

Описание
-------------------------
Этот блок кода содержит модульные тесты для проверки правильности импорта функций и классов из библиотеки `g4f`. Он проверяет, что функция `get_cookies` может быть импортирована как с помощью алиаса, так и напрямую, и что класс `StreamSession` является типом.

Шаги выполнения
-------------------------
1. **Импорт модулей**: Импортируется модуль `unittest` для написания тестов.
2. **Создание тестового класса**: Создается класс `TestImport`, наследующийся от `unittest.TestCase`, который содержит тестовые методы.
3. **Тест `test_get_cookies`**:
   - Импортируется функция `get_cookies` из `g4f` как `get_cookies_alias` и напрямую из `g4f.cookies`.
   - Проверяется, что `get_cookies_alias` и `get_cookies` ссылаются на одну и ту же функцию, используя метод `assertEqual`.
4. **Тест `test_requests`**:
   - Импортируется класс `StreamSession` из `g4f.requests`.
   - Проверяется, что `StreamSession` является типом (то есть классом), используя метод `assertIsInstance`.
5. **Запуск тестов**: Блок `if __name__ == '__main__':` гарантирует, что тесты будут запущены только при непосредственном выполнении этого файла.

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