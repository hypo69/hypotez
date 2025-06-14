-- u177424397_store.rsx9g_max_id source
SELECT MAX(max_id) AS global_max_id
FROM (
    SELECT MAX(id_category) AS max_id FROM rsx9g_category
    UNION ALL
    SELECT MAX(id_supplier) FROM rsx9g_supplier
    UNION ALL
    SELECT MAX(id_manufacturer) FROM rsx9g_manufacturer
    -- Добавьте другие таблицы по необходимости
) AS combined_ids;