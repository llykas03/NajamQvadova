-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 20, 2025 at 06:41 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `iznajmljivanjevozila`
--

-- --------------------------------------------------------

--
-- Table structure for table `istorija_iznajmljivanja`
--

CREATE TABLE `istorija_iznajmljivanja` (
  `id` int(11) NOT NULL,
  `korisnik_id` int(11) NOT NULL,
  `kvad_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `istorija_iznajmljivanja`
--

INSERT INTO `istorija_iznajmljivanja` (`id`, `korisnik_id`, `kvad_id`) VALUES
(10, 12, 3),
(12, 1, 4),
(13, 1, 6),
(15, 1, 4),
(16, 1, 4),
(17, 1, 6);

-- --------------------------------------------------------

--
-- Table structure for table `korisnici`
--

CREATE TABLE `korisnici` (
  `id` int(11) NOT NULL,
  `ime` varchar(100) NOT NULL,
  `prezime` varchar(100) NOT NULL,
  `srednje_ime` varchar(100) DEFAULT NULL,
  `jmbg` varchar(13) NOT NULL,
  `broj_licne_karte` varchar(20) NOT NULL,
  `lozinka` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `trenutniKorisnik` int(11) DEFAULT NULL,
  `kredit` decimal(10,2) DEFAULT 0.00,
  `rola` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `korisnici`
--

INSERT INTO `korisnici` (`id`, `ime`, `prezime`, `srednje_ime`, `jmbg`, `broj_licne_karte`, `lozinka`, `email`, `trenutniKorisnik`, `kredit`, `rola`) VALUES
(1, 'Mihajlo', 'Cekić', 'Ivica', '1234567890123', 'A123456789', 'root', 'root@gmail.com', 6, 490.00, 'administrator'),
(2, 'Marko', 'Jovanović', 'Stefan', '2345678901234', 'B234567890', 'lozinka234', 'marko@example.com', NULL, 1000.00, 'user'),
(3, 'Ana', 'Petrović', 'Maja', '3456789012345', 'C345678901', 'lozinka345', 'ana@example.com', NULL, 1000.00, 'user'),
(4, 'Jovana', 'Nikolić', 'Ivana', '4567890123456', 'D456789012', 'lozinka456', 'jovana@example.com', NULL, 2000.00, 'user'),
(5, 'Luka', 'Stojanović', 'Lazar', '5678901234567', 'E567890123', 'lozinka567', 'luka@example.com', NULL, 1000.00, 'user'),
(6, 'Nikola', 'Savić', 'Nemanja', '6789012345678', 'F678901234', 'lozinka678', 'nikola@example.com', NULL, 1000.00, 'user'),
(7, 'Ivana', 'Milić', 'Tanja', '7890123456789', 'G789012345', 'lozinka789', 'ivana@example.com', NULL, 1000.00, 'user'),
(9, 'Teodora', 'Vuković', 'Jovana', '9012345678901', 'I901234567', 'lozinka901', 'teodora@example.com', NULL, 1000.00, 'user'),
(12, 'Luka', 'Stojanović', 'aa', '2509003730074', '01123456789', 'luka', 'luka@gmail.com', NULL, 4300.00, 'user');

-- --------------------------------------------------------

--
-- Table structure for table `vozila`
--

CREATE TABLE `vozila` (
  `id` int(11) NOT NULL,
  `brojIznajmljivanja` int(11) NOT NULL,
  `cenaRadnogSata` int(11) NOT NULL,
  `satnicaUkupna` int(11) NOT NULL,
  `ime` varchar(255) NOT NULL,
  `boja` varchar(255) NOT NULL,
  `registracija` varchar(255) NOT NULL,
  `gorivo` varchar(255) NOT NULL,
  `motor` varchar(255) NOT NULL,
  `kubikaza` varchar(255) NOT NULL,
  `konjskeSnage` varchar(255) NOT NULL,
  `statusVozila` varchar(255) NOT NULL,
  `godinaProizvodnje` varchar(255) NOT NULL,
  `urlSlika` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vozila`
--

INSERT INTO `vozila` (`id`, `brojIznajmljivanja`, `cenaRadnogSata`, `satnicaUkupna`, `ime`, `boja`, `registracija`, `gorivo`, `motor`, `kubikaza`, `konjskeSnage`, `statusVozila`, `godinaProizvodnje`, `urlSlika`) VALUES
(3, 3, 70, 1, 'Polaris Sportsman', 'Crvena', 'KG456CD', 'Benzin', 'Jednocilindrični', '600', '44', 'Slobodno', '2021', 'https://drive.google.com/uc?export=view&id=1TuHRuCv-4cbuUo2zu7W7ksCyGzguhV6X'),
(4, 3, 70, 8, 'Honda TRX 450', 'Crna', 'NS789EF', 'Benzin', 'Četvorotaktni', '450', '40', 'Zauzeto', '2018', 'https://drive.google.com/uc?export=view&id=1kalvmN5isiGa7PgnvHpTZ5Rh0aHUmvfQ'),
(6, 2, 50, 6, 'Linhai 500l', 'crvena', 'le123do', 'benzin', 'jednocilindricni', '500', '40', 'Zauzeto', '2016', 'https://drive.google.com/uc?export=view&id=1kalvmN5isiGa7PgnvHpTZ5Rh0aHUmvfQ');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `istorija_iznajmljivanja`
--
ALTER TABLE `istorija_iznajmljivanja`
  ADD PRIMARY KEY (`id`),
  ADD KEY `korisnik_id` (`korisnik_id`),
  ADD KEY `kvad_id` (`kvad_id`);

--
-- Indexes for table `korisnici`
--
ALTER TABLE `korisnici`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `jmbg` (`jmbg`),
  ADD UNIQUE KEY `broj_licne_karte` (`broj_licne_karte`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `trenutniKorisnik` (`trenutniKorisnik`);

--
-- Indexes for table `vozila`
--
ALTER TABLE `vozila`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `istorija_iznajmljivanja`
--
ALTER TABLE `istorija_iznajmljivanja`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `korisnici`
--
ALTER TABLE `korisnici`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `vozila`
--
ALTER TABLE `vozila`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `istorija_iznajmljivanja`
--
ALTER TABLE `istorija_iznajmljivanja`
  ADD CONSTRAINT `istorija_iznajmljivanja_ibfk_1` FOREIGN KEY (`korisnik_id`) REFERENCES `korisnici` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `istorija_iznajmljivanja_ibfk_2` FOREIGN KEY (`kvad_id`) REFERENCES `vozila` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `korisnici`
--
ALTER TABLE `korisnici`
  ADD CONSTRAINT `korisnici_ibfk_1` FOREIGN KEY (`trenutniKorisnik`) REFERENCES `vozila` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
