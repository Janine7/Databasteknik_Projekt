-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: projekt
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `productslist`
--

DROP TABLE IF EXISTS `productslist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productslist` (
  `ProdID` int NOT NULL AUTO_INCREMENT,
  `ProdName` varchar(255) NOT NULL,
  `Price` varchar(255) NOT NULL,
  PRIMARY KEY (`ProdID`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productslist`
--

LOCK TABLES `productslist` WRITE;
/*!40000 ALTER TABLE `productslist` DISABLE KEYS */;
INSERT INTO `productslist` VALUES (1,'Cucumber','15'),(2,'Tomato','4'),(3,'Onion','2'),(4,'Salad','20'),(5,'Parsley','19'),(6,'Basil','22'),(7,'Lemon','10'),(8,'Apple','5'),(9,'Pear','9'),(10,'Banana','4'),(11,'Melon','28'),(12,'Grapes','35'),(13,'Bread','30'),(14,'Knäckebröd','22'),(15,'Skorpa','20'),(16,'Riskaka','15'),(17,'Cookie','20'),(18,'Ham','30'),(19,'Meatballs','23'),(20,'Sausage','36'),(21,'Minced meat','89'),(22,'Chicken','105'),(23,'Salmon','109'),(24,'Cod','70'),(25,'Liver paste','15'),(26,'Milk','12'),(27,'Yoghurt','25'),(28,'Butter','60'),(29,'Cheese','99'),(30,'Cream','29'),(31,'Cream Fraiche','16'),(32,'Beans','10'),(33,'Taco seasoning','10'),(34,'Tortilla','15'),(35,'Chips','29'),(36,'Candy','125'),(37,'Chocolate','22'),(38,'Ice cream','30'),(39,'Soda','19'),(40,'Juice','18');
/*!40000 ALTER TABLE `productslist` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-27 13:38:33
