# Модуль поиска свободного порта

## Обзор

Модуль `src/utils/port.py` предоставляет функцию `get_free_port` для поиска свободного порта на указанном хосте. Функция может работать как с заданным диапазоном портов, так и с поиском первого доступного порта, если диапазон не задан.

## Подробней

Данный модуль используется в проекте `hypotez` для автоматического определения доступных портов при запуске различных сервисов. 

## Функции

### `get_free_port`

**Назначение**: Функция `get_free_port` проверяет доступность портов на указанном хосте, и возвращает свободный порт.

**Параметры**:
- `host` (str): Адрес хоста для проверки доступности портов.
- `port_range` (Optional[Union[str, List[Union[str, List[int]]]]], optional): Диапазон(ы) портов. Может быть строкой "min-max", списком строк "min-max", списком списков чисел [min, max] или None. По умолчанию None.

**Возвращает**:
- `int`: Номер доступного порта.

**Вызывает исключения**:
- `ValueError`: Если не удалось найти свободный порт в указанном диапазоне(ах) или если формат диапазона некорректен.

**Как работает функция**:
1. Функция `get_free_port` принимает адрес хоста и диапазон портов. 
2. Если диапазон не задан (port_range is None), она начинает поиск с порта 1024 и увеличивает его, пока не найдет свободный порт.
3. Если задан диапазон или список диапазонов, функция перебирает все порты в указанном диапазоне и возвращает первый свободный.
4. Функция использует внутреннюю функцию `_is_port_in_use` для проверки занятости порта.
5. `_is_port_in_use` создает сокет и пытается привязать его к указанному адресу и порту. Если привязка удалась, значит, порт свободен, иначе порт занят.
6. Если не удалось найти свободный порт ни в одном из заданных диапазонов, выбрасывается исключение `ValueError`.

**Примеры**:

```python
>>> get_free_port('localhost', '3000-3005')
3001
>>> get_free_port('localhost', ['4000-4005', [5000, 5010]])
5002
```

### **Внутренние функции**

#### `_is_port_in_use`

**Назначение**: Функция `_is_port_in_use` проверяет, используется ли данный порт на указанном хосте.

**Параметры**:
- `host` (str): Адрес хоста.
- `port` (int): Номер порта для проверки.

**Возвращает**:
- `bool`: True, если порт используется, False в противном случае.

**Как работает функция**:
1. Функция создает сокет с использованием контекстного менеджера для автоматического закрытия.
2. Она пытается привязать сокет к адресу и порту. Если привязка удалась, значит, порт свободен.
3. Если произошла ошибка OSError (например, "Address already in use"), значит, порт занят.
4. Если возникла другая ошибка, функция логирует ее с использованием `logger.error` и возвращает `True`.

#### `_parse_port_range`

**Назначение**: Функция `_parse_port_range` парсит строку диапазона портов "min-max" в кортеж (min_port, max_port).

**Параметры**:
- `port_range_str` (str): Строка диапазона портов.

**Возвращает**:
- `Tuple[int, int]`: Кортеж, содержащий минимальный и максимальный номера портов.

**Вызывает исключения**:
- `ValueError`: Если формат строки диапазона портов некорректен.

**Как работает функция**:
1. Функция разделяет строку по символу "-".
2. Проверяет, что получилось ровно две части.
3. Преобразует части в целые числа.
4. Проверяет корректность диапазона (минимум меньше максимума) и допустимость номеров портов (от 0 до 65535).
5. Возвращает кортеж (min_port, max_port).

```markdown