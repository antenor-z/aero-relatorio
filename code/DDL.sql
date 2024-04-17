CREATE TABLE `City` (
  `CityName` varchar(50) NOT NULL,
  PRIMARY KEY (`CityName`)
);

CREATE TABLE `Aerodrome` (
  `ICAO` varchar(4) NOT NULL,
  `AerodromeName` varchar(100) NOT NULL,
  `City` varchar(100) NOT NULL,
  `Latitude` decimal(9,6) NOT NULL,
  `Longitude` decimal(9,6) NOT NULL,
  `METAR` varchar(100),
  PRIMARY KEY (`ICAO`),
  UNIQUE KEY `AerodromeName` (`AerodromeName`),
  KEY `City` (`City`),
  FOREIGN KEY (`City`) REFERENCES `City` (`CityName`)
);

CREATE TABLE `CommunicationType` (
  `CommType` varchar(20) NOT NULL,
  PRIMARY KEY (`CommType`)
);

CREATE TABLE `Communication` (
  `ICAO` varchar(4) NOT NULL,
  `Frequency` decimal(6,3) NOT NULL,
  `CommType` varchar(20) NOT NULL,
  PRIMARY KEY (`ICAO`,`Frequency`),
  UNIQUE KEY `ICAO` (`ICAO`,`Frequency`),
  KEY `CommType` (`CommType`),
  FOREIGN KEY (`ICAO`) REFERENCES `Aerodrome` (`ICAO`),
  FOREIGN KEY (`CommType`) REFERENCES `CommunicationType` (`CommType`)
);

CREATE TABLE `PavementType` (
  `Code` varchar(3) NOT NULL,
  `Material` varchar(50) NOT NULL,
  PRIMARY KEY (`Code`)
);

CREATE TABLE `Runway` (
  `ICAO` varchar(4) NOT NULL,
  `Head1` varchar(3) NOT NULL,
  `Head2` varchar(3) NOT NULL,
  `RunwayLength` int(11) NOT NULL,
  `RunwayWidth` int(11) DEFAULT NULL,
  `PavementCode` varchar(3) DEFAULT NULL,
  PRIMARY KEY (`ICAO`,`Head1`),
  UNIQUE KEY `ICAO` (`ICAO`,`Head1`,`Head2`),
  KEY `PavementCode` (`PavementCode`),
  FOREIGN KEY (`ICAO`) REFERENCES `Aerodrome` (`ICAO`),
  FOREIGN KEY (`PavementCode`) REFERENCES `PavementType` (`Code`)
);

CREATE TABLE `ILSCategory` (
  `Category` varchar(10) NOT NULL,
  PRIMARY KEY (`Category`)
);

CREATE TABLE `ILS` (
  `ICAO` varchar(4) NOT NULL,
  `Ident` varchar(20) NOT NULL,
  `RunwayHead` varchar(3) NOT NULL,
  `Frequency` decimal(6,3) NOT NULL,
  `Category` varchar(10) NOT NULL,
  `CRS` varchar(10) NOT NULL,
  `Minimum` int(11) DEFAULT NULL,
  PRIMARY KEY (`ICAO`,`Ident`),
  UNIQUE KEY `ICAO` (`ICAO`,`Frequency`),
  KEY `Category` (`Category`),
  FOREIGN KEY (`ICAO`) REFERENCES `Aerodrome` (`ICAO`),
  FOREIGN KEY (`Category`) REFERENCES `ILSCategory` (`Category`)
);

CREATE TABLE `VOR` (
  `ICAO` varchar(4) NOT NULL,
  `Ident` varchar(20) NOT NULL,
  `Frequency` decimal(6,3) NOT NULL,
  PRIMARY KEY (`ICAO`,`Ident`),
  UNIQUE KEY `ICAO` (`ICAO`,`Frequency`),
  FOREIGN KEY (`ICAO`) REFERENCES `Aerodrome` (`ICAO`)
);