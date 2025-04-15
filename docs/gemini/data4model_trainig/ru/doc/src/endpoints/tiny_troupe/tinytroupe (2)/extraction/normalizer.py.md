# Модуль для нормализации текстовых элементов
=================================================

Модуль содержит класс :class:`Normalizer`, который используется для нормализации текстовых элементов, таких как пассажи, концепции и другие.

Пример использования
----------------------

```python
normalizer = Normalizer(elements=['элемент1', 'элемент2'], n=2, verbose=True)
normalized_elements = normalizer.normalize(['элемент1', 'элемент3'])
```

## Обзор

Модуль `normalizer.py` предоставляет функциональность для нормализации текстовых элементов с использованием API OpenAI. Он включает класс `Normalizer`, который позволяет нормализовать список элементов и кэшировать результаты для повышения производительности.

## Подробнее

Этот модуль предназначен для нормализации текстовых данных, чтобы привести их к единообразному виду. Он использует OpenAI для обработки и нормализации входных элементов, а также кэширует результаты, чтобы избежать повторной обработки одних и тех же элементов. Это особенно полезно при работе с большими объемами текста, где требуется быстрая и эффективная нормализация.

## Классы

### `Normalizer`

**Описание**: Класс для нормализации текстовых элементов.

**Атрибуты**:
- `elements` (List[str]): Список элементов для нормализации.
- `n` (int): Количество нормализованных элементов для вывода.
- `verbose` (bool): Флаг для отображения отладочных сообщений.
- `normalized_elements` (dict): JSON-структура, где каждый выходной элемент является ключом к списку входных элементов, объединенных в него.
- `normalizing_map` (dict): Словарь, который сопоставляет каждый входной элемент с его нормализованным выводом (используется как кэш).

**Методы**:
- `__init__(elements: List[str], n: int, verbose: bool = False)`: Инициализирует экземпляр класса `Normalizer`.
- `normalize(element_or_elements: Union[str, List[str]]) -> Union[str, List[str]]`: Нормализует указанный элемент или элементы.

#### `__init__`

```python
def __init__(self, elements: List[str], n: int, verbose: bool = False):
    """
    Инициализирует экземпляр класса `Normalizer`.

    Args:
        elements (List[str]): Список элементов для нормализации.
        n (int): Количество нормализованных элементов для вывода.
        verbose (bool, optional): Флаг для отображения отладочных сообщений. По умолчанию `False`.
    """
```

**Назначение**: Инициализирует объект `Normalizer`, подготавливая его к нормализации элементов.

**Параметры**:
- `elements` (List[str]): Список элементов, которые необходимо нормализовать. Преобразуется в уникальный список.
- `n` (int): Количество нормализованных элементов, которые необходимо вывести.
- `verbose` (bool, optional): Флаг, определяющий, нужно ли выводить отладочные сообщения. По умолчанию `False`.

**Как работает функция**:
- Инициализирует атрибуты `elements`, `n` и `verbose` экземпляра класса.
- Компонирует сообщения для языковой модели (LLM) с использованием шаблонов Mustache.
- Отправляет сообщение в OpenAI API для получения нормализованных элементов.
- Извлекает результаты в формате JSON из ответа OpenAI.
- Сохраняет нормализованные элементы в атрибуте `normalized_elements`.

**Примеры**:

```python
normalizer = Normalizer(elements=['элемент1', 'элемент2'], n=2, verbose=True)
```

#### `normalize`

```python
def normalize(self, element_or_elements: Union[str, List[str]]) -> Union[str, List[str]]:
    """
    Нормализует указанный элемент или элементы.

    Args:
        element_or_elements (Union[str, List[str]]): Элемент или элементы для нормализации.

    Returns:
        Union[str, List[str]]: Нормализованный элемент или элементы.
    """
```

**Назначение**: Нормализует один или несколько элементов, используя кэширование для повышения производительности.

**Параметры**:
- `element_or_elements` (Union[str, List[str]]): Элемент (строка) или список элементов (строк) для нормализации.

**Возвращает**:
- Union[str, List[str]]: Нормализованный элемент (строка), если на входе была строка, или список нормализованных элементов (строк), если на входе был список.

