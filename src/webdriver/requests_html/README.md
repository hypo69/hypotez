# 🧑‍💻 How-to: Использование `requests-html` и `pyppeteer` для загрузки и парсинга HTML + JavaScript

Модуль **`requests-html`** — альтернатива `requests` + `BeautifulSoup`, позволяющая скачивать HTML, **рендерить JavaScript**, и т.п. в небольших проектах или в среде без сложных ограничений.

---

## 📦 Установка

```bash
pip install requests-html
```

Это автоматически установит и `pyppeteer`, который нужен для рендеринга JS-контента через Chromium.

---

## 🔧 Основные возможности `requests-html`

```python
from requests_html import HTMLSession

session = HTMLSession()
r = session.get('https://example.com')

# Парсинг HTML
title = r.html.find('title', first=True).text

# Поиск всех ссылок
links = r.html.find('a')
for link in links:
    print(link.attrs.get('href'))

# Рендеринг JavaScript (см. инструкции ниже)
r.html.render()
```

---

## ⚠️ Рендеринг JavaScript

`requests-html` использует `pyppeteer` (Python-обёртка для Chromium) для исполнения JavaScript.

### При первом вызове `r.html.render()`:

* `pyppeteer` скачивает Chromium (\~100–150 MB)
* Устанавливает его в:

  * Windows: `C:\Users\<User>\AppData\Local\pyppeteer`
  * Linux/macOS: `~/.pyppeteer/`

---

## 🛠 Автоматическая установка Chromium при запуске

```python
from requests_html import HTMLSession
from pyppeteer import chromium_downloader, executablePath
import os

def ensure_chromium_installed() -> None:
    """
    Проверяет наличие бинарника Chromium и при необходимости загружает его.
    """
    if not os.path.exists(executablePath()):
        print("Chromium не найден. Скачиваю...")
        chromium_downloader.download_chromium()
        print("Chromium успешно установлен.")
    else:
        print("Chromium уже установлен.")

def fetch_with_js(url: str, timeout: int = 20) -> str:
    """
    Загружает страницу с рендерингом JavaScript.

    Args:
        url (str): URL целевой страницы.
        timeout (int, optional): Таймаут рендеринга. По умолчанию 20 секунд.

    Returns:
        str: HTML содержимое страницы после рендеринга.
    """
    ensure_chromium_installed()

    session = HTMLSession()
    response = session.get(url)
    response.html.render(timeout=timeout)
    return response.html.html


# Пример использования
if __name__ == "__main__":
    html = fetch_with_js("https://quotes.toscrape.com/js/")
    print(html[:500])  # выводим первые 500 символов
```

---

## ❗ Возможные ошибки и решения

| Ошибка                                 | Причина                        | Решение                                   |
| -------------------------------------- | ------------------------------ | ----------------------------------------- |
| `RuntimeError: Failed to launch`       | Chromium не найден             | Установить: `python -m pyppeteer install` |
| `TimeoutError while rendering`         | Слишком долго загружается сайт | Увеличить `timeout`: `render(timeout=60)` |
| `ImportError: No module named asyncio` | Слишком старая версия Python   | Обновить до Python 3.7+                   |

---

## 📂 Ручная установка Chromium (если автоматическая не сработала)

```bash
python -m pyppeteer install
```

или в Python:

```python
from pyppeteer import chromium_downloader
chromium_downloader.download_chromium()
```

---

## 💡 Использование `pyppeteer` напрямую (вместо `requests-html`)

Можно использовать `pyppeteer` работы напрямую с headless-браузером,:

```bash
pip install pyppeteer
```

```python
import asyncio
from pyppeteer import launch

async def main():
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto('https://example.com')
    content = await page.content()
    print(content[:500])
    await browser.close()

asyncio.run(main())
```

### Полезные параметры:

```python
browser = await launch(
    headless=True,
    args=[
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage'
    ]
)
```

---

## 🧱 Использование Chromium вручную (если установлен отдельно)

Если у тебя уже есть Chrome/Chromium, можно указать путь вручную:

```python
r.html.render(executablePath='C:/Path/To/chrome.exe')
```

Или при запуске `pyppeteer`:

```python
browser = await launch(executablePath='/path/to/chrome')
```

---


Да, **с помощью `requests-html` ты можешь работать с веб-элементами**, но с **ограничениями**:

---

## ✅ Что `requests-html` умеет с веб-элементами

После выполнения:

```python
r.html.render()
```

ты получаешь **полноценный DOM**, и можешь:

* искать элементы (`find`, `xpath`, `css`)
* извлекать:

  * `.text`
  * `.attrs` (например, `href`, `src`)
  * `.html`
* получать списки элементов
* переходить по вложенным тегам

### Пример:

```python
from requests_html import HTMLSession

session = HTMLSession()
r = session.get('https://quotes.toscrape.com/js/')
r.html.render()

# Получаем все цитаты на странице
quotes = r.html.find('.quote')

for quote in quotes:
    text = quote.find('.text', first=True).text
    author = quote.find('.author', first=True).text
    print(f"{text} — {author}")
```

---

## ❌ Что `requests-html` НЕ умеет с взаимодействовать веб-элементами, как это делают:

* `Selenium`
* `Playwright`
* `pyppeteer` (напрямую)
* `pydoll` (напрямую)


| Недоступное действие             | Альтернатива                                           |
| -------------------------------- | ------------------------------------------------------ |
| Кликать (`click()`)              | Использовать `pyppeteer` или `selenium` или `pydoll`   |
| Вводить текст (`type()`)         | То же                                                  |
| Наводить курсор (`hover()`)      | То же                                                  |
| Прокручивать страницу (`scroll`) | То же                                                  |
| Получать computed styles         | Только через JS в `pyppeteer`                          |

---

## 💡 Альтернатива: использовать `pyppeteer` напрямую

```python
import asyncio
from pyppeteer import launch

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://quotes.toscrape.com/js/')
    
    # Клик по кнопке
    await page.click('button.load-more')

    # Ввод текста
    await page.type('#search', 'keyword')

    # Получение текста
    quote = await page.querySelectorEval('.quote', '(el) => el.innerText')
    print(quote)

    await browser.close()

asyncio.run(main())
```

---




## 🧠 Альтернативы `requests-html`

| Библиотека                    | Особенности                                                       |
| --------------------------    | ----------------------------------------------------------------- |
| `requests + BeautifulSoup`    | Классика, без поддержки JavaScript                                |
| `httpx + selectolax`          | Быстро, асинхронно                                                |
| `playwright`                  | Современная, мощная альтернатива для JS                           |
| `selenium`                    | Полный контроль над браузером, медленнее                          |
| `Pydoll`                      | Ассинхронная библиотека напрямую работающая с браузером Chоrmium  |

---


