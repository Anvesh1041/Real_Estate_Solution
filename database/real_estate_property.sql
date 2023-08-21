-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: real_estate
-- ------------------------------------------------------
-- Server version	8.0.34

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
-- Table structure for table `property`
--

DROP TABLE IF EXISTS `property`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `property` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Price` varchar(10) NOT NULL,
  `Location` varchar(20) NOT NULL,
  `BHK` int NOT NULL,
  `Address` varchar(45) NOT NULL,
  `Img_Path` text,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property`
--

LOCK TABLES `property` WRITE;
/*!40000 ALTER TABLE `property` DISABLE KEYS */;
INSERT INTO `property` VALUES (1,'60 Lakh','Wadala',1,'ram nagar','/static/img/properties/0_House.jpg'),(2,'3 Cr','Dadar',2,'ganesh nagar','\\static\\img\\properties\\1.jpg'),(3,'80 lakh','Kharghar',2,'Laxman Nagar','\\static\\img\\properties\\2.jpg'),(4,'70 lakh','Kalyan',1,'ram nagar','\\static\\img\\properties\\3.jpg'),(5,'2 Cr','Andheri',2,'sai nagar','\\static\\img\\properties\\4.jpg'),(6,'4 Cr','parel',3,'sai nagar','\\static\\img\\properties\\5.jpg'),(7,'80 lakh','wadala',1,'ganesh nagar','\\static\\img\\properties\\6.jpg'),(8,'2.5 Cr','wadala',2,'ganesh nagar','\\static\\img\\properties\\7.jpg'),(9,'2 Cr','wadala',2,'ganesh nagar','\\static\\img\\properties\\8.jpg'),(10,'1.5 Cr','wadala',2,'ram nagar','\\static\\img\\properties\\9.jpg'),(11,'2.5 Cr','wadala',3,'ram nagar','\\static\\img\\properties\\10.jpg'),(12,'3 Cr','wadala',3,'laxman nagar','\\static\\img\\properties\\11.jpg'),(13,'1.2 Cr','wadala',1,'laxman nagar','\\static\\img\\properties\\12.jpg'),(14,'2.3 Cr','wadala',2,'laxman nagar','\\static\\img\\properties\\13.jpg'),(15,'50 lakh','wadala',1,'abc nagar','\\static\\img\\properties\\14.jpg'),(16,'1.2 Cr','Dadar',1,'abc nagar','\\static\\img\\properties\\15.jpg');
/*!40000 ALTER TABLE `property` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-14  0:13:27
