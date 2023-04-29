-- --------------------------------------------------------
-- Host:                         localhost
-- Server version:               5.1.72-community - MySQL Community Server (GPL)
-- Server OS:                    Win32
-- HeidiSQL Version:             9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping structure for table interstellar cargo transportation.captain
CREATE TABLE IF NOT EXISTS `captain` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(50) DEFAULT NULL,
  `lastname` varchar(50) DEFAULT NULL,
  `rank` varchar(50) DEFAULT NULL,
  `homeplanet` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

-- Dumping data for table interstellar cargo transportation.captain: 4 rows
/*!40000 ALTER TABLE `captain` DISABLE KEYS */;
INSERT INTO captain (firstname, lastname, rank, homeplanet) VALUES
('James', 'Kirk', 'Captain', 'Earth'),
('Jean-Luc', 'Picard', 'Captain', 'Neptune'),
('Benjamin', 'Sisko', 'Admiral', 'Earth'),
('Kathryn', 'Janeway', 'Lieutennant', 'Venus'),
('Jonathan', 'Archer', 'Rear Admiral', '55 Cancri e');

/*!40000 ALTER TABLE `captain` ENABLE KEYS */;

-- Dumping structure for table interstellar cargo transportation.cargo
CREATE TABLE IF NOT EXISTS `cargo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `weight` float NOT NULL,
  `cargotype` varchar(255) NOT NULL,
  `departure` date DEFAULT NULL,
  `arrival` date DEFAULT NULL,
  `shipid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `shipid` (`shipid`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

-- Dumping data for table interstellar cargo transportation.cargo: 5 rows
/*!40000 ALTER TABLE `cargo` DISABLE KEYS */;
INSERT INTO cargo (weight, cargotype, departure, arrival, shipid)
VALUES
  (100.5, 'machinery', '2023-05-01', '2023-05-07', 1),
  (200.0, 'food', '2023-05-02', '2023-05-09', 1),
  (500.0, 'raw materials', '2023-05-03', '2023-05-10', 2),
  (300.0, 'vehicles', '2023-05-05', '2023-05-12', 3),
  (400.0, 'machinery', '2023-05-06', '2023-05-13', 2);

/*!40000 ALTER TABLE `cargo` ENABLE KEYS */;

-- Dumping structure for table interstellar cargo transportation.spaceship
CREATE TABLE IF NOT EXISTS `spaceship` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `maxweight` float NOT NULL,
  `captainid` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `captainid` (`captainid`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

-- Dumping data for table interstellar cargo transportation.spaceship: 3 rows
/*!40000 ALTER TABLE `spaceship` DISABLE KEYS */;
INSERT INTO `spaceship` (`maxweight`, `captainid`) VALUES
(150.0, 1),
(200.0, 2),
(100.0, 3),
(250.0, 4),
(180.0, 5);

/*!40000 ALTER TABLE `spaceship` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