**Как работает функция**:
1. **Определяет тип входных данных**: Проверяет, является ли входной параметр строкой или списком. Если это строка, преобразует ее в список.
2. **Использует кэш**: Проверяет, есть ли элементы для нормализации в кэше (`self.normalizing_map`). Если элемент уже нормализован, он пропускается.
3. **Вызывает OpenAI API для новых элементов**: Для элементов, которых нет в кэше, отправляет запрос в OpenAI API для получения нормализованных значений.
4. **Обновляет кэш**: Сохраняет нормализованные элементы в кэше (`self.normalizing_map`).
5. **Возвращает нормализованные элементы**: Возвращает нормализованные элементы в том же порядке, в котором они были переданы на вход.

**Примеры**:

```python
normalizer = Normalizer(elements=['элемент1', 'элемент2'], n=2)
normalized_element = normalizer.normalize('элемент1')
normalized_elements = normalizer.normalize(['элемент1', 'элемент3'])
```
```python
def normalize(self, element_or_elements: Union[str, List[str]]) -> Union[str, List[str]]:
    """
    Нормализует указанный элемент или элементы.

    Этот метод использует механизм кэширования для повышения производительности. Если элемент был нормализован ранее, 
    его нормализованная форма хранится в кэше (self.normalizing_map). Когда один и тот же элемент необходимо 
    снова нормализовать, метод сначала проверит кэш и использует сохраненную нормализованную форму, если она доступна, 
    вместо повторной нормализации элемента.

    Порядок элементов на выходе будет таким же, как и на входе. Это обеспечивается обработкой 
    элементов в том порядке, в котором они появляются на входе, и добавлением нормализованных элементов в выходной 
    список в том же порядке.

    Args:
        element_or_elements (Union[str, List[str]]): Элемент или элементы для нормализации.

    Returns:
        str: Нормализованный элемент, если на входе была строка.
        list: Нормализованные элементы, если на входе был список, сохраняя порядок элементов на входе.
    """
    if isinstance(element_or_elements, str):
        denormalized_elements = [element_or_elements]
    elif isinstance(element_or_elements, list):
        denormalized_elements = element_or_elements
    else:
        raise ValueError("The element_or_elements must be either a string or a list.")
    
    normalized_elements = []
    elements_to_normalize = []
    for element in denormalized_elements:
        if element not in self.normalizing_map:
            elements_to_normalize.append(element)
    
    if elements_to_normalize:
        rendering_configs = {"categories": self.normalized_elements,
                                "elements": elements_to_normalize}
        
        messages = utils.compose_initial_LLM_messages_with_templates("normalizer.applier.system.mustache", "normalizer.applier.user.mustache",                                  
                                                                 base_module_folder="extraction",
                                                                 rendering_configs=rendering_configs)
        
        next_message = openai_utils.client().send_message(messages, temperature=0.1)
        
        debug_msg = f"Normalization result message: {next_message}"
        logger.debug(debug_msg)
        if self.verbose:
            print(debug_msg)

        normalized_elements_from_llm = utils.extract_json(next_message["content"])
        assert isinstance(normalized_elements_from_llm, list), "The normalized element must be a list."
        assert len(normalized_elements_from_llm) == len(elements_to_normalize), "The number of normalized elements must be equal to the number of elements to normalize."

        for i, element in enumerate(elements_to_normalize):
            normalized_element = normalized_elements_from_llm[i]
            self.normalizing_map[element] = normalized_element
    
    for element in denormalized_elements:
        normalized_elements.append(self.normalizing_map[element])
    
    return normalized_elements
```

**Внутренние функции**:
Внутри данной функции нету внутренних функций.

## Параметры класса

- `elements` (List[str]): Список элементов, которые необходимо нормализовать.
- `n` (int): Количество нормализованных элементов, которые необходимо вывести.
- `verbose` (bool): Флаг, определяющий, нужно ли выводить отладочные сообщения.
- `normalized_elements` (dict): Структура, содержащая нормализованные элементы.
- `normalizing_map` (dict): Словарь для кэширования нормализованных элементов.