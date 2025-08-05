TRUNCATE TABLE ps_connections;

TRUNCATE TABLE ps_connections_source;

TRUNCATE TABLE ps_connections_page;

TRUNCATE TABLE ps_pagenotfound;

TRUNCATE TABLE ps_statssearch;

TRUNCATE TABLE ps_mail;

DELETE FROM `PREFIX_specific_price` WHERE `to` != '0000-00-00 00:00:00' AND `to` < NOW();

DELETE FROM `PREFIX_specific_price_rule` WHERE `to` != '0000-00-00 00:00:00' AND `to` < NOW();

TRUNCATE TABLE ps_smarty_cache;

TRUNCATE TABLE ps_smarty_last_flush;

TRUNCATE TABLE ps_smarty_lazy_cache;