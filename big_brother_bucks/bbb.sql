# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Hôte: localhost (MySQL 5.6.28-log)
# Base de données: cryptocurrencies
# Temps de génération: 2016-12-06 10:45:46 +0000
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
  `a_balance` int(11) DEFAULT '0',
  `a_pubkey` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`a_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;

INSERT INTO `account` (`a_id`, `a_balance`, `a_pubkey`)
VALUES
	(5,10,NULL),
	(6,90,NULL);

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
	(1,5,6,100,1),
	(2,5,6,100,1),
	(3,5,6,100,1),
	(4,5,6,100,1),
	(5,6,5,200,1),
	(6,5,6,100,1),
	(7,5,6,90,1);

/*!40000 ALTER TABLE `transaction` ENABLE KEYS */;
UNLOCK TABLES;

DELIMITER ;;
/*!50003 SET SESSION SQL_MODE="NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`localhost` */ /*!50003 TRIGGER `update_balance` BEFORE INSERT ON `transaction` FOR EACH ROW BEGIN
	DECLARE balance INT;
	SELECT a_balance INTO balance FROM account WHERE a_id = NEW.t_from;
	IF ( balance >= NEW.t_amount ) THEN
		UPDATE 
			account a1 JOIN account a2 
			ON a1.a_id = NEW.t_from AND a2.a_id = NEW.t_to
			SET
				a1.a_balance = a1.a_balance - NEW.t_amount,
				a2.a_balance = a2.a_balance + NEW.t_amount;
	ELSE
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = "Unsufficient amount, transaction aborted";  
	END IF;
END */;;
DELIMITER ;
/*!50003 SET SESSION SQL_MODE=@OLD_SQL_MODE */;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
