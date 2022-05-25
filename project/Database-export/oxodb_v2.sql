-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: oxodb_v2
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `actie`
--

DROP TABLE IF EXISTS `actie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actie` (
  `actieid` int NOT NULL AUTO_INCREMENT,
  `actiebeschrijving` varchar(145) DEFAULT NULL,
  PRIMARY KEY (`actieid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actie`
--

LOCK TABLES `actie` WRITE;
/*!40000 ALTER TABLE `actie` DISABLE KEYS */;
INSERT INTO `actie` VALUES (1,'joystick waarden bewaren'),(2,'rfid waarden bewaren'),(3,'drukknop waarde bewaren'),(4,'touch sensor waarde bewaren'),(5,'aanschakelen actuator');
/*!40000 ALTER TABLE `actie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device`
--

DROP TABLE IF EXISTS `device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device` (
  `deviceid` int NOT NULL AUTO_INCREMENT,
  `devicenaam` varchar(45) NOT NULL,
  `beschrijving` varchar(145) DEFAULT 'null',
  `type` varchar(45) NOT NULL,
  `meeteenheid` varchar(45) DEFAULT 'null',
  PRIMARY KEY (`deviceid`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device`
--

LOCK TABLES `device` WRITE;
/*!40000 ALTER TABLE `device` DISABLE KEYS */;
INSERT INTO `device` VALUES (1,'drukpi','drukknop om raspberry Pi aan/uit te zetten','sensor','null'),(2,'drukdown1','drukknop voor speler 1 om naar beneden te gaan','sensor','null'),(3,'drukup1','drukknop voor speler 2 om naar boven te gaan','sensor','null'),(4,'drukdown2','drukknop voor speler 2 om naar beneden te gaan','sensor','null'),(5,'drukup2','drukknop voor speler 2 om naar boven te gaan','sensor','null'),(6,'rgb','rgb led om te tonen wie aan de beurt is','actuator','null'),(7,'touch1','touch sensor voor speler 1','sensor','null'),(8,'touch2','touch sensor voor speler 2','sensor','null'),(9,'oled','oled scherm om het IP-adres te tonen, wie aan de beurt is en of het scannen gelukt is','actuator','null'),(10,'rfid','scant de studentenkaarten','sensor','null'),(11,'neo','neopixels die de keuzes van de spelers tonen','actuator','null'),(12,'servo1','servo motor voor speler 1 die de score toont','actuator','°'),(13,'servo2','servo motor voor speler 2 die de score toont','actuator','°'),(14,'joy1','joystick voor speler 1 die de positie registreert','sensor','step'),(15,'joy2','joystick voor speler 2 die de positie registreert','sensor','step');
/*!40000 ALTER TABLE `device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historiek`
--

DROP TABLE IF EXISTS `historiek`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historiek` (
  `volgnummer` int NOT NULL AUTO_INCREMENT,
  `deviceid` int DEFAULT NULL,
  `actieid` int DEFAULT NULL,
  `waarde` float DEFAULT NULL,
  `commentaar` varchar(145) DEFAULT 'null',
  `actiedatum` datetime DEFAULT NULL,
  PRIMARY KEY (`volgnummer`),
  UNIQUE KEY `volgnummer` (`volgnummer`) /*!80000 INVISIBLE */,
  KEY `actieid_idx` (`actieid`),
  KEY `deviceid_idx` (`deviceid`),
  CONSTRAINT `actieid` FOREIGN KEY (`actieid`) REFERENCES `actie` (`actieid`),
  CONSTRAINT `deviceid` FOREIGN KEY (`deviceid`) REFERENCES `device` (`deviceid`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historiek`
--

LOCK TABLES `historiek` WRITE;
/*!40000 ALTER TABLE `historiek` DISABLE KEYS */;
INSERT INTO `historiek` VALUES (1,1,3,1,'aan','2022-05-23 10:00:00'),(2,1,3,0,'uit','2022-05-24 10:00:00'),(3,2,3,1,'aan','2022-05-25 10:00:00'),(4,2,3,0,'uit','2022-05-26 10:00:00'),(5,3,3,1,'aan','2022-05-27 10:00:00'),(6,3,3,0,'uit','2022-05-28 10:00:00'),(7,4,3,1,'aan','2022-05-29 10:00:00'),(8,4,3,0,'uit','2022-05-30 10:00:00'),(9,5,3,1,'aan','2022-05-31 10:00:00'),(10,5,3,0,'uit','2022-06-01 10:00:00'),(11,6,5,1,'null','2022-06-02 10:00:00'),(12,7,4,1,'aanraking gedetecteerd','2022-06-03 10:00:00'),(13,8,4,1,'aanraking gedetecteerd','2022-06-04 10:00:00'),(14,9,5,1,'null','2022-06-05 10:00:00'),(15,10,2,1,'kaart gescand','2022-06-06 10:00:00'),(16,11,5,2,'null','2022-06-07 10:00:00'),(17,12,5,120,'null','2022-06-08 10:00:00'),(18,13,5,90,'null','2022-06-09 10:00:00'),(19,14,1,1024,'joystick registreerde beweging','2022-06-10 10:00:00'),(20,14,1,1024,'joystick registreerde beweging','2022-06-11 10:00:00'),(21,15,1,1024,'joystick registreerde beweging','2022-06-12 10:00:00'),(22,15,1,1024,'joystick registreerde beweging','2022-06-13 10:00:00'),(23,1,3,1,'aan','2022-06-14 10:00:00'),(24,1,3,0,'uit','2022-06-15 10:00:00'),(25,2,3,1,'aan','2022-06-16 10:00:00'),(26,2,3,0,'uit','2022-06-17 10:00:00'),(27,3,3,1,'aan','2022-06-18 10:00:00'),(28,3,3,0,'uit','2022-06-19 10:00:00'),(29,4,3,1,'aan','2022-06-20 10:00:00'),(30,4,3,0,'uit','2022-06-21 10:00:00'),(31,5,3,1,'aan','2022-06-22 10:00:00'),(32,5,3,0,'uit','2022-06-23 10:00:00'),(33,6,5,1,'null','2022-06-24 10:00:00'),(34,7,4,1,'aanraking gedetecteerd','2022-06-25 10:00:00'),(35,8,4,1,'aanraking gedetecteerd','2022-06-26 10:00:00'),(36,9,5,1,'null','2022-06-27 10:00:00'),(37,10,2,1,'kaart gescand','2022-06-28 10:00:00'),(38,11,5,2,'null','2022-06-29 10:00:00'),(39,12,5,120,'null','2022-06-30 10:00:00'),(40,13,5,90,'null','2022-07-01 10:00:00'),(41,14,1,1024,'joystick registreerde beweging','2022-07-02 10:00:00'),(42,14,1,1024,'joystick registreerde beweging','2022-07-03 10:00:00'),(43,15,1,1024,'joystick registreerde beweging','2022-07-04 10:00:00'),(44,15,1,1024,'joystick registreerde beweging','2022-07-05 10:00:00'),(45,1,3,1,'aan','2022-07-06 10:00:00'),(46,1,3,0,'uit','2022-07-07 10:00:00'),(47,2,3,1,'aan','2022-07-08 10:00:00'),(48,2,3,0,'uit','2022-07-09 10:00:00'),(49,3,3,1,'aan','2022-07-10 10:00:00'),(50,3,3,0,'uit','2022-07-11 10:00:00');
/*!40000 ALTER TABLE `historiek` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `player`
--

DROP TABLE IF EXISTS `player`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player` (
  `playerid` int NOT NULL AUTO_INCREMENT,
  `naam` varchar(145) DEFAULT NULL,
  `voornaam` varchar(145) DEFAULT NULL,
  `gespeeld` int DEFAULT NULL,
  `verloren` int DEFAULT NULL,
  `gewonnen` int DEFAULT NULL,
  PRIMARY KEY (`playerid`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `player`
--

LOCK TABLES `player` WRITE;
/*!40000 ALTER TABLE `player` DISABLE KEYS */;
INSERT INTO `player` VALUES (1,'Van Goud','Amber',4,2,2),(2,'Van Gent','Bo',4,2,2),(3,'De Keyser','Eliah',4,2,2),(4,'Dal','Elizabet',2,2,0),(5,'Boogaard','Tom',3,2,1),(6,'Van Impe','Margeaux',3,2,1),(7,'Van den Bosche','Tim',5,2,3),(8,'Corte','Alisa',3,1,2),(9,'Maegerman','Sander',3,1,2),(10,'Vinnik','Aléssia',4,4,0);
/*!40000 ALTER TABLE `player` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spel`
--

DROP TABLE IF EXISTS `spel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `spel` (
  `spelid` int NOT NULL AUTO_INCREMENT,
  `winnerid` int DEFAULT NULL,
  `verliezerid` int DEFAULT NULL,
  `datum` date DEFAULT NULL,
  PRIMARY KEY (`spelid`),
  KEY `fk_spel_player1_idx` (`winnerid`),
  KEY `fk_spel_player2_idx` (`verliezerid`),
  CONSTRAINT `fk_spel_player1` FOREIGN KEY (`winnerid`) REFERENCES `player` (`playerid`),
  CONSTRAINT `fk_spel_player2` FOREIGN KEY (`verliezerid`) REFERENCES `player` (`playerid`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spel`
--

LOCK TABLES `spel` WRITE;
/*!40000 ALTER TABLE `spel` DISABLE KEYS */;
INSERT INTO `spel` VALUES (1,1,9,'2022-05-23'),(2,2,7,'2022-05-24'),(3,3,1,'2022-05-25'),(4,4,2,'2022-05-26'),(5,5,3,'2022-05-27'),(6,6,8,'2022-05-28'),(7,7,8,'2022-05-29'),(8,8,3,'2022-05-30'),(9,9,5,'2022-05-31'),(10,10,8,'2022-06-01'),(11,1,6,'2022-06-02'),(12,2,5,'2022-06-03'),(13,3,4,'2022-06-04'),(14,4,2,'2022-06-05'),(15,5,3,'2022-06-06'),(16,10,2,'2022-06-07'),(17,7,1,'2022-06-08');
/*!40000 ALTER TABLE `spel` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-05-25 10:02:13
