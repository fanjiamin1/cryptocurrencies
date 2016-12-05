# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Hôte: localhost (MySQL 5.6.28-log)
# Base de données: cryptocurrencies
# Temps de génération: 2016-12-05 13:49:02 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Affichage de la table account
# ------------------------------------------------------------

DROP TABLE IF EXISTS `account`;

CREATE TABLE `account` (
  `a_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `a_desc` int(11) DEFAULT NULL,
  PRIMARY KEY (`a_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;

INSERT INTO `account` (`a_id`, `a_desc`)
VALUES
	(1,NULL),
	(3,25);

/*!40000 ALTER TABLE `account` ENABLE KEYS */;
UNLOCK TABLES;


# Affichage de la table transaction
# ------------------------------------------------------------

DROP TABLE IF EXISTS `transaction`;

CREATE TABLE `transaction` (
  `t_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `t_from` int(11) unsigned DEFAULT '0',
  `t_to` int(11) unsigned DEFAULT '0',
  `t_amount` int(11) DEFAULT NULL,
  `t_session` int(11) DEFAULT NULL,
  PRIMARY KEY (`t_id`),
  KEY `t_a_from` (`t_from`),
  KEY `t_a_to` (`t_to`),
  CONSTRAINT `t_a_from` FOREIGN KEY (`t_from`) REFERENCES `account` (`a_id`),
  CONSTRAINT `t_a_to` FOREIGN KEY (`t_to`) REFERENCES `account` (`a_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `transaction` WRITE;
/*!40000 ALTER TABLE `transaction` DISABLE KEYS */;

INSERT INTO `transaction` (`t_id`, `t_from`, `t_to`, `t_amount`, `t_session`)
VALUES
	(18,1,1,20,10),
	(19,3,3,50,10),
	(20,3,3,50,10);

/*!40000 ALTER TABLE `transaction` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
