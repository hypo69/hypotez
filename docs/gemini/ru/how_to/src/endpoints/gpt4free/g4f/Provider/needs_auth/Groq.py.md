### Как использовать блок кода Groq
=========================================================================================

Описание
-------------------------
Этот блок кода определяет класс `Groq`, который наследуется от класса `OpenaiTemplate`. Он содержит конфигурацию для взаимодействия с API Groq, включая URL, базовый URL API, флаги и список поддерживаемых моделей.

Шаги выполнения
-------------------------
1. Импортируется модуль `OpenaiTemplate` из относительного пути `..template`.
2. Определяется класс `Groq`, наследующийся от `OpenaiTemplate`.
3. Устанавливаются атрибуты класса:
    - `url`: URL для доступа к playground Groq.
    - `login_url`: URL для страницы ключей API Groq.
    - `api_base`: Базовый URL для API Groq.
    - `working`: Флаг, указывающий, что провайдер работает.
    - `needs_auth`: Флаг, указывающий, что требуется аутентификация.
    - `default_model`: Модель, используемая по умолчанию (`mixtral-8x7b-32768`).
    - `fallback_models`: Список резервных моделей.
    - `model_aliases`: Словарь с псевдонимами моделей.

Пример использования
-------------------------

```python
    from g4f.Provider.needs_auth import Groq

    groq_provider = Groq()

    print(f"URL: {groq_provider.url}")
    print(f"API Base: {groq_provider.api_base}")
    print(f"Default Model: {groq_provider.default_model}")
    print(f"Fallback Models: {groq_provider.fallback_models}")