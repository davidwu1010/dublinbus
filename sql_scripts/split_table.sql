CREATE TABLE IF NOT EXISTS dublinbus.Jan_LeaveTimes(PRIMARY KEY(DayOfService, TripID, ProgrNumber))
    SELECT *
    FROM dublinbus.RT_LeaveTimes
    WHERE month(DayOfService) = 1;

CREATE TABLE IF NOT EXISTS dublinbus.Feb_LeaveTimes(PRIMARY KEY(DayOfService, TripID, ProgrNumber))
    SELECT *
    FROM dublinbus.RT_LeaveTimes
    WHERE month(DayOfService) = 2;

CREATE TABLE IF NOT EXISTS dublinbus.Mar_LeaveTimes(PRIMARY KEY(DayOfService, TripID, ProgrNumber))
    SELECT *
    FROM dublinbus.RT_LeaveTimes
    WHERE month(DayOfService) = 3;

CREATE TABLE IF NOT EXISTS dublinbus.Apr_LeaveTimes(PRIMARY KEY(DayOfService, TripID, ProgrNumber))
    SELECT *
    FROM dublinbus.RT_LeaveTimes
    WHERE month(DayOfService) = 4;

CREATE TABLE IF NOT EXISTS dublinbus.May_LeaveTimes(PRIMARY KEY(DayOfService, TripID, ProgrNumber))
    SELECT *
    FROM dublinbus.RT_LeaveTimes
    WHERE month(DayOfService) = 5;

CREATE TABLE IF NOT EXISTS dublinbus.Jun_LeaveTimes(PRIMARY KEY(DayOfService, TripID, ProgrNumber))
    SELECT *
    FROM dublinbus.RT_LeaveTimes
    WHERE month(DayOfService) = 6;

CREATE TABLE IF NOT EXISTS dublinbus.Jul_LeaveTimes(PRIMARY KEY(DayOfService, TripID, ProgrNumber))
    SELECT *
    FROM dublinbus.RT_LeaveTimes
    WHERE month(DayOfService) = 7;

CREATE TABLE IF NOT EXISTS dublinbus.Aug_LeaveTimes(PRIMARY KEY(DayOfService, TripID, ProgrNumber))
    SELECT *
    FROM dublinbus.RT_LeaveTimes
    WHERE month(DayOfService) = 8;

CREATE TABLE IF NOT EXISTS dublinbus.Sep_LeaveTimes(PRIMARY KEY(DayOfService, TripID, ProgrNumber))
    SELECT *
    FROM dublinbus.RT_LeaveTimes
    WHERE month(DayOfService) = 9;

CREATE TABLE IF NOT EXISTS dublinbus.Oct_LeaveTimes(PRIMARY KEY(DayOfService, TripID, ProgrNumber))
    SELECT *
    FROM dublinbus.RT_LeaveTimes
    WHERE month(DayOfService) = 10;

CREATE TABLE IF NOT EXISTS dublinbus.Nov_LeaveTimes(PRIMARY KEY(DayOfService, TripID, ProgrNumber))
    SELECT *
    FROM dublinbus.RT_LeaveTimes
    WHERE month(DayOfService) = 11;

CREATE TABLE IF NOT EXISTS dublinbus.Dec_LeaveTimes(PRIMARY KEY(DayOfService, TripID, ProgrNumber))
    SELECT *
    FROM dublinbus.RT_LeaveTimes
    WHERE month(DayOfService) = 12;
