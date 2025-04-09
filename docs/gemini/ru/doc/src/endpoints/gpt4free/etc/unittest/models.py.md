# Документация модуля `models.py`

## Обзор

Модуль содержит юнит-тесты для проверки наличия моделей у провайдеров и их работоспособности в контексте проекта `hypotez`. Он использует библиотеку `unittest` для автоматизированного тестирования, а также модуль `g4f` для получения информации о моделях и провайдерах.

## Подробней

Данный модуль предназначен для автоматической проверки соответствия моделей, поддерживаемых различными провайдерами, и убеждается, что все провайдеры функционируют корректно. Это важная часть системы контроля качества, гарантирующая, что интеграция с различными AI-моделями работает как ожидается.

## Классы

### `TestProviderHasModel`

**Описание**: Класс, содержащий юнит-тесты для проверки наличия моделей у провайдеров и их работоспособности.

**Наследует**: `unittest.TestCase`

**Атрибуты**:

- `cache` (dict): Статический атрибут класса, используемый для кэширования результатов вызова `provider.get_models()`, чтобы избежать повторных вызовов и ускорить выполнение тестов.

**Методы**:

- `test_provider_has_model()`: Тестовый метод, который итерируется по всем моделям и провайдерам, определенным в `__models__`, и проверяет, что каждый провайдер, реализующий `ProviderModelMixin`, имеет соответствующую модель в своем списке `model_aliases` или использует имя модели по умолчанию.
- `provider_has_model(provider: Type[BaseProvider], model: str)`: Метод, проверяющий наличие указанной модели в списке моделей, предоставляемых указанным провайдером.
- `test_all_providers_working()`: Тестовый метод, который итерируется по всем моделям и провайдерам и проверяет, что атрибут `working` у каждого провайдера имеет значение `True`.

## Функции

### `test_provider_has_model`

```python
def test_provider_has_model(self):
    """
    Проверяет, что каждый провайдер имеет соответствующие модели.

    Args:
        self (TestProviderHasModel): Экземпляр класса TestProviderHasModel.

    Returns:
        None

    Raises:
        AssertionError: Если провайдер не имеет ожидаемую модель.

    Example:
        >>> test_provider = TestProviderHasModel()
        >>> test_provider.test_provider_has_model()
    """
```

**Назначение**: Этот метод выполняет итерацию по всем зарегистрированным моделям и провайдерам, чтобы убедиться, что каждый провайдер, реализующий `ProviderModelMixin`, поддерживает заявленные модели.

**Как работает функция**:

1.  **Инициализация цикла по моделям и провайдерам**: Происходит перебор всех моделей и связанных с ними провайдеров, хранящихся в `__models__.values()`.
2.  **Проверка на `ProviderModelMixin`**: Для каждого провайдера проверяется, является ли он подклассом `ProviderModelMixin`. Этот класс-миксин указывает на то, что провайдер должен предоставлять информацию о поддерживаемых моделях.
3.  **Определение имени модели**: Если провайдер имеет атрибут `model_aliases`, то используется соответствующий псевдоним модели. В противном случае используется стандартное имя модели.
4.  **Вызов `provider_has_model`**: Вызывается метод `self.provider_has_model` для фактической проверки наличия модели у провайдера.

**ASCII flowchart**:

```
Начало --> Перебор моделей и провайдеров (Модель, Провайдер)
|
V
Провайдер является подклассом ProviderModelMixin?
|
Да --> Получение имени модели (Псевдоним или стандартное имя)
|
V
Вызов provider_has_model(Провайдер, Имя модели)
|
V
Конец
```

**Примеры**:

```python
class TestProviderHasModelExample(unittest.TestCase):
    def test_provider_has_model_example(self):
        # Создаем экземпляр класса TestProviderHasModel
        test_instance = TestProviderHasModel()
        
        # Вызываем метод test_provider_has_model (предполагая, что __models__ уже определен)
        test_instance.test_provider_has_model()
```

### `provider_has_model`

