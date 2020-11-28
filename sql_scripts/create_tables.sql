CREATE DATABASE IF NOT EXISTS dublinbus;

CREATE TABLE dublinbus.RT_Vehicles(
    DataSource VARCHAR(4),
    DayOfService DATETIME,
    VehicleID VARCHAR(10), 
    Distance INT,
    Minutes INT,
    LastUpdate DATETIME NOT NULL,
    Note VARCHAR(255),
    PRIMARY KEY (DataSource, DayOfService, VehicleID)
);

CREATE TABLE dublinbus.RT_Trips(
    DataSource VARCHAR(4),
    DayOfService DATETIME,
    TripID VARCHAR(30),
    LineID VARCHAR(10),
    RouteID VARCHAR(20),
    Direction VARCHAR(2),
    PlannedTime_Dep INT,
    PlannedTime_Arr INT,
    Basin VARCHAR(20),
    TenderLot VARCHAR(30),
    ActualTime_Dep INT,
    ActualTime_Arr INT,
    Suppressed INT,
    JustificationID INT,
    LastUpdate DATETIME NOT NULL,
    Note VARCHAR(255),
    PRIMARY KEY (DataSource, DayOfService, TripID)
);

CREATE TABLE dublinbus.RT_LeaveTimes(
    DayOfService DATE,
    TripID VARCHAR(15),
    ProgrNumber INT,
    StopPointID VARCHAR(16),
    PlannedTime_Arr INT,
    ActualTime_Arr INT,
    ActualTime_Dep INT,
    VehicleID VARCHAR(10),
    PRIMARY KEY (DayOfService, TripID, ProgrNumber)
);


CREATE DATABASE IF NOT EXISTS db_product;

CREATE DATABASE IF NOT EXISTS db_test;
USE dublinbus;

CREATE TABLE `his_weather` (
  `dt` int(10) COMMENT 'weather update timestamp, pk',
  `temp` float(5,2) NOT NULL DEFAULT 99.99 COMMENT  'Celsius temperature',
  `feels_like` float(5,2) NOT NULL DEFAULT 99.99 COMMENT  'feels-like temperature in Celsius',
  `temp_min` float(5,2) NOT NULL DEFAULT 99.99 COMMENT 'Celsius temperature',
  `temp_max` float(5,2) NOT NULL DEFAULT 99.99 COMMENT 'Celsius temperature',
  `pressure` int(10) NOT NULL DEFAULT 0 COMMENT 'atm pressure,hPa',
  `humidity` int(10) NOT NULL DEFAULT 0 COMMENT 'humidity, %',
  `wind_speed` float(5,2) NOT NULL DEFAULT 0 COMMENT 'wind speed, m/s',
  `wind_deg` int(10) NOT NULL DEFAULT 999 COMMENT 'wind direction, degrees(meteorological)',
  `clouds` int(10) NOT NULL DEFAULT 999 COMMENT 'cloudiness, %',
  `weather_id` int(11) NOT NULL DEFAULT 0 COMMENT '3-digit id represents main weather',
  `weather_main` VARCHAR(32) DEFAULT NULL COMMENT 'weather main, describe weather_id',
  `weather_desc` VARCHAR(128) DEFAULT NULL COMMENT 'weather desc',
  PRIMARY KEY (`dt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


USE db_product;

CREATE TABLE `cur_weather` (
  `dt` int(10) COMMENT 'weather update timestamp, every 30 min',
  `temp` float(5,2) NOT NULL DEFAULT 99.99 COMMENT  'Celsius temperature',
  `feels_like` float(5,2) NOT NULL DEFAULT 99.99 COMMENT  'feels-like temperature in Celsius',
  `temp_min` float(5,2) NOT NULL DEFAULT 99.99 COMMENT 'Celsius temperature',
  `temp_max` float(5,2) NOT NULL DEFAULT 99.99 COMMENT 'Celsius temperature',
  `pressure` int(10) NOT NULL DEFAULT 0 COMMENT 'atm pressure,hPa',
  `humidity` int(10) NOT NULL DEFAULT 0 COMMENT 'humidity, %',
  `wind_speed` float(5,2) NOT NULL DEFAULT 0 COMMENT 'wind speed, m/s',
  `wind_deg` int(10) NOT NULL DEFAULT 999 COMMENT 'wind direction, degrees(meteorological)',
  `clouds` int(10) NOT NULL DEFAULT 999 COMMENT 'cloudiness, %',
  `weather_id` int(11) NOT NULL DEFAULT 0 COMMENT '3-digit id represents main weather',
  `weather_main` VARCHAR(32) DEFAULT NULL COMMENT 'describe weather_id',
  `weather_desc` VARCHAR(128) DEFAULT NULL COMMENT 'weather desc',
  `modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'last modify time',
  PRIMARY KEY (`dt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;