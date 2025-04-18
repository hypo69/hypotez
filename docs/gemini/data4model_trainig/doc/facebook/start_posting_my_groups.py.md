# Модуль для запуска рекламных кампаний в Facebook (мои группы?)

## Обзор

Модуль `src.endpoints.advertisement.facebook.start_posting_my_groups` предназначен для отправки рекламных объявлений в группы Facebook (предположительно, в управляемые пользователем группы).

## Подробней

Модуль использует веб-драйвер для автоматизации процесса публикации рекламных объявлений в группах Facebook.

## Переменные

*   `d` (Driver): Экземпляр веб-драйвера Chrome.
*   `filenames` (list): Список файлов, содержащих данные о группах.
*   `campaigns` (list): Список рекламных кампаний.
*   `promoter` (FacebookPromoter): Экземпляр класса `FacebookPromoter` для управления продвижением.

## Как работает модуль

1.  Инициализируется веб-драйвер Chrome и открывается страница Facebook.
2.  Создается экземпляр класса `FacebookPromoter` с указанием веб-драйвера, списка файлов групп и флага отключения видео.
3.  В бесконечном цикле вызывается метод `run_campaigns` для отправки рекламных кампаний в группы.
4.  При получении сигнала `KeyboardInterrupt` логируется сообщение о прерывании продвижения.