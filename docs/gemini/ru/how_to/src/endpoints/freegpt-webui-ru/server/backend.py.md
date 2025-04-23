### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код реализует API для общения с языковой моделью, используя библиотеку `g4f`. Он включает в себя функциональность для обработки запросов, взаимодействия с моделью, добавления веб-результатов и инструкций jailbreak, а также управления прокси.

Шаги выполнения
-------------------------
1. **Инициализация API**: Класс `Backend_Api` инициализируется с Flask app и конфигурацией. Он определяет маршруты для обработки запросов.
2. **Обработка запроса на разговор**: Функция `_conversation` обрабатывает POST-запросы к маршруту `/backend-api/v2/conversation`.
3. **Построение сообщения**: Функция `build_messages` создает контекст для запроса к языковой модели, включая системное сообщение, историю разговора, веб-результаты и инструкции jailbreak.
4. **Получение веб-результатов**: Функция `fetch_search_results` выполняет поиск в интернете с использованием DuckDuckGo API и добавляет результаты в контекст разговора.
5. **Генерация ответа**: Функция `generate_stream` генерирует ответ от языковой модели, учитывая инструкции jailbreak, если они включены.
6. **Проверка Jailbreak**: Функция `isJailbreak` добавляет специальные инструкции в зависимости от выбранного jailbreak.
7. **Установка языка ответа**: Функция `set_response_language` определяет язык запроса и устанавливает соответствующее требование для ответа.

Пример использования
-------------------------

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# Здесь должна быть ваша конфигурация
config = {
    'use_auto_proxy': False
}

# Инициализация API
backend_api = Backend_Api(app, config)

# Добавление маршрутов из API в Flask app
for route, data in backend_api.routes.items():
    app.add_url_rule(route, view_func=data['function'], methods=data['methods'])

# Пример запроса
@app.route('/test', methods=['POST'])
def test():
    # Пример данных запроса
    data = {
        'stream': True,
        'jailbreak': 'Default',
        'model': 'gpt-3.5-turbo',
        'meta': {
            'content': {
                'conversation': [],
                'internet_access': False,
                'parts': [{'role': 'user', 'content': 'Hello, how are you?'}]
            }
        }
    }
    
    # Эмуляция запроса
    with app.test_request_context('/backend-api/v2/conversation', method='POST', json=data):
        response = backend_api._conversation()
        return response

if __name__ == '__main__':
    app.run(debug=True)