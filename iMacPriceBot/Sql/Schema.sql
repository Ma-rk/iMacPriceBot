 CREATE TABLE `imac_spec_prc` (
  `seq`           int(11) unsigned NOT NULL AUTO_INCREMENT,
  `model_type`    char(1) NOT NULL,
  `cpu_default`   varchar(40) NOT NULL,
  `cpu_max`       varchar(40) NOT NULL,
  `hdd`           varchar(30) NOT NULL,
  `graphic`       varchar(40) NOT NULL,
  `prc_krw`       char(8) NOT NULL,
  `prc_jpy`       char(7) NOT NULL,
  `crrency_rate`  char(5) NOT NULL,
  `converted_prc` char(10) NOT NULL,
  PRIMARY KEY (`seq`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
