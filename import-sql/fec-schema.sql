-- MySQL dump 10.13  Distrib 5.6.33, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: fec
-- ------------------------------------------------------
-- Server version	5.6.33-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `committee`
--

DROP TABLE IF EXISTS `committee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `committee` (
  `CMTE_ID` varchar(9) DEFAULT NULL,
  `CMTE_NM` varchar(200) DEFAULT NULL,
  `TRES_NM` varchar(90) DEFAULT NULL,
  `CMTE_ST1` varchar(34) DEFAULT NULL,
  `CMTE_ST2` varchar(34) DEFAULT NULL,
  `CMTE_CITY` varchar(30) DEFAULT NULL,
  `CMTE_ST` varchar(2) DEFAULT NULL,
  `CMTE_ZIP` varchar(9) DEFAULT NULL,
  `CMTE_DSGN` varchar(1) DEFAULT NULL,
  `CMTE_TP` varchar(1) DEFAULT NULL,
  `CMTE_PTY_AFFILIATION` varchar(3) DEFAULT NULL,
  `CMTE_FILING_FREQ` varchar(1) DEFAULT NULL,
  `ORG_TP` varchar(1) DEFAULT NULL,
  `CONNECTED_ORG_NM` varchar(200) DEFAULT NULL,
  `CAND_ID` varchar(9) DEFAULT NULL,
  `idcomittee` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`idcomittee`)
) ENGINE=InnoDB AUTO_INCREMENT=20387951 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `indiv`
--

DROP TABLE IF EXISTS `indiv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `indiv` (
  `CMTE_ID` varchar(9) NOT NULL,
  `AMNDT_IND` varchar(1) DEFAULT NULL,
  `RPT_TP` varchar(3) DEFAULT NULL,
  `TRANSACTION_PGI` varchar(5) DEFAULT NULL,
  `IMAGE_NUM` varchar(18) DEFAULT NULL,
  `TRANSACTION_TP` varchar(3) DEFAULT NULL,
  `ENTITY_TP` varchar(3) DEFAULT NULL,
  `NAME` varchar(200) NOT NULL,
  `CITY` varchar(30) DEFAULT NULL,
  `STATE` varchar(2) DEFAULT NULL,
  `ZIP_CODE` varchar(9) DEFAULT NULL,
  `EMPLOYER` varchar(38) DEFAULT NULL,
  `OCCUPATION` varchar(38) DEFAULT NULL,
  `TRANSACTION_DT` varchar(8) DEFAULT NULL,
  `TRANSACTION_AMT` float(14,2) DEFAULT NULL,
  `OTHER_ID` varchar(9) DEFAULT NULL,
  `TRAN_ID` varchar(32) DEFAULT NULL,
  `FILE_NUM` int(22) DEFAULT NULL,
  `MEMO_CD` varchar(1) DEFAULT NULL,
  `MEMO_TEXT` varchar(100) DEFAULT NULL,
  `SUB_ID` int(19) NOT NULL,
  `idindiv` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`idindiv`)
) ENGINE=InnoDB AUTO_INCREMENT=38990579 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
