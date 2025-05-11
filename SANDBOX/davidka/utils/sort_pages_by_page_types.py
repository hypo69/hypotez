## \file /sandbox/davidka/sort_pages_by_page_types.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль сортировки JSON файлов по page_type. из директории `supplier_files` в поддиректории `supplier_files_by_page_type` по page_type.
========================================================================================================================================
Sort JSON files by page_type from the `supplier_files` directory into subdirectories `supplier_files_by_page_type` by page_type.


```rst
 .. module:: sandbox.davidka.sort_pages_by_page_types
```
"""
import json
import os
import glob
from collections import defaultdict
import shutil # Для удобной очистки тестовых директорий в примере

def sort_by_page_type(input_base_dir, output_base_dir, chunk_size=100):
    """
    Рассортировывает словари из JSON файлов (найденных рекурсивно в input_base_dir)
    по page_type. Все элементы одного page_type собираются вместе и сохраняются
    в соответствующую поддиректорию в output_base_dir (например, output_base_dir/products/).
    Файлы в этих поддиректориях разбиваются на чанки.
    Обработанные словари удаляются из исходных файлов.

    Args:
        input_base_dir (str): Путь к базовой входной директории с JSON файлами.
        output_base_dir (str): Путь к базовой выходной директории для сохранения.
        chunk_size (int): Максимальное количество ключей в одном выходном файле-чанке.
    """
    if not os.path.isdir(input_base_dir):
        print(f"Ошибка: Базовая входная директория '{input_base_dir}' не найдена.")
        return
    if chunk_size <= 0:
        print(f"Ошибка: Размер чанка (chunk_size) должен быть положительным числом.")
        return

    os.makedirs(output_base_dir, exist_ok=True)
    print(f"Файлы будут обрабатываться из: {os.path.abspath(input_base_dir)}")
    print(f"Результаты будут сохранены в: {os.path.abspath(output_base_dir)}")
    print(f"Максимальный размер файла (количество ключей на чанк): {chunk_size}")

    # Глобальная агрегация данных по page_type со всех файлов
    aggregated_data_by_type = defaultdict(dict)

    # Рекурсивный поиск JSON файлов во всех поддиректориях input_base_dir
    json_files = glob.glob(os.path.join(input_base_dir, '**', '*.json'), recursive=True)

    if not json_files:
        print(f"В директории '{input_base_dir}' и ее поддиректориях не найдено JSON файлов.")
        return

    processed_files_count = 0

    for filepath in json_files:
        print(f"\nОбработка файла: {filepath}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print(f"  Ошибка: Не удалось декодировать JSON из файла {filepath}. Файл пропущен.")
            continue
        except Exception as e:
            print(f"  Ошибка при чтении файла {filepath}: {e}. Файл пропущен.")
            continue

        if not isinstance(data, dict):
            print(f"  Предупреждение: Содержимое файла {filepath} не является словарем. Файл пропущен.")
            continue

        items_to_keep_in_original_file = {} 
        urls_to_process = list(data.keys())

        items_extracted_from_this_file = 0
        for url in urls_to_process:
            item_data = data.get(url)
            if not isinstance(item_data, dict):
                items_to_keep_in_original_file[url] = item_data
                continue

            page_type = item_data.get("page_type")

            if page_type and isinstance(page_type, str):
                # Добавляем элемент в ГЛОБАЛЬНЫЕ агрегированные данные
                # Если URL уже существует для этого page_type (из другого файла),
                # данные из последнего обработанного файла перезапишут предыдущие.
                aggregated_data_by_type[page_type][url] = item_data
                items_extracted_from_this_file += 1
            else:
                # Элементы без page_type или с некорректным page_type остаются в исходном файле
                items_to_keep_in_original_file[url] = item_data
        
        if items_extracted_from_this_file > 0:
            print(f"  Извлечено {items_extracted_from_this_file} элементов с 'page_type' из {filepath}.")
        
        # Перезаписываем исходный файл
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(items_to_keep_in_original_file, f, indent=4, ensure_ascii=False)
            
            if not items_to_keep_in_original_file and items_extracted_from_this_file > 0:
                 print(f"  Исходный файл {filepath} теперь пуст (все подходящие элементы извлечены).")
            elif items_to_keep_in_original_file and items_extracted_from_this_file > 0 :
                 print(f"  Исходный файл {filepath} обновлен, {len(items_to_keep_in_original_file)} элементов сохранено в нем.")
            # Если items_extracted_from_this_file == 0, файл не должен был измениться.
            
        except Exception as e:
            print(f"  Ошибка при записи обновленного исходного файла {filepath}: {e}")
        
        processed_files_count +=1

    # --- Сохранение агрегированных данных в отдельные директории по page_type ---
    if not aggregated_data_by_type:
        print("\nНе найдено элементов с 'page_type' для сортировки во всех обработанных файлах.")
        return
        
    print("\nСохранение агрегированных данных по категориям page_type...")
    total_output_chunks_created = 0

    for page_type, all_items_for_type in aggregated_data_by_type.items():
        if not all_items_for_type: continue

        # Формируем безопасное имя для директории и базовое имя файла из page_type
        safe_page_type_name = "".join(c if c.isalnum() or c in ('_', '-') else '_' for c in page_type.lower())
        if not safe_page_type_name: 
            safe_page_type_name = "unnamed_page_type"
        
        # Создаем целевую директорию для этого page_type
        target_page_type_dir = os.path.join(output_base_dir, safe_page_type_name)
        os.makedirs(target_page_type_dir, exist_ok=True)

        # Очищаем директорию от старых *.json чанков ПЕРЕД записью новых
        # Это важно, чтобы удалить файлы, которые могли остаться от предыдущих запусков,
        # если количество элементов или их распределение по URL изменилось.
        print(f"  Очистка и подготовка директории: {target_page_type_dir}")
        for old_file in glob.glob(os.path.join(target_page_type_dir, '*.json')):
            try:
                os.remove(old_file)
                # print(f"    Удален старый файл: {old_file}") # Для отладки
            except OSError as e:
                print(f"    Ошибка при удалении старого файла {old_file}: {e}")
        
        items_list = list(all_items_for_type.items())
        total_items = len(items_list)
        num_chunks = (total_items + chunk_size - 1) // chunk_size

        print(f"  Для page_type '{page_type}' (всего {total_items} элементов) будет создано {num_chunks} чанк(ов) в '{target_page_type_dir}'.")

        for i in range(num_chunks):
            chunk_number = i + 1 
            start_index = i * chunk_size
            end_index = start_index + chunk_size
            
            current_chunk_list = items_list[start_index:end_index]
            current_chunk_dict = dict(current_chunk_list)

            # Имя файла чанка теперь включает имя page_type как префикс
            output_filename = f"{safe_page_type_name}_{chunk_number:04d}.json"
            output_filepath = os.path.join(target_page_type_dir, output_filename)
            
            try:
                with open(output_filepath, 'w', encoding='utf-8') as f_out:
                    json.dump(current_chunk_dict, f_out, indent=4, ensure_ascii=False)
                # print(f"    Чанк {chunk_number}/{num_chunks} ({len(current_chunk_dict)} элементов) сохранен в {output_filepath}")
                total_output_chunks_created +=1
            except Exception as e:
                print(f"    Ошибка при записи файла {output_filepath}: {e}")

    print(f"\nОбработка завершена. Всего обработано входных файлов: {processed_files_count}.")
    print(f"Всего создано/обновлено выходных чанков: {total_output_chunks_created}.")


# --- Пример использования ---
if __name__ == "__main__":
    base_test_dir = "test_json_processing_categorized_output" 
    input_dir_name = "J:\My Drive\hypo69\llm\data_by_supplier - Copy"
    output_dir_name = "J:\My Drive\hypo69\llm\data_by_supplie_page_type"

    current_input_base_dir = os.path.join(base_test_dir, input_dir_name)
    current_output_base_dir = os.path.join(base_test_dir, output_dir_name)

    if os.path.exists(base_test_dir): 
        shutil.rmtree(base_test_dir)
    
    os.makedirs(current_input_base_dir, exist_ok=True)
    # current_output_base_dir будет создана функцией

    print(f"Тестовые входные файлы будут созданы в: {os.path.abspath(current_input_base_dir)}")
    print(f"Тестовые выходные файлы будут созданы в: {os.path.abspath(current_output_base_dir)}")

    # --- Создаем тестовую структуру входных файлов ---
    # Файл в корне input_files
    data_root = {
        "https://site.com/product1": {"page_type": "product", "name": "Product 1", "ts": "t1"},
        "https://site.com/error1": {"page_type": "error", "code": 404, "ts": "t2"},
        "https://site.com/untyped1": {"info": "no type here", "ts": "t_ut1"}
    }
    with open(os.path.join(current_input_base_dir, "root_data.json"), "w", encoding="utf-8") as f: json.dump(data_root, f, indent=4)

    # Файлы в input_files/subdir_A/
    subdir_a = os.path.join(current_input_base_dir, "subdir_A")
    os.makedirs(subdir_a, exist_ok=True)
    
    data_sA_f1 = {
        "https://site.com/product2": {"page_type": "Product", "name": "Product 2 from SubdirA", "ts": "t3"}, # Product с большой буквы
        "https://site.com/category1": {"page_type": "category", "items": 10, "ts": "t4"}
    }
    with open(os.path.join(subdir_a, "sA_file1.json"), "w", encoding="utf-8") as f: json.dump(data_sA_f1, f, indent=4)
    
    # Файл для создания многих продуктов, чтобы протестировать чанкинг
    many_products = {}
    for i in range(120): # 120 продуктов -> 2 чанка по 50 + 1 чанк 20 (если chunk_size=50)
        many_products[f"https://site.com/product_bulk_{i}"] = {"page_type": "product", "id": f"bulk_p_{i}", "ts": f"ts_p_bulk_{i}"}
    with open(os.path.join(subdir_a, "sA_many_products.json"), "w", encoding="utf-8") as f: json.dump(many_products, f, indent=4)


    # Файлы в input_files/subdir_B/deeper/
    deeper_dir = os.path.join(current_input_base_dir, "subdir_B", "deeper")
    os.makedirs(deeper_dir, exist_ok=True)
    data_deep_f1 = {
        "https://site.com/error2": {"page_type": "Error", "code": 500, "ts": "t5"}, # Error с большой буквы
        "https://site.com/product3": {"page_type": "product", "name": "Product 3 from Deeper", "ts": "t6"},
        "https://site.com/untyped2_deep": {"info": "another no type", "ts": "t_ut2"}
    }
    with open(os.path.join(deeper_dir, "deep_file1.json"), "w", encoding="utf-8") as f: json.dump(data_deep_f1, f, indent=4)

    print("\n--- Запуск sort_by_page_type ---")
    # Установим chunk_size для теста, например, 50
    sort_by_page_type(current_input_base_dir, current_output_base_dir, chunk_size=50)

    # --- Проверка результатов ---
    print(f"\n--- Структура и содержимое выходных директорий и файлов в '{os.path.abspath(current_output_base_dir)}': ---")
    
    # Список ожидаемых категорий (в нижнем регистре, как они будут в именах директорий)
    expected_categories = ["product", "error", "category"] 
    
    for category_name in sorted(os.listdir(current_output_base_dir)):
        category_path = os.path.join(current_output_base_dir, category_name)
        if os.path.isdir(category_path):
            print(f"\nКатегория (директория): {category_name}")
            category_files = sorted(glob.glob(os.path.join(category_path, '*.json')))
            if not category_files:
                print("  Нет файлов в этой категории.")
                continue
            total_keys_in_category = 0
            for chunk_file_path in category_files:
                file_basename = os.path.basename(chunk_file_path)
                try:
                    with open(chunk_file_path, 'r', encoding='utf-8') as f: content_dict = json.load(f)
                    num_keys = len(content_dict)
                    total_keys_in_category += num_keys
                    print(f"  Файл-чанк: {file_basename} (ключей: {num_keys})")
                except Exception as e: 
                    print(f"  Ошибка чтения/обработки файла {file_basename}: {e}")
            print(f"  ИТОГО ключей в категории '{category_name}': {total_keys_in_category}")
        else:
            print(f"  Найден файл, а не директория в корне output: {category_name}")


    print(f"\n--- Содержимое исходных файлов в '{os.path.abspath(current_input_base_dir)}' после обработки: ---")
    input_files_after = sorted(glob.glob(os.path.join(current_input_base_dir, '**', '*.json'), recursive=True))
    for in_file_path in input_files_after:
        relative_in_path = os.path.relpath(in_file_path, current_input_base_dir)
        print(f"\nФайл: {relative_in_path}")
        try:
            with open(in_file_path, 'r', encoding='utf-8') as f: content_str = f.read().strip()
            if not content_str or content_str == '{}':
                print("  {} (пустой или все элементы с page_type обработаны)")
            else:
                remaining_data = json.loads(content_str)
                print(f"  Осталось ключей: {len(remaining_data)}")
                if len(remaining_data) > 0:
                    print(f"  Пример оставшихся ключей: {list(remaining_data.keys())[:3]}") 
        except Exception as e: print(f"  Ошибка чтения/обработки файла: {e}")

    print(f"\nПроверьте содержимое директорий '{os.path.abspath(current_input_base_dir)}' и '{os.path.abspath(current_output_base_dir)}'.")
