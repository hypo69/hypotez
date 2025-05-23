### `campaign`  
**Описание**:  
Модуль `campaign` предназначен для управления процессом создания и публикации 
рекламных кампаний на Фейсбук. 
Он включает функционал для инициализации параметров кампании (название, язык, валюта), 
создания структуры директорий, сохранения конфигураций для новой кампании, 
сбора и сохранения данных о товарах через `ali` или `html`, 
генерации рекламных материалов, проверки кампании и публикации ее на Facebook.

```mermaid
flowchart TD
    A[Начало: Создание рекламной кампании для размещения на Facebook] --> B[Инициализация названия кампании, языка и валюты]
    B --> C[Создание директорий для кампании и категорий]
    C --> D[Сохранение конфигурации кампании]
    D --> E[Сбор данных о товарах]
    E --> F[Сохранение данных о товарах]
    F --> G[Создание рекламных материалов]
    G --> H[Проверка кампании]
    H --> I{Готова ли кампания?}
    I -- Да --> J[Публикация кампании на Facebook]
    I -- Нет --> H
    J --> K[Конец: Завершение создания рекламной кампании]
```