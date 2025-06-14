CREATE TABLE u177424397_all_categories.amazon (
	id INT auto_increment NOT NULL,
	category_id int(11) NOT NULL,
	category_name varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL NULL,
	parent_category_id int(11) DEFAULT NULL NULL,
	hypotez_category_id int(11) DEFAULT NULL NULL,
	url varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL NULL,
	CONSTRAINT amazon_pk PRIMARY KEY (id),
	CONSTRAINT amazon_unique UNIQUE KEY (category_id)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;
