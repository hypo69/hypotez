# Модуль `g4f.client.service`
## Обзор
Модуль `g4f.client.service` предоставляет функции для выбора модели и провайдера для работы с GPT-4 Free API. 

## Детали

Этот модуль отвечает за определение модели и провайдера, используемых для обработки запросов к API GPT-4 Free. Он содержит функции, которые позволяют пользователю явно указать модель и провайдера или автоматически выбрать наиболее подходящие.

## Функции
### `convert_to_provider(provider: str) -> ProviderType`
#### Цель:
 Преобразует строковое представление провайдера в объект `ProviderType`.

#### Параметры:
- `provider` (str): Строковое представление провайдера.
#### Возвращает:
- `ProviderType`: Объект `ProviderType`, соответствующий провайдеру.

#### Исключения:
- `ProviderNotFoundError`: Если провайдер не найден.
#### Пример:
```python
>>> convert_to_provider('gpt4free')
<class 'g4f.providers.gpt4free.GPT4Free'>
```
### `get_model_and_provider(model: Union[Model, str], provider: Union[ProviderType, str, None], stream: bool, ignore_working: bool = False, ignore_stream: bool = False, logging: bool = True, has_images: bool = False) -> tuple[str, ProviderType]`
#### Цель:
 Получает модель и провайдера, основываясь на введенных параметрах.

#### Параметры:
- `model` (Union[Model, str]): Модель для использования, либо как объект, либо как строковый идентификатор.
- `provider` (Union[ProviderType, str, None]): Провайдер для использования, либо как объект, либо как строковый идентификатор, либо None.
- `stream` (bool): Указывает, следует ли выполнять операцию как поток.
- `ignore_working` (bool, optional): Если True, игнорирует состояние работы провайдера. По умолчанию False.
- `ignore_stream` (bool, optional): Если True, игнорирует возможность потоковой передачи провайдера. По умолчанию False.
- `logging` (bool, optional): Если True, записывает в лог информацию о выбранных модели и провайдере. По умолчанию True.
- `has_images` (bool, optional): Если True, предполагает, что запрос содержит изображения. По умолчанию False.
#### Возвращает:
- tuple[str, ProviderType]: Кортеж, содержащий имя модели и тип провайдера.
#### Исключения:
- `ProviderNotFoundError`: Если провайдер не найден.
- `ModelNotFoundError`: Если модель не найдена.
- `ProviderNotWorkingError`: Если провайдер не работает.
- `StreamNotSupportedError`: Если провайдер не поддерживает потоковую передачу.
#### Пример:
```python
>>> get_model_and_provider(model='gpt-3.5-turbo', provider='gpt4free', stream=False)
('gpt-3.5-turbo', <class 'g4f.providers.gpt4free.GPT4Free'>)
```
### `get_last_provider(as_dict: bool = False) -> Union[ProviderType, dict[str, str], None]`
#### Цель:
 Возвращает последний использованный провайдер.

#### Параметры:
- `as_dict` (bool, optional): Если True, возвращает информацию о провайдере в виде словаря. По умолчанию False.
#### Возвращает:
- Union[ProviderType, dict[str, str]]: Последний использованный провайдер, либо как объект, либо как словарь.
#### Пример:
```python
>>> get_last_provider()
<class 'g4f.providers.gpt4free.GPT4Free'>
```