```python
def provider_has_model(self, provider: Type[BaseProvider], model: str):
    """
    Проверяет, что провайдер поддерживает указанную модель.

    Args:
        provider (Type[BaseProvider]): Класс провайдера для проверки.
        model (str): Имя модели для проверки.

    Returns:
        None

    Raises:
        AssertionError: Если провайдер не поддерживает указанную модель.

    Example:
        >>> from g4f.providers import ChatBase
        >>> test_provider = TestProviderHasModel()
        >>> test_provider.provider_has_model(ChatBase, "gpt-3.5-turbo")
    """
```

**Назначение**: Этот метод проверяет, присутствует ли указанная модель в списке моделей, поддерживаемых данным провайдером.

**Как работает функция**:

1.  **Проверка кэша**: Сначала проверяется, есть ли в кэше (`self.cache`) информация о моделях, поддерживаемых данным провайдером. Если информации нет, делается попытка получить список моделей с помощью `provider.get_models()`.
2.  **Обработка исключений**: Если при получении списка моделей возникают исключения `MissingRequirementsError` или `MissingAuthError`, функция завершает работу, чтобы не прерывать выполнение тестов из-за отсутствия зависимостей или аутентификации.
3.  **Проверка наличия модели**: Если список моделей получен успешно, проверяется, присутствует ли в нем указанная модель. Если модель отсутствует, вызывается `self.assertIn` для генерации ошибки.

**ASCII flowchart**:

```
Начало --> Проверка кэша провайдера
|
V
Информация в кэше?
|
Нет --> Попытка получения списка моделей (provider.get_models())
|    |
|    V
|    Исключение (MissingRequirementsError, MissingAuthError)?
|       |
|       Да --> Выход
|       |
|    Нет --> Проверка наличия модели в списке
|
Да --> Конец
|
V
Генерация ошибки (assertIn)
|
V
Конец
```

**Примеры**:

```python
class TestProviderHasModelExample(unittest.TestCase):
    def test_provider_has_model_example(self):
        # Создаем экземпляр класса TestProviderHasModel
        test_instance = TestProviderHasModel()
        
        # Пример вызова функции provider_has_model с ChatBase и "gpt-3.5-turbo"
        # Предполагается, что ChatBase и gpt-3.5-turbo существуют и доступны
        from g4f.providers import ChatBase
        test_instance.provider_has_model(ChatBase, "gpt-3.5-turbo")
```

### `test_all_providers_working`

```python
def test_all_providers_working(self):
    """
    Проверяет, что все провайдеры находятся в рабочем состоянии.

    Args:
        self (TestProviderHasModel): Экземпляр класса TestProviderHasModel.

    Returns:
        None

    Raises:
        AssertionError: Если провайдер не работает.

    Example:
        >>> test_provider = TestProviderHasModel()
        >>> test_provider.test_all_providers_working()
    """
```

**Назначение**: Этот метод проверяет, что все провайдеры, связанные с моделями, находятся в рабочем состоянии (атрибут `working` имеет значение `True`).

**Как работает функция**:

1.  **Инициализация цикла по моделям и провайдерам**: Происходит перебор всех моделей и связанных с ними провайдеров, хранящихся в `__models__.values()`.
2.  **Проверка атрибута `working`**: Для каждого провайдера проверяется значение атрибута `working`. Если атрибут имеет значение `False`, вызывается `self.assertTrue` для генерации ошибки и сообщения о том, какой провайдер не работает.

**ASCII flowchart**:

```
Начало --> Перебор моделей и провайдеров (Модель, Провайдер)
|
V
Провайдер.working == True?
|
Да --> Конец
|
V
Генерация ошибки (assertTrue)
|
V
Конец
```

**Примеры**:

```python
class TestProviderHasModelExample(unittest.TestCase):
    def test_all_providers_working_example(self):
        # Создаем экземпляр класса TestProviderHasModel
        test_instance = TestProviderHasModel()
        
        # Вызываем метод test_all_providers_working
        test_instance.test_all_providers_working()