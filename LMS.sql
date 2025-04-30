-- MySQL dump 10.13  Distrib 8.0.41, for Linux (x86_64)
--
-- Host: localhost    Database: LMS
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `Book`
--

DROP DATABASE IF EXISTS LMS;
CREATE DATABASE LMS; -- Library Managemente System

USE LMS;

DROP TABLE IF EXISTS `Book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Book` (
  `book_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `book_publisher` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`book_id`),
  KEY `book_publisher` (`book_publisher`),
  CONSTRAINT `Book_ibfk_1` FOREIGN KEY (`book_publisher`) REFERENCES `Publisher` (`publisher_name`)
) ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Book`
--

LOCK TABLES `Book` WRITE;
/*!40000 ALTER TABLE `Book` DISABLE KEYS */;
INSERT INTO `Book` VALUES (1,'To Kill a Mockingbird','HarperCollins'),(2,'1984','Penguin Books'),(3,'Pride and Prejudice','Penguin Classics'),(4,'The Great Gatsby','Scribner'),(5,'One Hundred Years of Solitude','Harper & Row'),(6,'Animal Farm','Penguin Books'),(7,'The Catcher in the Rye','Little, Brown and Company'),(8,'Lord of the Flies','Faber and Faber'),(9,'Brave New World','Chatto & Windus'),(10,'The Picture of Dorian Gray','Ward, Lock and Co.'),(11,'The Alchemist','HarperCollins'),(12,'The God of Small Things','Random House India'),(13,'Wuthering Heights','Thomas Cautley Newby'),(14,'The Hobbit','Allen & Unwin'),(15,'The Lord of the Rings','Allen & Unwin'),(16,'The Hitchhiker\'s Guide to the Galaxy','Pan Books'),(17,'The Diary of a Young Girl','Bantam Books'),(18,'The Da Vinci Code','Doubleday'),(19,'The Adventures of Huckleberry Finn','Penguin Classics'),(20,'The Adventures of Tom Sawyer','American Publishing Company'),(21,'A Tale of Two Cities','Chapman and Hall'),(999,'Harry Potter and the Sorcerer\'s Stone','Oxford Publishing');
/*!40000 ALTER TABLE `Book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Book_Authors`
--

DROP TABLE IF EXISTS `Book_Authors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Book_Authors` (
  `book_id` int NOT NULL,
  `author_name` varchar(100) NOT NULL,
  PRIMARY KEY (`book_id`,`author_name`),
  CONSTRAINT `Book_Authors_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `Book` (`book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Book_Authors`
--

LOCK TABLES `Book_Authors` WRITE;
/*!40000 ALTER TABLE `Book_Authors` DISABLE KEYS */;
INSERT INTO `Book_Authors` VALUES (1,'Harper Lee'),(2,'George Orwell'),(3,'Jane Austen'),(4,'F. Scott Fitzgerald'),(5,'Gabriel Garcia Marquez'),(6,'George Orwell'),(7,'J.D. Salinger'),(8,'William Golding'),(9,'Aldous Huxley'),(10,'Oscar Wilde'),(11,'Paulo Coelho'),(12,'Arundhati Roy'),(13,'Emily Bronte'),(14,'J.R.R. Tolkien'),(15,'J.R.R. Tolkien'),(16,'Douglas Adams'),(17,'Anne Frank'),(18,'Dan Brown'),(19,'Mark Twain'),(20,'Mark Twain'),(21,'Charles Dickens'),(999,'J.K. Rowling');
/*!40000 ALTER TABLE `Book_Authors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Book_Copies`
--

DROP TABLE IF EXISTS `Book_Copies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Book_Copies` (
  `book_id` int NOT NULL,
  `branch_id` int NOT NULL,
  `no_of_copies` int DEFAULT NULL,
  PRIMARY KEY (`book_id`,`branch_id`),
  KEY `branch_id` (`branch_id`),
  CONSTRAINT `Book_Copies_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `Book` (`book_id`),
  CONSTRAINT `Book_Copies_ibfk_2` FOREIGN KEY (`branch_id`) REFERENCES `Library_Branch` (`branch_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Book_Copies`
--

LOCK TABLES `Book_Copies` WRITE;
/*!40000 ALTER TABLE `Book_Copies` DISABLE KEYS */;
INSERT INTO `Book_Copies` VALUES (1,1,3),(2,1,2),(3,2,1),(4,3,5),(5,1,5),(6,2,3),(7,2,2),(8,3,2),(9,1,4),(10,2,2),(11,1,3),(12,3,3),(13,3,2),(14,1,5),(15,3,2),(16,2,3),(17,3,3),(18,3,3),(19,1,5),(20,3,2),(21,3,2);
/*!40000 ALTER TABLE `Book_Copies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Book_Loans`
--

DROP TABLE IF EXISTS `Book_Loans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Book_Loans` (
  `book_id` int NOT NULL,
  `branch_id` int NOT NULL,
  `card_no` int NOT NULL,
  `date_out` date NOT NULL,
  `due_date` date DEFAULT NULL,
  `returned_date` date DEFAULT NULL,
  `Late` int DEFAULT NULL,
  PRIMARY KEY (`book_id`,`branch_id`,`card_no`,`date_out`),
  KEY `branch_id` (`branch_id`),
  KEY `card_no` (`card_no`),
  CONSTRAINT `Book_Loans_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `Book` (`book_id`),
  CONSTRAINT `Book_Loans_ibfk_2` FOREIGN KEY (`branch_id`) REFERENCES `Library_Branch` (`branch_id`),
  CONSTRAINT `Book_Loans_ibfk_3` FOREIGN KEY (`card_no`) REFERENCES `Borrower` (`card_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Book_Loans`
--

LOCK TABLES `Book_Loans` WRITE;
/*!40000 ALTER TABLE `Book_Loans` DISABLE KEYS */;
INSERT INTO `Book_Loans` VALUES (1,1,123456,'2022-01-01','2022-02-01','2022-02-01',0),(2,1,789012,'2022-01-02','2022-02-02',NULL,1),(3,2,345678,'2022-01-03','2022-02-03',NULL,1),(4,3,901234,'2022-01-04','2022-02-04','2022-02-04',0),(5,1,567890,'2022-01-05','2022-02-05','2022-02-09',1),(6,2,234567,'2022-01-06','2022-02-06','2022-02-10',1),(7,2,890123,'2022-01-07','2022-02-07','2022-03-08',1),(8,3,456789,'2022-01-08','2022-02-08','2022-03-10',1),(9,1,111111,'2022-01-09','2022-02-09','2022-02-06',0),(10,2,222222,'2022-01-10','2022-02-10','2022-02-07',0),(11,1,333333,'2022-03-01','2022-03-08','2022-03-08',0),(12,3,444444,'2022-03-03','2022-03-10','2022-03-10',0),(13,3,555555,'2022-02-03','2022-03-03','2022-02-18',0),(14,1,565656,'2022-01-14','2022-02-14','2022-03-31',1),(15,3,676767,'2022-01-15','2022-02-15','2022-02-21',1),(16,2,787878,'2022-03-05','2022-03-12','2022-03-24',1),(17,3,989898,'2022-03-23','2022-03-30','2022-03-30',0),(18,3,121212,'2022-01-18','2022-02-18','2022-02-18',0),(19,1,232323,'2022-03-24','2022-03-31','2022-03-31',0),(20,3,343434,'2022-01-21','2022-02-21','2022-02-21',0),(21,3,454545,'2022-01-24','2022-02-24','2022-02-24',0);
/*!40000 ALTER TABLE `Book_Loans` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Borrower`
--

DROP TABLE IF EXISTS `Borrower`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Borrower` (
  `card_no` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`card_no`)
) ENGINE=InnoDB AUTO_INCREMENT=989900 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Borrower`
--

LOCK TABLES `Borrower` WRITE;
/*!40000 ALTER TABLE `Borrower` DISABLE KEYS */;
INSERT INTO `Borrower` VALUES (111111,'Alex Kim','983 Sine St, Arizona, AR 70451','678-784-5563'),(121212,'Chloe Park','345 Shark St, Arizona, AR 72213','755-905-5572'),(123456,'John Smith','456 Oak St, Arizona, AR 70010','205-555-5555'),(222222,'Rachel Lee','999 Apple Ave, Arizona, AR 70671','231-875-5564'),(232323,'William Chen','890 Sting St, New York, NY 10459','406-755-5580'),(234567,'Emily Lee','389 Oaklay St, Arizona, AR 70986','231-678-5560'),(333333,'William Johnson','705 Paster St, New Jersey 32002','235-525-5567'),(343434,'Olivia Johnson','345 Pine St, New Jersey, NJ 32095','662-554-5575'),(345678,'Bob Johnson','12 Elm St, Arizona, AR 70345 ','545-234-5557'),(444444,'Ethan Martinez','466 Deeplm St, New York, NY 10321','555-555-5569'),(454545,'Dylan Kim','567 Cowboy way St, New Jersey, NJ 32984','435-254-5578'),(456789,'Laura Chen','345 Mapman Ave, Arizona, AR 70776','565-985-9962'),(555555,'Grace Hernandez','315 Babes St, Arizona, AR 70862 ','455-567-5587'),(565656,'Sophia Park','678 Dolphin St, New York, NY 10062','675-455-5568'),(567890,'Tom Lee','678  S Oak St, New York, NY 10045','209-525-5559'),(676767,'Olivia Lee','345 Spine St, New York, NY 10092','435-878-5569'),(787878,'Noah Thompson','189 GreenOak Ave, New Jersey, NJ 32453','245-555-5571'),(789012,'Jane Doe','789 Maple Ave, New Jersey, NJ 32542','555-235-5556'),(890123,'Michael Park','123 Pinewood St, New Jersey, NJ 32954','655-890-2161'),(901234,'Sarah Kim','345 Pine St, New York, NY 10065','515-325-2158'),(989898,'Olivia Smith','178 Elm St, New Jersey, NJ 32124','325-500-5579'),(989899,'Alice Cooper','999 Unity St, Plano, TX','(837) 721-8965');
/*!40000 ALTER TABLE `Borrower` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Library_Branch`
--

DROP TABLE IF EXISTS `Library_Branch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Library_Branch` (
  `branch_id` int NOT NULL,
  `branch_name` varchar(100) DEFAULT NULL,
  `branch_address` varchar(255) DEFAULT NULL,
  `LateFee` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`branch_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Library_Branch`
--

LOCK TABLES `Library_Branch` WRITE;
/*!40000 ALTER TABLE `Library_Branch` DISABLE KEYS */;
INSERT INTO `Library_Branch` VALUES (1,'Main Branch','123 Main St, New York, NY 10003',1.20),(2,'West Branch','456 West St, Arizona, AR 70622',0.75),(3,'East Branch','789 East St, New Jersy, NY 32032',2.30),(4,'North Branch','456 NW, Irving, TX 76100',0.50),(5,'UTA Branch','123 Cooper St, Arlington TX 76101',0.50);
/*!40000 ALTER TABLE `Library_Branch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Publisher`
--

DROP TABLE IF EXISTS `Publisher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Publisher` (
  `publisher_name` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`publisher_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Publisher`
--

LOCK TABLES `Publisher` WRITE;
/*!40000 ALTER TABLE `Publisher` DISABLE KEYS */;
INSERT INTO `Publisher` VALUES ('Allen & Unwin','212-782-9001','22 New Wharf Rd, Arizona, AR 70654'),('American Publishing Company','682-243-3524','7652 Northgate way lane, Georgia, GA 30054'),('Bantam Books','313-243-5354','1745 Broadway, New York, NY 10019'),('Chapman and Hall','833-342-2343','789 Oak St, Texas, TX 76010'),('Chatto & Windus','442-727-3800','Bloomsbury House, 7477 Great Russell St, Arizona, AR 72965'),('Doubleday','212-782-9000','789 Division St, Minnesota, MN 55344'),('Faber and Faber','201-797-3800','463 south centre street, Arizona, AR 71653'),('Harper & Row','212-207-7000','1195 Border street, Montana, MT 59007'),('HarperCollins','212-207-7000','195 Broadway, New York, NY 10007'),('Little, Brown and Company','212-764-2000','111 Huddle St, New Jersey, NJ 32014'),('Oxford Publishing','(111) 222-3333','123 Oxford St, UK'),('Pan Books','313-243-5353','567 Pine Tree Rd, Colorado, CO 87348'),('Penguin Books','212-366-3000','475 Hudson St, New York, NY 10014'),('Penguin Classics','212-366-2000','123 Main St, California, CA 01383'),('Random House India','291-225-6634','423 baywatch centre street, Alabama, AL 30513'),('Scribner','212-207-7474','19 Broadway, New York, NY 10007'),('Thomas Cautley Newby','243-353-2352','890 Elmwood Dr, Floride, FL 98238'),('Ward, Lock and Co.','647-242-3434','456 Maple Ave, Texas, TX 76013 ');
/*!40000 ALTER TABLE `Publisher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `vBookLoanInfo`
--

DROP TABLE IF EXISTS `vBookLoanInfo`;
/*!50001 DROP VIEW IF EXISTS `vBookLoanInfo`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vBookLoanInfo` AS SELECT 
 1 AS `Card_No`,
 1 AS `Borrower Name`,
 1 AS `Date_Out`,
 1 AS `Due_Date`,
 1 AS `Returned_date`,
 1 AS `TotalDays`,
 1 AS `Book Title`,
 1 AS `Number of days returned late`,
 1 AS `Branch ID`,
 1 AS `LateFeeBalance`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `vBookLoanInfo`
--

/*!50001 DROP VIEW IF EXISTS `vBookLoanInfo`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vBookLoanInfo` AS select `BW`.`card_no` AS `Card_No`,`BW`.`name` AS `Borrower Name`,`B_L`.`date_out` AS `Date_Out`,`B_L`.`due_date` AS `Due_Date`,`B_L`.`returned_date` AS `Returned_date`,(to_days(`B_L`.`returned_date`) - to_days(`B_L`.`date_out`)) AS `TotalDays`,`Bk`.`title` AS `Book Title`,(case when (`B_L`.`returned_date` between `B_L`.`date_out` and `B_L`.`due_date`) then 0 else (to_days(`B_L`.`returned_date`) - to_days(`B_L`.`due_date`)) end) AS `Number of days returned late`,`L_B`.`branch_id` AS `Branch ID`,(case when (`B_L`.`returned_date` between `B_L`.`date_out` and `B_L`.`due_date`) then 0 else (`L_B`.`LateFee` * (to_days(`B_L`.`returned_date`) - to_days(`B_L`.`due_date`))) end) AS `LateFeeBalance` from (((`Borrower` `BW` join `Book_Loans` `B_L` on((`BW`.`card_no` = `B_L`.`card_no`))) join `Book` `Bk` on((`B_L`.`book_id` = `Bk`.`book_id`))) join `Library_Branch` `L_B` on((`B_L`.`branch_id` = `L_B`.`branch_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-29 21:19:31
