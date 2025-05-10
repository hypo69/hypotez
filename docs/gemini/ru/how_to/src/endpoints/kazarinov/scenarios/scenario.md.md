## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода представляет собой сценарий для автоматизации создания "мехирона" для Сергея Казаринова. 
Сценарий использует библиотеку `selenium` для сбора данных с веб-страниц, 
`src.ai.gemini` для обработки данных с помощью AI, а также библиотеку 
`src.endpoints.advertisement.facebook.scenarios` для публикации обработанных 
данных в Facebook. 

Шаги выполнения
-------------------------
1. **Инициализация WebDriver**: Создаётся экземпляр класса `Driver` для управления 
браузером.
2. **Инициализация MexironBuilder**: Создаётся экземпляр класса `MexironBuilder` 
с использованием ранее инициализированного WebDriver. 
3. **Запуск сценария**: Вызывается метод `run_scenario` класса `MexironBuilder` с 
необходимыми параметрами (например, URL-адреса товаров).
4. **Сбор данных**: Сценарий выполняет следующие действия:
    - Проверяет, есть ли URL-адреса для парсинга, и, если да, получает данные
    с помощью соответствующего грабера.
    - Парсит полученные данные и конвертирует их в требуемый формат.
    - Сохраняет данные в файл.
5. **Обработка данных AI**:  Обработка данных осуществляется с помощью 
`src.ai.gemini`. 
6. **Создание отчётов**:  Создаются HTML- и PDF-отчёты с обработанными данными.
7. **Публикация в Facebook**:  Обработанные данные публикуются в Facebook с 
помощью `src.endpoints.advertisement.facebook.scenarios`.


Пример использования
-------------------------

```python
from src.webdriver.driver import Driver
from src.endpoints.kazarinov.scenarios.scenario_pricelist import MexironBuilder

# Initialize Driver
driver = Driver(...)

# Initialize MexironBuilder
mexiron_builder = MexironBuilder(driver)

# Run Scenario
urls = ['https://example.com/product1', 'https://example.com/product2']
mexiron_builder.run_scenario(urls=urls)
```