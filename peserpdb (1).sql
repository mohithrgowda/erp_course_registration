-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 10, 2022 at 07:59 PM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 8.0.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `peserpdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `backlogdata`
--

CREATE TABLE `backlogdata` (
  `Id` int(11) NOT NULL,
  `USN` varchar(100) DEFAULT NULL,
  `Course` varchar(100) DEFAULT NULL,
  `Sem` varchar(100) DEFAULT NULL,
  `Subject` varchar(100) DEFAULT NULL,
  `Scode` varchar(50) NOT NULL,
  `Credits` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `backlogdata`
--

INSERT INTO `backlogdata` (`Id`, `USN`, `Course`, `Sem`, `Subject`, `Scode`, `Credits`) VALUES
(1, '4vm10mca89', 'Automobile', '2', 'test', '', ''),
(2, '4vm10mca89', 'Civil', '5', 'dede', '', ''),
(3, '4PS16CS045', 'Computer Science', '4', 'Test', 'Ps123', '5');

-- --------------------------------------------------------

--
-- Table structure for table `electivesdata`
--

CREATE TABLE `electivesdata` (
  `Id` int(11) NOT NULL,
  `Subject` varchar(100) DEFAULT NULL,
  `Stype` varchar(100) DEFAULT NULL,
  `Course` varchar(100) DEFAULT NULL,
  `Sem` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `electivesdata`
--

INSERT INTO `electivesdata` (`Id`, `Subject`, `Stype`, `Course`, `Sem`) VALUES
(2, 'Demo', 'BSC(Basic Science Course)', 'Automobile', '1');

-- --------------------------------------------------------

--
-- Table structure for table `hoddata`
--

CREATE TABLE `hoddata` (
  `Id` int(11) NOT NULL,
  `Uname` varchar(50) NOT NULL,
  `Pswd` varchar(50) NOT NULL,
  `Dept` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `hoddata`
--

INSERT INTO `hoddata` (`Id`, `Uname`, `Pswd`, `Dept`) VALUES
(1, 'Cshod#1', 'hod#1', 'Computer Science'),
(2, 'ishod#1', 'hod#1', 'Information Science'),
(3, 'mehod#1', 'hod#1', 'Mechanical'),
(4, 'eehod#1', 'hod#1', 'Electrical and electronics'),
(5, 'echod#1', 'hod#1', 'Electronics and communication');

-- --------------------------------------------------------

--
-- Table structure for table `mentordata`
--

CREATE TABLE `mentordata` (
  `Id` int(11) NOT NULL,
  `Mname` varchar(100) DEFAULT NULL,
  `Course` varchar(100) DEFAULT NULL,
  `Sem` varchar(100) DEFAULT NULL,
  `Uname` varchar(100) DEFAULT NULL,
  `Pswd` varchar(100) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `mentordata`
--

INSERT INTO `mentordata` (`Id`, `Mname`, `Course`, `Sem`, `Uname`, `Pswd`, `Email`) VALUES
(2, 'ddd', 'Automobile', '2', 'Shushruth2697', 'qazwsx', 'madhsunil@gmail.com'),
(3, 'ddd', 'Computer Science', '5', 'Shushruth2697', 'qazwsx', 'madhsunil@gmail.com'),
(4, 'Jainam', 'Computer Science', '3', 'Jain', 'qqq', 'mailtoboyka@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `rounddata`
--

CREATE TABLE `rounddata` (
  `Id` int(11) NOT NULL,
  `Sdate` varchar(50) DEFAULT NULL,
  `Edate` varchar(50) DEFAULT NULL,
  `Round` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `rounddata`
--

INSERT INTO `rounddata` (`Id`, `Sdate`, `Edate`, `Round`) VALUES
(2, '2022-07-10', '2022-07-10', '1'),
(3, '2022-07-11', '2022-07-11', '2'),
(4, '2022-07-12', '2022-07-12', '3');

-- --------------------------------------------------------

--
-- Table structure for table `stualloc`
--

CREATE TABLE `stualloc` (
  `Id` int(11) NOT NULL,
  `Uname` varchar(100) DEFAULT NULL,
  `USN` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `stualloc`
--

INSERT INTO `stualloc` (`Id`, `Uname`, `USN`) VALUES
(2, 'Shushruth2697', '4PS18CS073'),
(3, 'Shushruth2697', '4PS16CS045'),
(4, 'Jain', '4PS16CS045');

-- --------------------------------------------------------

--
-- Table structure for table `studentdata`
--

CREATE TABLE `studentdata` (
  `USN` varchar(20) DEFAULT NULL,
  `Name` varchar(50) DEFAULT NULL,
  `Dept` varchar(50) DEFAULT NULL,
  `Pswd` varchar(50) DEFAULT NULL,
  `CGPA` varchar(50) NOT NULL,
  `Sem` varchar(50) NOT NULL,
  `Phone` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `studentdata`
--

INSERT INTO `studentdata` (`USN`, `Name`, `Dept`, `Pswd`, `CGPA`, `Sem`, `Phone`) VALUES
('4PS16CS045', 'LALNUNMAWIA HD ', 'Computer Science', 'student@1234', '6.38', '8', '9902585285'),
('4PS16CS057', 'LAWMTHARZELA', 'Computer Science', 'student@1234', '6.38', '8', '9902585285'),
('4PS17CS103', 'SUHAS H', 'Computer Science', 'student@1234', '6.38', '8', '9902585285'),
('4PS18CS027 ', 'DAIVIK GOWDA', 'Computer Science', 'student@1234', '6.38', '8', '9902585285'),
('4PS18CS048', 'KRUTHIK B R', 'Computer Science', 'student@1234', '5.45', '8', '9902585285'),
('4PS18CS073', 'PRANADHIHARAN ', 'Computer Science', 'student@1234', '5.45', '8', '9902585285'),
('4PS18CS114', 'THEJAS .S', 'Computer Science', 'student@1234', '5.45', '8', '9902585285'),
('4PS18CS122', 'VISHRUTH', 'Computer Science', 'student@1234', '5.45', '8', '9902585285'),
('4PS19CS002', 'ABHISHEK ANAND', 'Computer Science', 'student@1234', '5.45', '8', '9902585285'),
('4PS19CS003', 'ABHIYANSHU SAHU', 'Computer Science', 'student@1234', '5.45', '8', '9902585285'),
('4PS19CS004', 'ADARSH RAJ', 'Computer Science', 'student@1234', '8.32', '8', '9902585285'),
('4PS19CS005', 'ADARSH SINGH', 'Computer Science', 'student@1234', '8.32', '8', '9902585285'),
('4PS19CS006', 'AISHWARYA PADKI', 'Computer Science', 'student@1234', '8.32', '8', '9902585285'),
('4PS19CS007', 'AKSHAT KUMAR', 'Computer Science', 'student@1234', '8.32', '8', '9902585285'),
('4PS19CS008', 'AKSHAY HARWALKAR', 'Computer Science', 'student@1234', '8.32', '8', '9902585285'),
('4PS19CS009', 'AKSHAY KUMAR S', 'Computer Science', 'student@1234', '9.33', '8', '9902585285'),
('4PS19CS010', 'AKSHAY N S', 'Computer Science', 'student@1234', '9.33', '8', '9902585285'),
('4PS19CS011', 'ANIMESH GHOSH', 'Computer Science', 'student@1234', '9.33', '8', '9902585285'),
('4PS19CS012', 'ANJALI C', 'Computer Science', 'student@1234', '9.33', '8', '9902585285'),
('4PS19CS013', 'ANNIKA RAI', 'Computer Science', 'student@1234', '9.33', '8', '9902585285'),
('4PS19CS014', 'ANUSHA.H', 'Computer Science', 'student@1234', '9.33', '8', '9902585285'),
('4PS19CS015', 'ANVIKA', 'Computer Science', 'student@1234', '10', '8', '9902585285'),
('4PS19CS016 ', 'ARKA DEEP SHIT', 'Computer Science', 'student@1234', '10', '8', '9902585285'),
('4PS19CS017', 'BALVINDER SINGH', 'Computer Science', 'student@1234', '10', '8', '9902585285'),
('4PS19CS018', 'BHANUPRAKASH ', 'Computer Science', 'student@1234', '10', '8', '9902585285'),
('4PS19CS019', 'BHOOMIKA.H.L', 'Computer Science', 'student@1234', '10', '8', '9902585285'),
('4PS19CS020', 'BHUMIKA R', 'Computer Science', 'student@1234', '10', '8', '9902585285'),
('4PS19CS021', 'BINDUSHREE GS', 'Computer Science', 'student@1234', '10', '8', '9902585285'),
('4PS19CS022', 'LALTHANFELA C', 'Computer Science', 'student@1234', '7.33', '8', '9902585285'),
('4PS19CS023', 'CHANDRASHEKAR M B', 'Computer Science', 'student@1234', '7.33', '8', '9902585285'),
('4PS19CS024', 'D N VEERENDRA PATEL ', 'Computer Science', 'student@1234', '7.33', '8', '9902585285'),
('4PS19CS025', 'DARSHAN GUPTA', 'Computer Science', 'student@1234', '7.33', '8', '9902585285'),
('4PS19CS026', 'DEBADITYA SUTRADHAR', 'Computer Science', 'student@1234', '7.33', '8', '9902585285'),
('4PS19CS027', 'DEVIKA C R', 'Computer Science', 'student@1234', '7.33', '8', '9902585285'),
('4PS19CS028', 'DHANUSH KS', 'Computer Science', 'student@1234', '7.33', '8', '9902585285'),
('4PS19CS029 ', 'DISHA C', 'Computer Science', 'student@1234', '7.33', '8', '9902585285'),
('4PS19CS030', 'DIVYANSH', 'Computer Science', 'student@1234', '8.22', '8', '9902585285'),
('4PS19CS031', 'FAITH BENNY HINN', 'Computer Science', 'student@1234', '8.22', '8', '9902585285'),
('4PS19CS032', 'GURU PRASAD S', 'Computer Science', 'student@1234', '8.22', '8', '9902585285'),
('4PS19CS033', 'HARSH MISHRA', 'Computer Science', 'student@1234', '8.22', '8', '9902585285'),
('4PS19CS034', 'HARSHAN GOWDA H K', 'Computer Science', 'student@1234', '8.22', '8', '9902585285'),
('4PS19CS035', 'HARSHIT RAJ KUMAR', 'Computer Science', 'student@1234', '8.22', '8', '9902585285'),
('4PS19CS036', 'HARSHITHA R', 'Computer Science', 'student@1234', '8.22', '8', '9902585285'),
('4PS19CS037', 'HMINGTHANSANGI KHIANGTE', 'Computer Science', 'student@1234', '7.96', '8', '9902585285'),
('4PS19CS038', 'KEERTHANA_HL', 'Computer Science', 'student@1234', '7.96', '8', '9902585285'),
('4PS19CS039 ', 'KOUSHIK JAYARAM', 'Computer Science', 'student@1234', '7.96', '8', '9902585285'),
('4PS19CS040', 'KRUTHIKA_M', 'Computer Science', 'student@1234', '7.96', '8', '9902585285'),
('4PS19CS041', 'KUMAR SOMU', 'Computer Science', 'student@1234', '7.96', '8', '9902585285'),
('4PS19CS042', 'KUNAL VERMA ', 'Computer Science', 'student@1234', '5.55', '8', '9902585285'),
('4PS19CS043', 'KUSHAL RANGANATH.M.B', 'Computer Science', 'student@1234', '5.54', '8', '9902585285'),
('4PS19CS044', 'KUSHAL S KUMAR', 'Computer Science', 'student@1234', '5.54', '8', '9902585285'),
('4PS19CS045 ', 'L.A SHREE GOWRI', 'Computer Science', 'student@1234', '5.54', '8', '9902585285'),
('4PS19CS046', 'LAKSHMISH R ', 'Computer Science', 'student@1234', '5.54', '8', '9902585285'),
('4PS19CS047', 'LAVANYA S S', 'Computer Science', 'student@1234', '5.54', '8', '9902585285'),
('4PS19CS048', 'LIKHITH J K ', 'Computer Science', 'student@1234', '5.54', '8', '9902585285'),
('4PS19CS049', 'LIKITHA PURUSHOTHAM', 'Computer Science', 'student@1234', '4.25', '8', '9902585285'),
('4PS19CS050', 'MADAN GOWDA PM', 'Computer Science', 'student@1234', '4.25', '8', '9902585285'),
('4PS19CS051', 'MERYL FREEDA DCRUZ', 'Computer Science', 'student@1234', '4.25', '8', '9902585285'),
('4PS19CS052', 'METILDA D SANCHEZ', 'Computer Science', 'student@1234', '4.25', '8', '9902585285'),
('4PS19CS053', 'MICHAEL VANLALHRIATPUIA', 'Computer Science', 'student@1234', '4.25', '8', '9902585285'),
('4PS19CS054', 'MISHKAATH S', 'Computer Science', 'student@1234', '4.25', '8', '9902585285'),
('4PS19CS055', 'MOHAMMED ADNAN', 'Computer Science', 'student@1234', '4.25', '8', '9902585285'),
('4PS19CS056', 'MOHAMMED DANIAL', 'Computer Science', 'student@1234', '6.22', '8', '9902585285'),
('4PS19CS057', 'MONISHA M', 'Computer Science', 'student@1234', '6.22', '8', '9902585285'),
('4PS19CS058', 'MUKESH K C ', 'Computer Science', 'student@1234', '6.22', '8', '9902585285'),
('4PS19CS059', 'MUTUKUNDU MAHENDRA REDDY', 'Computer Science', 'student@1234', '6.22', '8', '9902585285'),
('4PS19CS060', 'GOWTHAM N', 'Computer Science', 'student@1234', '6.22', '8', '9902585285'),
('4PS19CS061', 'NAGAPPA M', 'Computer Science', 'student@1234', '6.22', '8', '9902585285'),
('4PS19CS062', 'NAGARJUNA T R', 'Computer Science', 'student@1234', '6.22', '8', '9902585285'),
('4PS19CS063', 'NAVEEN KUMAR M', 'Computer Science', 'student@1234', '7.62', '8', '9902585285'),
('4PS19CS064 ', 'NAYANKUMAR M', 'Computer Science', 'student@1234', '7.62', '8', '9902585285'),
('4PS19CS065', 'NEELAMBIKA N', 'Computer Science', 'student@1234', '7.62', '8', '9902585285'),
('4PS19CS066', 'NITHYASHREE MP', 'Computer Science', 'student@1234', '7.62', '8', '9902585285'),
('4PS19CS067', 'NITIN JAIN D', 'Computer Science', 'student@1234', '7.62', '8', '9902585285'),
('4PS19CS068', 'OM KUMAR SINGH', 'Computer Science', 'student@1234', '7.62', '8', '9902585285'),
('4PS19CS069', 'PALLAVI S', 'Computer Science', 'student@1234', '7.62', '8', '9902585285'),
('4PS19CS070', 'PANKAJA.M.D', 'Computer Science', 'student@1234', '9.55', '8', '9902585285'),
('4PS19CS071', 'POORVI.MN', 'Computer Science', 'student@1234', '9.55', '8', '9902585285'),
('4PS19CS072', 'PRADIP SINHA', 'Computer Science', 'student@1234', '9.55', '8', '9902585285'),
('4PS19CS073', 'PRAKRUTHI H S', 'Computer Science', 'student@1234', '9.55', '8', '9902585285'),
('4PS19CS074', 'PRAKRUTHI P', 'Computer Science', 'student@1234', '9.55', '8', '9902585285'),
('4PS19CS075', 'PRAYAG RAJ', 'Computer Science', 'student@1234', '9.55', '8', '9902585285'),
('4PS19CS076', 'PREETHAM DEV T B ', 'Computer Science', 'student@1234', '9.55', '8', '9902585285'),
('4PS19CS077', 'PREETHI.M', 'Computer Science', 'student@1234', '7.23', '8', '9902585285'),
('4PS19CS078', 'RACHANA A', 'Computer Science', 'student@1234', '7.23', '8', '9902585285'),
('4PS19CS079', 'RAKESH S ', 'Computer Science', 'student@1234', '7.23', '8', '9902585285'),
('4PS19CS080', 'RAKSHA P', 'Computer Science', 'student@1234', '7.23', '8', '9902585285'),
('4PS19CS081', 'RAKSHITHA HN', 'Computer Science', 'student@1234', '7.23', '8', '9902585285'),
('4PS19CS082', 'RAMESH KUMAR', 'Computer Science', 'student@1234', '7.23', '8', '9902585285'),
('4PS19CS083', 'RENUKA PRASAD SM', 'Computer Science', 'student@1234', '7.23', '8', '9902585285'),
('4PS19CS084', 'RIYA KUMARI', 'Computer Science', 'student@1234', '9.67', '8', '9902585285'),
('4PS19CS085 ', 'ROHINI R', 'Computer Science', 'student@1234', '9.67', '8', '9902585285'),
('4PS19CS086', 'ROUSHAN KUMAR', 'Computer Science', 'student@1234', '9.67', '8', '9902585285'),
('4PS19CS087', 'NIREEKSHA JAIN S S', 'Computer Science', 'student@1234', '9.67', '8', '9902585285'),
('4PS19CS088', 'SAHANA B', 'Computer Science', 'student@1234', '9.67', '8', '9902585285'),
('4PS19CS089', 'SAHANA.R', 'Computer Science', 'student@1234', '9.67', '8', '9902585285'),
('4PS19CS090', 'SAHANA. S', 'Computer Science', 'student@1234', '9.67', '8', '9902585285'),
('4PS19CS091', 'SAHANA S R', 'Computer Science', 'student@1234', '9.67', '8', '9902585285'),
('4PS19CS093', 'SANTHOSH R', 'Computer Science', 'student@1234', '9.67', '8', '9902585285'),
('4PS19CS094', 'SAWIKAR SINGH', 'Computer Science', 'student@1234', '9.67', '8', '9902585285'),
('4PS19CS095', 'SHAHID EQUBAL', 'Computer Science', 'student@1234', '9.67', '8', '9902585285'),
('4PS19CS096', 'SHANU JAISWAL', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS097', 'SHARVARI M S ', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS098', 'SHASHANK GOWDA HS ', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS100', 'SHILPITHA', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS101', 'SHIVAPRASAD D N', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS102', 'SHREEKALA. M. K', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS103', 'SNEHA .R', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS104', 'SOMASUNDAR  M', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS105', 'SONIKA N', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS106', 'SOUMYA SHREYA', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS107', 'SPANDANA C', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS108', 'SPANDANA C S', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS109', 'SREYANJANA SAHA ', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS110', 'STEVE PRATHIK FERNANDES', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS111', 'SUHAS M DEV', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS112', 'SUMUKH S R KASHYAP', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS113', 'SYED MOHAMMAD NOOR UN NABI', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS114', 'TARUN BRAMHENDRA M', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS115', 'TARUN KUMAR', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS116', 'TEJAS N', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS117', 'UDAYADITYA D', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS118', 'UMME HANI', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS119', 'UMME-HANI', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS120', 'VIDHWAN M S', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS121', 'VIDYA BHUSHAN', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS122', 'VIDYA SHREE R', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS123', 'VINUTH K', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS124', 'VISHAL M G', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS125', 'VIVEK SAGAR', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS126', 'YASHUMATHI K L', 'Computer Science', 'student@1234', '6.43', '8', '9902585285'),
('4PS19CS127', 'YUVARANI K S ', 'Computer Science', 'student@1234', '7.45', '8', '9902585285'),
('4PS19CSOO8', 'AKSHAY HARWALKAR', 'Computer Science', 'student@1234', '7.45', '8', '9902585285'),
('4PS20CS400', 'ADNAN AHMED KHAN', 'Computer Science', 'student@1234', '7.45', '8', '9902585285'),
('4PS20CS401', 'AKSHATHA S', 'Computer Science', 'student@1234', '7.45', '8', '9902585285'),
('4PS20CS402', 'ANJALI C', 'Computer Science', 'student@1234', '7.45', '8', '9902585285'),
('4PS20CS403', 'APPU GOWDA K C ', 'Computer Science', 'student@1234', '7.45', '8', '9902585285'),
('4PS20CS404', 'AVINASH J', 'Computer Science', 'student@1234', '7.45', '8', '9902585285'),
('4PS20CS405', 'DEEPIKA', 'Computer Science', 'student@1234', '7.45', '8', '9902585285'),
('4PS20CS406', 'POOJA H M', 'Computer Science', 'student@1234', '6.55', '8', '9902585285'),
('4PS20CS408', 'SHREERAKSHA', 'Computer Science', 'student@1234', '6.55', '8', '9902585285'),
('4PS20CS409', 'SNEHA M', 'Computer Science', 'student@1234', '6.55', '8', '9902585285'),
('4PS20CS410', 'VENKATESH NAIK', 'Computer Science', 'student@1234', '6.55', '8', '9902585285'),
('4PS20CS411', 'VISHAL N R', 'Computer Science', 'student@1234', '6.55', '8', '9902585285');

-- --------------------------------------------------------

--
-- Table structure for table `stuelectives`
--

CREATE TABLE `stuelectives` (
  `Id` int(11) NOT NULL,
  `Scode` varchar(50) DEFAULT NULL,
  `Subject` varchar(50) DEFAULT NULL,
  `Sem` varchar(50) DEFAULT NULL,
  `Credits` varchar(50) DEFAULT NULL,
  `USN` varchar(50) DEFAULT NULL,
  `Stat` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `stupecelectives`
--

CREATE TABLE `stupecelectives` (
  `Id` int(11) NOT NULL,
  `Scode` varchar(50) DEFAULT NULL,
  `Subject` varchar(50) DEFAULT NULL,
  `Sem` varchar(50) DEFAULT NULL,
  `Credits` varchar(50) DEFAULT NULL,
  `USN` varchar(50) DEFAULT NULL,
  `Stat` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `subjectdata`
--

CREATE TABLE `subjectdata` (
  `Id` int(11) NOT NULL,
  `Subject` varchar(500) DEFAULT NULL,
  `Stype` varchar(500) DEFAULT NULL,
  `Course` varchar(500) DEFAULT NULL,
  `Sem` varchar(500) DEFAULT NULL,
  `Credit` varchar(50) NOT NULL,
  `SubCode` varchar(50) NOT NULL,
  `Seats` int(11) NOT NULL,
  `Exclusion` varchar(4000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `subjectdata`
--

INSERT INTO `subjectdata` (`Id`, `Subject`, `Stype`, `Course`, `Sem`, `Credit`, `SubCode`, `Seats`, `Exclusion`) VALUES
(4, 'Software Engineering', 'BSC(Basic Science Course)', 'Computer Science', '8', '4', 'p18cs001', 60, ''),
(5, 'Computer Networks', 'BSC(Basic Science Course)', 'Computer Science', '8', '4', 'p18cs002', 0, ''),
(6, 'Business Intelligence', 'OEC(Open Elective Course)', 'Computer Science', '8', '3', 'p18cs003', 60, 'All Branches'),
(7, 'motors and engines', 'OEC(Open Elective Course)', 'Mechanical', '8', '3', 'p18me004', 40, 'Computer Science,Electronics and Electrical'),
(8, 'building materials', 'OEC(Open Elective Course)', 'Civil', '8', '3', 'p18cs005', 60, 'Civil'),
(9, 'remote sensing ', 'OEC(Open Elective Course)', 'Civil', '8', '3', 'p18cs006', 60, 'Civil'),
(10, 'just in time manufacturing', 'OEC(Open Elective Course)', 'Mechanical', '8', '4', 'p18cs007', 40, 'Mechanical Engineering'),
(11, 'software project management', 'PEC(Professional Elective Course)', 'Computer Science', '8', '4', 'p18csp001', 40, ''),
(12, 'machine learning', 'PEC(Professional Elective Course)', 'Computer Science', '8', '4', 'p18csp002', 40, ''),
(13, 'deep learning ', 'BSC(Basic Science Course)', 'Computer Science', '8', '4', 'p18cs009', 0, ''),
(14, 'html&css&js', 'PEC(Professional Elective Course)', 'Computer Science', '8', '1.5', 'p18csl001', 0, ''),
(15, 'dsa lab', 'ESC(Engineering Science Course)', 'Computer Science', '8', '1.5', 'p18csl002', 0, ''),
(17, 'Construction Management', 'OEC(Open Elective Course)', 'Civil', '8', '4', 'p18cv009', 60, 'Civil'),
(18, 'Production management', 'OEC(Open Elective Course)', 'Industrial Production Engineering', '8', '4', 'p18ip001', 40, 'Industrial');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `backlogdata`
--
ALTER TABLE `backlogdata`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `electivesdata`
--
ALTER TABLE `electivesdata`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `hoddata`
--
ALTER TABLE `hoddata`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `mentordata`
--
ALTER TABLE `mentordata`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `rounddata`
--
ALTER TABLE `rounddata`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `stualloc`
--
ALTER TABLE `stualloc`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `stuelectives`
--
ALTER TABLE `stuelectives`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `stupecelectives`
--
ALTER TABLE `stupecelectives`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `subjectdata`
--
ALTER TABLE `subjectdata`
  ADD PRIMARY KEY (`Id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `backlogdata`
--
ALTER TABLE `backlogdata`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `electivesdata`
--
ALTER TABLE `electivesdata`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `hoddata`
--
ALTER TABLE `hoddata`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `mentordata`
--
ALTER TABLE `mentordata`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `rounddata`
--
ALTER TABLE `rounddata`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `stualloc`
--
ALTER TABLE `stualloc`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `stuelectives`
--
ALTER TABLE `stuelectives`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=77;

--
-- AUTO_INCREMENT for table `stupecelectives`
--
ALTER TABLE `stupecelectives`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `subjectdata`
--
ALTER TABLE `subjectdata`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
