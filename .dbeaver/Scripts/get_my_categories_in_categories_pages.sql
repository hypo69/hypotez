SELECT
	cc.`id_cms_category`,
	cc.`id_parent`,
	cc.`active`,
	cc.`POSITION`,
	ccl.`name`,
	ccl.`description`
FROM
	wxrq_cms_category cc
LEFT JOIN wxrq_cms_category_lang ccl ON
	ccl.`id_cms_category` = cc.`id_cms_category`
INNER JOIN wxrq_cms_category_shop ccs ON
	ccs.`id_cms_category` = cc.`id_cms_category`
WHERE
	(ccl.`id_lang` = 1)
	AND (ccl.`id_shop` IN ('1'))
	AND (cc.`id_parent` = 2)

ORDER BY
	POSITION ASC
LIMIT 50

