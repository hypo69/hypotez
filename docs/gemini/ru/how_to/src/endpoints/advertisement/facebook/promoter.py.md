### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предназначен для продвижения товаров и событий в группах Facebook. Он содержит классы и функции для автоматизации процесса публикации рекламных материалов, проверки интервалов между публикациями и обработки различных сценариев продвижения.

Шаги выполнения
-------------------------
1. **Инициализация класса `FacebookPromoter`**:
   - Создается экземпляр класса `FacebookPromoter`, который принимает драйвер WebDriver, имя промоутера и пути к файлам групп Facebook.

2. **Метод `promote`**:
   - Определяет, является ли продвигаемый элемент событием или сообщением.
   - Проверяет соответствие языка и валюты группы.
   - Вызывает соответствующие функции (`post_event` или `post_message`) для публикации в группе.
   - Обновляет данные группы после успешной публикации.

3. **Метод `process_groups`**:
   - Проходит по списку файлов групп Facebook.
   - Загружает данные групп из JSON-файла.
   - Фильтрует группы на основе категорий и статуса.
   - Получает элемент для продвижения (категорию или событие).
   - Проверяет, был ли уже продвинут данный элемент в группе.
   - Вызывает метод `promote` для публикации в группе.
   - Обновляет данные группы и сохраняет их в файл.

4. **Метод `get_category_item`**:
   - Получает информацию о категории для продвижения в зависимости от промоутера (`aliexpress` или другой).
   - Для `aliexpress` использует класс `AliCampaignEditor` для получения категорий и продуктов.
   - Для других промоутеров загружает данные из JSON-файла и выбирает случайную категорию.

5. **Метод `check_interval`**:
   - Проверяет, прошло ли достаточно времени с момента последней публикации в группе.

6. **Метод `get_event_url`**:
   - Формирует URL для создания события в Facebook группе на основе URL группы.

Пример использования
-------------------------

```python
from src.endpoints.advertisement.facebook.promoter import FacebookPromoter, get_event_url
from src.webdriver.driver import Driver, Chrome
from types import SimpleNamespace
import pytest

@pytest.fixture
def promoter_instance():
    # Инициализация драйвера и промоутера для тестов
    driver = Driver(Chrome)
    promoter = FacebookPromoter(d=driver, promoter='test_promoter')
    yield promoter
    driver.close()

def test_promote_method(promoter_instance):
    # Подготовка данных для теста
    group_data = {
        "group_url": "https://www.facebook.com/groups/1234567890",
        "group_categories": ["sales"],
        "status": "active",
        "language": "EN",
        "currency": "USD",
        "promoted_categories": [],
        "last_promo_sended": None
    }
    group = SimpleNamespace(**group_data)
    item = SimpleNamespace(category_name='Test Category', language=SimpleNamespace(EN='Test Message'))

    # Вызов метода promote
    result = promoter_instance.promote(group=group, item=item)
    assert result is None

def test_get_event_url():
    group_url = "https://www.facebook.com/groups/1234567890"
    event_url = get_event_url(group_url)
    assert "https://www.facebook.com/events/create/" in event_url
    assert "group_id=1234567890" in event_url
```