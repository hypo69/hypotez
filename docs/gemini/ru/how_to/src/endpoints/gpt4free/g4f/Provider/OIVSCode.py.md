### **Инструкция по использованию блока кода**

=========================================================================================

Описание
-------------------------
Этот код определяет класс `OIVSCode`, который является подклассом `OpenaiTemplate`. Он предоставляет конфигурацию для использования модели `gpt-4o-mini-2024-07-18` через сервер OI VSCode. Класс определяет URL-адреса API, поддерживает потоковую передачу, системные сообщения и историю сообщений.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируется `OpenaiTemplate` из `.template`.

2. **Определение класса `OIVSCode`**:
   - Класс `OIVSCode` наследуется от `OpenaiTemplate`.
   - Устанавливаются атрибуты класса:
     - `label`: Отображаемое имя провайдера ("OI VSCode Server").
     - `url`: Базовый URL сервера ("https://oi-vscode-server.onrender.com").
     - `api_base`: URL для API ("https://oi-vscode-server-2.onrender.com/v1").
     - `working`: Указывает, что провайдер работает (`True`).
     - `needs_auth`: Указывает, что не требуется аутентификация (`False`).
     - `supports_stream`: Указывает, что поддерживается потоковая передача (`True`).
     - `supports_system_message`: Указывает, что поддерживаются системные сообщения (`True`).
     - `supports_message_history`: Указывает, что поддерживается история сообщений (`True`).
     - `default_model`: Модель, используемая по умолчанию ("gpt-4o-mini-2024-07-18").
     - `default_vision_model`: Модель для обработки изображений по умолчанию (`default_model`).
     - `vision_models`: Список моделей, поддерживающих обработку изображений.
     - `models`: Список всех поддерживаемых моделей, включая `vision_models` и "deepseek-ai/DeepSeek-V3".
     - `model_aliases`: Словарь псевдонимов моделей для упрощения использования.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.OIVSCode import OIVSCode

# Создание экземпляра класса OIVSCode
oivscode = OIVSCode()

# Вывод информации о провайдере
print(f"Label: {oivscode.label}")
print(f"URL: {oivscode.url}")
print(f"Default model: {oivscode.default_model}")

# Пример использования псевдонима модели
default_model = oivscode.model_aliases.get("gpt-4o-mini")
print(f"Alias for gpt-4o-mini: {default_model}")