-- MySQL dump 10.13  Distrib 8.0.34, for Linux (x86_64)
--
-- Host: localhost    Database: coffeeshopdb
-- ------------------------------------------------------
-- Server version	8.0.34-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `COFFEESHOP`
--

DROP TABLE IF EXISTS `COFFEESHOP`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `COFFEESHOP` (
  `ShopID` int NOT NULL,
  `ShopName` varchar(255) DEFAULT NULL,
  `Location` varchar(255) DEFAULT NULL,
  `Rating` float DEFAULT NULL,
  `ManagerID` int DEFAULT NULL,
  PRIMARY KEY (`ShopID`),
  KEY `fk_manager` (`ManagerID`),
  CONSTRAINT `fk_manager` FOREIGN KEY (`ManagerID`) REFERENCES `EMPLOYEE` (`EmployeeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `COFFEESHOP`
--

LOCK TABLES `COFFEESHOP` WRITE;
/*!40000 ALTER TABLE `COFFEESHOP` DISABLE KEYS */;
INSERT INTO `COFFEESHOP` VALUES (1001,'Starbucks','500 Spruce St',4.2,4001),(1002,'CopperMountain','429 Brooks St',4.6,4002),(1003,'LaPetite','44 Higgins',4.7,4003),(1004,'Clyde','4 S St E',4.7,4004),(1005,'Blackcoffee','32 Johnson St',4.5,4005),(1006,'Break Espresso','22 Higgins',4.6,4006),(1007,'LadderCoffeeCo','529 Western Ave',4.8,4007);
/*!40000 ALTER TABLE `COFFEESHOP` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CONTRACT`
--

DROP TABLE IF EXISTS `CONTRACT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CONTRACT` (
  `ContractID` int NOT NULL,
  `SupplierID` int DEFAULT NULL,
  `ShopID` int DEFAULT NULL,
  PRIMARY KEY (`ContractID`),
  KEY `fk_supplier` (`SupplierID`),
  KEY `fk_coffeeshop` (`ShopID`),
  CONSTRAINT `fk_coffeeshop` FOREIGN KEY (`ShopID`) REFERENCES `COFFEESHOP` (`ShopID`),
  CONSTRAINT `fk_supplier` FOREIGN KEY (`SupplierID`) REFERENCES `SUPPLIER` (`SupplierID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CONTRACT`
--

LOCK TABLES `CONTRACT` WRITE;
/*!40000 ALTER TABLE `CONTRACT` DISABLE KEYS */;
INSERT INTO `CONTRACT` VALUES (2001,5001,1001),(2002,5002,1002),(2003,5003,1003),(2004,5004,1004),(2005,5005,1005),(2006,5006,1006),(2007,5007,1007);
/*!40000 ALTER TABLE `CONTRACT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EMPLOYEE`
--

DROP TABLE IF EXISTS `EMPLOYEE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `EMPLOYEE` (
  `EmployeeID` int NOT NULL,
  `EmployeeName` varchar(255) DEFAULT NULL,
  `ShopID` int DEFAULT NULL,
  `ManagerID` int DEFAULT NULL,
  PRIMARY KEY (`EmployeeID`),
  KEY `fk_employeemanager` (`ManagerID`),
  CONSTRAINT `fk_employeemanager` FOREIGN KEY (`ManagerID`) REFERENCES `EMPLOYEE` (`EmployeeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EMPLOYEE`
--

LOCK TABLES `EMPLOYEE` WRITE;
/*!40000 ALTER TABLE `EMPLOYEE` DISABLE KEYS */;
INSERT INTO `EMPLOYEE` VALUES (4001,'Chris Brown',1001,4001),(4002,'John Frank',1002,4002),(4003,'Fred Red',1003,4003),(4004,'Bo Green',1004,4004),(4005,'Mark Smart',1005,4005),(4006,'Reed Free',1006,4006),(4007,'Joe Bro',1007,4007);
/*!40000 ALTER TABLE `EMPLOYEE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ITEM_CATEGORY`
--

DROP TABLE IF EXISTS `ITEM_CATEGORY`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ITEM_CATEGORY` (
  `ItemCategory` varchar(255) NOT NULL,
  PRIMARY KEY (`ItemCategory`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ITEM_CATEGORY`
--

LOCK TABLES `ITEM_CATEGORY` WRITE;
/*!40000 ALTER TABLE `ITEM_CATEGORY` DISABLE KEYS */;
INSERT INTO `ITEM_CATEGORY` VALUES ('Add-on'),('Bakery'),('Cold Drink'),('Hot Drink'),('Pastry'),('Sandwich'),('Special');
/*!40000 ALTER TABLE `ITEM_CATEGORY` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MENU_ITEM`
--

DROP TABLE IF EXISTS `MENU_ITEM`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MENU_ITEM` (
  `ItemID` int NOT NULL,
  `ItemPrice` decimal(10,2) DEFAULT NULL,
  `ItemCategory` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ItemID`),
  KEY `fk_item_category` (`ItemCategory`),
  CONSTRAINT `fk_item_category` FOREIGN KEY (`ItemCategory`) REFERENCES `ITEM_CATEGORY` (`ItemCategory`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MENU_ITEM`
--

LOCK TABLES `MENU_ITEM` WRITE;
/*!40000 ALTER TABLE `MENU_ITEM` DISABLE KEYS */;
INSERT INTO `MENU_ITEM` VALUES (3001,2.99,'Pastry'),(3002,5.00,'Bakery'),(3003,5.00,'Hot Drink'),(3004,4.00,'Cold Drink'),(3005,7.00,'Sandwich'),(3006,2.00,'Add-on'),(3007,9.99,'Special');
/*!40000 ALTER TABLE `MENU_ITEM` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SUPPLIER`
--

DROP TABLE IF EXISTS `SUPPLIER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SUPPLIER` (
  `SupplierID` int NOT NULL,
  `SupplierName` varchar(255) DEFAULT NULL,
  `SupplierLocation` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`SupplierID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SUPPLIER`
--

LOCK TABLES `SUPPLIER` WRITE;
/*!40000 ALTER TABLE `SUPPLIER` DISABLE KEYS */;
INSERT INTO `SUPPLIER` VALUES (5001,'PlatanoGreens','Brazil'),(5002,'LadderBeans','USA'),(5003,'BlackerRange','Ethiopia'),(5004,'EthoJoe','Argentina'),(5005,'RockWater','Peru'),(5006,'ShadyPlains','Brazil'),(5007,'HorizenHarvest','El Salvador');
/*!40000 ALTER TABLE `SUPPLIER` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-10-24  1:49:55
