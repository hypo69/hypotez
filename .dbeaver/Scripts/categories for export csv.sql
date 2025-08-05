SELECT 
    c.id_category, 
    c.active, 
    l.name,
    c.id_parent
FROM 
    wxrq_category c
JOIN 
    wxrq_category_lang l ON c.id_category = l.id_category
WHERE 
    l.id_lang = 1;