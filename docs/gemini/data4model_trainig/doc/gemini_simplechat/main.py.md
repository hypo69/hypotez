# Модуль простого чата с использованием Gemini

## Обзор

Модуль `src.endpoints.gemini_simplechat.main` реализует простой чат с использованием модели Google Gemini. Он предоставляет API для взаимодействия с моделью Gemini и возвращает ответы на запросы.

## Подробней

Модуль использует FastAPI для создания веб-сервера, который принимает запросы на чат и возвращает ответы, сгенерированные моделью Gemini. Он также настраивает CORS для разрешения запросов с разных доменов.

## Функции

### `root`

```python
@app.get("/", response_class=HTMLResponse)
async def root():
    try:
        html_content = Path( __root__ / gs.fast_api.index_path).read_text(encoding="utf-8")
        return HTMLResponse(content=html_content)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error reading templates:{str(ex)}" )
```

**Назначение**: Обрабатывает GET-запросы к корневому пути ("/").

**Как работает функция**:

1.  Читает содержимое HTML-файла, расположенного по пути `__root__ / gs.fast_api.index_path`.
2.  Возвращает HTML-контент в качестве ответа.
3.  В случае ошибки при чтении файла генерирует исключение `HTTPException` с кодом состояния 500 и детальным описанием ошибки.

### `chat`

```python
@app.post("/api/chat")
async def chat(request: ChatRequest):
    global model
    try:
        response = await model.chat(request.message)
        return {"response": response}
    except Exception as ex:
        logger.error(f"Error in chat: ",ex)
        raise HTTPException(status_code=500, detail=str(e))
```

**Назначение**: Обрабатывает POST-запросы к пути "/api/chat".

**Параметры**:

*   `request` (ChatRequest): Запрос, содержащий сообщение для чата.

**Как работает функция**:

1.  Вызывает метод `chat` объекта `model` (экземпляр класса `GoogleGenerativeAi`), передавая ему сообщение из запроса.
2.  Возвращает ответ в формате JSON, содержащий сгенерированный моделью ответ.
3.  В случае ошибки логирует информацию об ошибке и генерирует исключение `HTTPException` с кодом состояния 500 и детальным описанием ошибки.

## Переменные

*   `app` (FastAPI): Экземпляр класса FastAPI для создания веб-сервера.
*   `system_instruction` (str): Системная инструкция, прочитанная из файла "instructions/system\_instruction.md".
*   `model` (GoogleGenerativeAi): Экземпляр класса GoogleGenerativeAi для взаимодействия с моделью Gemini.

## Запуск приложения

Для запуска приложения необходимо выполнить файл `main.py`:

```bash
python src/endpoints/gemini_simplechat/main.py
```

Приложение будет запущено на хосте и порту, указанных в `gs.fast_api.host` и `gs.fast_api.port` соответственно.