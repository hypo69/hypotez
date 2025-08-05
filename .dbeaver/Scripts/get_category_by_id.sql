

select wcl.id_category, wcl.name  from wxrq_category wc
inner join wxrq_category_lang wcl on wc.id_category = wcl.id_category 
where wc.id_category = 11280 and id_lang = 1