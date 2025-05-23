## Как использовать класс DDG
=========================================================================================

### Описание
-------------------------
Класс DDG предоставляет асинхронный генератор для взаимодействия с API DuckDuckGo AI Chat. 
Он позволяет отправить сообщение в чат-бот, получить ответ и обработать его.
DDG поддерживает различные модели, включая gpt-4o-mini, Llama-3.3-70B, Claude-3-Haiku, O3-Mini и Mistral-Small-24B.
Он также поддерживает потоковую обработку ответов, отправку системных сообщений и ведение истории чата.

### Шаги выполнения
-------------------------
1. **Инициализация**: Создайте экземпляр класса DDG.
2. **Выбор модели**: Укажите модель, которую вы хотите использовать, например, `model="gpt-4o-mini"`.
3. **Отправка сообщения**: Используйте метод `create_async_generator()` для отправки сообщения в чат-бот.
4. **Получение ответа**: Метод `create_async_generator()` возвращает асинхронный генератор, который вы можете использовать для получения частей ответа по мере их поступления.
5. **Обработка ответа**: Пройдите по генератору, используя цикл `async for`, чтобы обработать каждую часть ответа.

### Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.DDG import DDG

async def main():
    """Пример использования класса DDG для отправки сообщения в чат-бот DuckDuckGo."""

    # Создайте экземпляр класса DDG
    provider = DDG(model="gpt-4o-mini")

    # Отправьте сообщение
    async for response_part in provider.create_async_generator(messages=["Привет, мир!"]):
        # Обработайте части ответа
        print(response_part)

if __name__ == "__main__":
    asyncio.run(main())
```

### Дополнительная информация
-------------------------

- **Rate Limiting**: DDG реализует механизм ограничения скорости запросов, чтобы избежать блокировки IP-адреса.
- **Cookies**: Класс DDG автоматически обрабатывает cookies, необходимые для API DuckDuckGo.
- **X-VQD**: DDG автоматически извлекает и использует token X-VQD для аутентификации.
- **Retries**: DDG автоматически повторяет запросы при возникновении ошибок, чтобы повысить надежность.
- **История чата**: DDG сохраняет историю сообщений, что позволяет использовать контекст предыдущих сообщений при отправке новых.
- **System Messages**: DDG позволяет отправить системное сообщение, чтобы задать контекст для диалога.