### **Как использовать этот блок кода**

=========================================================================================

Описание
-------------------------
Этот код предназначен для автоматического получения и тестирования списка прокси-серверов, а также для выбора случайного рабочего прокси из этого списка. Он использует потоки для параллельного тестирования прокси и периодически обновляет список рабочих прокси.

Шаги выполнения
-------------------------
1. **Получение списка прокси**:
   - Функция `fetch_proxies` отправляет запрос на `https://www.proxy-list.download/api/v1/get?type=http` и извлекает список прокси-серверов в формате "IP:Port".
   - Если запрос выполнен успешно (код состояния 200), текст ответа разделяется на строки, и все строки, кроме последней, возвращаются в виде списка.
   - Если запрос не удался, выводится сообщение об ошибке и возвращается пустой список.

2. **Тестирование прокси**:
   - Функция `test_proxy` проверяет работоспособность заданного прокси-сервера.
   - Измеряется время, необходимое для выполнения запроса с использованием данного прокси.
   - Если время ответа меньше заданного таймаута, прокси считается рабочим, и информация о нем выводится в консоль.
   - Рабочий прокси добавляется в глобальный список `working_proxies` с помощью функции `add_working_proxy`.
   - Если во время тестирования прокси возникает исключение, оно игнорируется.

3. **Добавление рабочего прокси**:
   - Функция `add_working_proxy` добавляет прокси-сервер в глобальный список `working_proxies`.

4. **Удаление прокси**:
   - Функция `remove_proxy` удаляет прокси-сервер из глобального списка `working_proxies`, если он там присутствует.

5. **Получение рабочих прокси**:
   - Функция `get_working_proxies` получает список прокси-серверов с помощью `fetch_proxies` и запускает несколько потоков для параллельного тестирования каждого прокси с использованием функции `test_proxy`.
   - Каждый поток тестирует прокси с заданным `prompt` и `timeout`.
   - Потоки запускаются и ожидается их завершение в течение заданного времени `timeout`.

6. **Автоматическое обновление списка прокси**:
   - Функция `update_working_proxies` периодически обновляет глобальный список `working_proxies`.
   - Она вызывает `get_working_proxies` с тестовым запросом "What is the capital of France?" для получения и тестирования новых прокси.
   - Список прокси очищается перед каждым обновлением.
   - Функция выполняется в бесконечном цикле, обновляя список прокси каждые 30 минут.

7. **Получение случайного прокси**:
   - Функция `get_random_proxy` выбирает случайный прокси-сервер из глобального списка `working_proxies`.
   - Если список `working_proxies` пуст, будет вызвана ошибка `IndexError: list index out of range`.

Пример использования
-------------------------

```python
import random
import requests
import time
import threading

# Глобальный список рабочих прокси
working_proxies = []


def fetch_proxies():
    """Извлекает список прокси-серверов с proxyscrape.com.

    Returns:
        list: Список прокси-серверов в формате "IP:Port".
    """
    url = "https://www.proxy-list.download/api/v1/get?type=http"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.split("\\r\\n")[:-1]
    print(f"Ошибка при извлечении прокси: {response.status_code}")
    return []


def test_proxy(proxy, prompt, timeout):
    """Тестирует заданный прокси-сервер с указанным запросом и таймаутом.

    Args:
        proxy (str): Прокси-сервер в формате "IP:Port".
        prompt (str): Тестовый запрос, используемый для тестирования.
        timeout (int): Максимальное время в секундах, отведенное на тест.
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


def add_working_proxy(proxy):
    """Добавляет рабочий прокси-сервер в глобальный список working_proxies.

    Args:
        proxy (str): Прокси-сервер в формате "IP:Port".
    """
    global working_proxies
    working_proxies.append(proxy)


def remove_proxy(proxy):
    """Удаляет прокси-сервер из глобального списка working_proxies.

    Args:
        proxy (str): Прокси-сервер в формате "IP:Port".
    """
    global working_proxies
    if proxy in working_proxies:
        working_proxies.remove(proxy)


def get_working_proxies(prompt, timeout=5):
    """Извлекает и тестирует прокси-серверы, добавляя рабочие прокси в глобальный список working_proxies.

    Args:
        prompt (str): Тестовый запрос, используемый для тестирования.
        timeout (int, optional): Максимальное время в секундах, отведенное на тестирование. По умолчанию 5.
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
    """Непрерывно обновляет глобальный список working_proxies рабочими прокси-серверами."""
    global working_proxies
    test_prompt = "What is the capital of France?"

    while True:
        working_proxies = []  # Очищает список перед обновлением
        get_working_proxies(test_prompt)
        print('прокси обновлены')
        time.sleep(1800)  # Обновляет список прокси каждые 30 минут


def get_random_proxy():
    """Получает случайный рабочий прокси-сервер из глобального списка working_proxies.

    Returns:
        str: Случайный рабочий прокси-сервер в формате "IP:Port".
    """
    global working_proxies
    if not working_proxies:
        return None  # Возвращает None, если список прокси пуст
    return random.choice(working_proxies)


# Пример использования
if __name__ == '__main__':
    # Запуск обновления прокси в отдельном потоке
    proxy_updater = threading.Thread(target=update_working_proxies)
    proxy_updater.daemon = True  # Завершение потока вместе с основной программой
    proxy_updater.start()

    # Даем время на обновление списка прокси
    time.sleep(60)

    # Используем случайный прокси для запроса
    random_proxy = get_random_proxy()
    if random_proxy:
        print(f"Используем прокси: {random_proxy}")
        try:
            response = requests.get("https://www.google.com", proxies={"http": random_proxy, "https": random_proxy}, timeout=10)
            print(f"Статус код: {response.status_code}")
        except Exception as e:
            print(f"Ошибка при использовании прокси: {e}")
    else:
        print("Нет рабочих прокси в списке.")