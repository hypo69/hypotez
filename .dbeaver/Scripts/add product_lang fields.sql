ALTER TABLE u782528968_L6mH.we4x_product_lang ADD delivery_additional_message varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL NULL COMMENT 'Дополнительное сообщение к условиям отправки';
ALTER TABLE u782528968_L6mH.we4x_product_lang ADD affiliate_short_link varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL NULL;
ALTER TABLE u782528968_L6mH.we4x_product_lang ADD affiliate_text mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL NULL;
ALTER TABLE u782528968_L6mH.we4x_product_lang ADD affiliate_summary mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL NULL;
ALTER TABLE u782528968_L6mH.we4x_product_lang ADD affiliate_summary_2 mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL NULL;
ALTER TABLE u782528968_L6mH.we4x_product_lang ADD affiliate_image_small varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL NULL;
ALTER TABLE u782528968_L6mH.we4x_product_lang ADD affiliate_image_medium varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL NULL;
ALTER TABLE u782528968_L6mH.we4x_product_lang ADD affiliate_image_large varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL NULL;
ALTER TABLE u782528968_L6mH.we4x_product_lang ADD specification tinytext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL NULL;
ALTER TABLE u782528968_L6mH.we4x_product_lang ADD how_to_use tinytext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL NULL COMMENT 'нструкция по использованию товара';
ALTER TABLE u782528968_L6mH.we4x_product_lang ADD ingredients tinytext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL NULL;
ALTER TABLE u782528968_L6mH.we4x_product ADD volume varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL NULL;

ALTER TABLE u782528968_L6mH.we4x_product ADD product_as_service tinyint(1) DEFAULT NULL NULL;
ALTER TABLE u782528968_L6mH.we4x_product ADD link_to_video varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL NULL;