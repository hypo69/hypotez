SELECT
    c.id_category,
    c.id_parent,
    cl.name,
    cl.description,
    cl.link_rewrite,
    cl.meta_title
FROM
    wxrq_category c
JOIN
    wxrq_category_lang cl ON c.id_category = cl.id_category
WHERE
    cl.id_shop = 1  
    AND cl.id_lang = 1 
;