### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код предназначен для извлечения ссылок на отдельные чаты из веб-страницы `chatgpt.com`. Он использует веб-драйвер (Chrome или Firefox) для навигации по странице и локаторы, определенные в JSON-файле, чтобы найти и извлечь необходимые ссылки.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются модули, такие как `header`, `gs`, `Driver`, `Chrome`, `Firefox`, и `j_loads_ns`.
2. **Загрузка локаторов**: Функция `j_loads_ns` загружает локаторы из файла `chats_list.json`, который содержит информацию о том, как находить элементы на веб-странице.
3. **Определение функции `get_links`**: Эта функция принимает объект `Driver` (веб-драйвер) в качестве аргумента.
4. **Извлечение ссылок**: Функция `d.execute_locator(locator.link)` использует локатор `link` для поиска всех элементов ссылок на странице и возвращает их.
5. **Инициализация и использование драйвера (в `if __name__ == '__main__'`**:
   - Создается экземпляр драйвера `Driver` (в данном случае, Firefox).
   - Драйвер переходит по URL `https://chatgpt.com/`.
   - Функция `get_links` вызывается для получения ссылок на чаты.

Пример использования
-------------------------

```python
import header
from src import gs
from src.webdriver.driver import Driver
from src.webdriver.chrome import Chrome
from src.webdriver.firefox import Firefox
from src.utils.jjson import j_loads_ns

locator = j_loads_ns(gs.path.src / 'suppliers' / 'chat_gpt' / 'locators' / 'chats_list.json')

def get_links(d: Driver):
    """Ссылки на отдельные чаты"""
    links = d.execute_locator(locator.link)
    return links

if __name__ == '__main__':
    d = Driver(Firefox)
    d.get_url('https://chatgpt.com/')
    links = get_links(d)
    # Далее можно обработать полученные ссылки
    for link in links:
        print(link)
```