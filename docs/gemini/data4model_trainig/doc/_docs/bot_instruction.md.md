# Инструкции для бота

!hi: Приветствует пользователя.
!train <data> <data_dir> <positive> <attachment>: Обучает модель с предоставленными данными. Используйте data для файла, data_dir для каталога или attachment для вложения файла.
!test <test_data>: Тестирует модель с предоставленными тестовыми данными в формате JSON.
!archive <directory>: Архивирует файлы в указанном каталоге.
!select_dataset <path_to_dir_positive> <positive>: Выбирает набор данных для обучения из указанного каталога.
!instruction: Отображает это сообщение с инструкциями.