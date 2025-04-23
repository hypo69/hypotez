### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Этот код предназначен для автоматического получения и тестирования прокси-серверов с целью их последующего использования в других частях приложения. Он включает в себя функции для загрузки списка прокси, проверки их работоспособности и добавления рабочих прокси в глобальный список.

Шаги выполнения
-------------------------
1. **Извлечение списка прокси**: Функция `fetch_proxies` отправляет запрос на сайт `www.proxy-list.download` и извлекает список прокси-серверов в формате "IP:Port". Если запрос выполнен успешно (код состояния 200), список прокси возвращается. В противном случае выводится сообщение об ошибке.

2. **Тестирование прокси**: Функция `test_proxy` проверяет работоспособность заданного прокси-сервера, используя тестовый запрос. Если прокси проходит проверку в пределах заданного времени ожидания (`timeout`), он добавляется в список рабочих прокси-серверов.

3. **Добавление рабочего прокси**: Функция `add_working_proxy` добавляет прокси-сервер в глобальный список `working_proxies`.

4. **Удаление прокси**: Функция `remove_proxy` удаляет прокси-сервер из глобального списка `working_proxies`.

5. **Получение рабочих прокси**: Функция `get_working_proxies` получает список прокси-серверов, создает потоки для их одновременной проверки и добавляет рабочие прокси в глобальный список `working_proxies`.

6. **Обновление рабочих прокси**: Функция `update_working_proxies` периодически обновляет список рабочих прокси-серверов, очищая его перед каждым обновлением.

7. **Получение случайного прокси**: Функция `get_random_proxy` возвращает случайный рабочий прокси-сервер из глобального списка `working_proxies`.

Пример использования
-------------------------

```python
import random
import requests
import time
import threading

# Глобальный список для хранения рабочих прокси
working_proxies = []

def fetch_proxies():
    """
    Функция извлекает список прокси-серверов с сайта proxyscrape.com.

    Returns:
        list: Список прокси-серверов в формате "IP:Port".
    """
    url = "https://www.proxy-list.download/api/v1/get?type=http"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.split("\\r\\n")[:-1]
    print(f"Ошибка при извлечении прокси: {response.status_code}")
    return []


def test_proxy(proxy: str, prompt: str, timeout: int):
    """
    Функция тестирует заданный прокси-сервер с указанным запросом и временем ожидания.

    Args:
        proxy (str): Прокси-сервер в формате "IP:Port".
        prompt (str): Тестовый запрос для использования при тестировании.
        timeout (int): Максимальное время в секундах, допустимое для теста.
    """
    try:
        start_time = time.time()
        # res = gpt3.Completion.create(prompt=prompt, proxy=proxy)
        end_time = time.time()
        response_time = end_time - start_time

        if response_time < timeout:
            response_time = int(response_time * 1000)
            print(f'прокси: {proxy} [{response_time}ms] ✅')
            add_working_proxy((proxy))
    except Exception as e:
        pass


def add_working_proxy(proxy: str):
    """
    Функция добавляет рабочий прокси-сервер в глобальный список working_proxies.

    Args:
        proxy (str): Прокси-сервер в формате "IP:Port".
    """
    global working_proxies
    working_proxies.append(proxy)


def remove_proxy(proxy: str):
    """
    Функция удаляет прокси-сервер из глобального списка working_proxies.

    Args:
        proxy (str): Прокси-сервер в формате "IP:Port".
    """
    global working_proxies
    if proxy in working_proxies:
        working_proxies.remove(proxy)


def get_working_proxies(prompt: str, timeout: int = 5):
    """
    Функция извлекает и тестирует прокси-серверы, добавляя рабочие прокси в глобальный список working_proxies.

    Args:
        prompt (str): Тестовый запрос для использования при тестировании.
        timeout (int, optional): Максимальное время в секундах, допустимое для тестирования. По умолчанию 5.
    """
    proxy_list = fetch_proxies()
    threads = []

    for proxy in proxy_list:
        thread = threading.Thread(target=test_proxy, args=(
            proxy, prompt, timeout))
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join(timeout)


def update_working_proxies():
    """
    Функция непрерывно обновляет глобальный список working_proxies рабочими прокси-серверами.
    """
    global working_proxies
    test_prompt = "What is the capital of France?"

    while True:
        working_proxies = []  # Очистка списка перед обновлением
        get_working_proxies(test_prompt)
        print('прокси обновлены')
        time.sleep(1800)  # Обновление списка прокси каждые 30 минут


def get_random_proxy():
    """
    Функция получает случайный рабочий прокси-сервер из глобального списка working_proxies.

    Returns:
        str: Случайный рабочий прокси-сервер в формате "IP:Port".
    """
    global working_proxies
    return random.choice(working_proxies)

# Пример использования:
# Запуск обновления прокси в отдельном потоке
update_thread = threading.Thread(target=update_working_proxies)
update_thread.daemon = True  # Позволяет завершить поток при завершении основной программы
update_thread.start()

# Получение случайного прокси для использования
# time.sleep(60)  # Даем время наполниться списку прокси
# random_proxy = get_random_proxy()
# print(f"Случайный рабочий прокси: {random_proxy}")