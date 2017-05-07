CREATE TABLE `imac_spec_prc` (
  `seq` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `cwral_seq` int(11) unsigned NOT NULL,
  `model_type` char(1) NOT NULL,
  `cpu_default` varchar(40) NOT NULL,
  `cpu_max` varchar(40) NOT NULL,
  `hdd` varchar(30) NOT NULL,
  `graphic` varchar(40) NOT NULL,
  `prc_krw` char(8) NOT NULL,
  `prc_jpy` char(7) NOT NULL,
  `crrency_rate` char(5) NOT NULL,
  `converted_prc` char(10) NOT NULL,
  `insert_dt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`seq`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
