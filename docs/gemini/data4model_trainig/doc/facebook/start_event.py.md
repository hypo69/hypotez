# Модуль для отправки мероприятий в группы Facebook

## Обзор

Модуль `src.endpoints.advertisement.facebook.start_event` предназначен для отправки мероприятий в группы Facebook.

## Подробней

Модуль использует веб-драйвер для автоматизации процесса публикации мероприятий в группах Facebook.

## Переменные

*   `d` (Driver): Экземпляр веб-драйвера Chrome.
*   `filenames` (list[str]): Список файлов, содержащих данные о группах.
*   `excluded_filenames` (list[str]): Список файлов, которые следует исключить.
*   `events_names` (list[str]): Список названий мероприятий.
*   `promoter` (FacebookPromoter): Экземпляр класса `FacebookPromoter` для управления продвижением.

## Как работает модуль

1.  Инициализируется веб-драйвер Chrome и открывается страница Facebook.
2.  Создается экземпляр класса `FacebookPromoter` с указанием веб-драйвера, списка файлов групп и флага отключения видео.
3.  В бесконечном цикле выполняются следующие действия:

    *   Логируется время начала работы.
    *   Вызывается метод `run_events` для отправки мероприятий в группы.
    *   Логируется время завершения работы.
    *   Ожидание в течение 7200 секунд (2 часа).

4.  При получении сигнала `KeyboardInterrupt` логируется сообщение о прерывании продвижения.

## Отсутствующие элементы

В предоставленном коде отсутствуют функции и методы для:

*   Определения списка мероприятий для отправки.
*   Реализации логики отправки мероприятий в группы Facebook.
*   Обработки возможных ошибок и исключений при отправке.