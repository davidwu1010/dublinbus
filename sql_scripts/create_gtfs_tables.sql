CREATE DATABASE IF NOT EXISTS gtfs;

CREATE TABLE IF NOT EXISTS gtfs.Stops(
    StopID VARCHAR(30),
    StopName VARCHAR(50),
    Lat DECIMAL(15, 13),
    Lon DECIMAL(15, 14),
    StopNumber INT,
    PRIMARY KEY (StopID)
);

CREATE TABLE IF NOT EXISTS gtfs.Stop_Times(
    TripID VARCHAR(30),
    ArrivalTime TIME,
    DepartureTime TIME,
    StopID VARCHAR(30),
    StopSequence INT,
    StopHeadsign VARCHAR(30),
    PickupType INT,
    DropOffType INT,
    ShapeDistTraveled DOUBLE(13, 2),
    PRIMARY KEY (TripID, StopSequence)
);

CREATE TABLE IF NOT EXISTS gtfs.Routes(
    RouteID VARCHAR(30),
    ShortName VARCHAR(10),
    PRIMARY KEY (RouteID)
);

CREATE TABLE IF NOT EXISTS gtfs.Shapes(
    ShapeID VARCHAR(30),
    Lat DECIMAL(15, 13),
    Lon DECIMAL(15, 14),
    ShapePtSequence INT,
    ShapeDistTraveled DOUBLE(13, 2),
    PRIMARY KEY (ShapeID, ShapePtSequence)
);

CREATE TABLE IF NOT EXISTS gtfs.Trips(
    RouteID VARCHAR(30),
    ServiceID VARCHAR(10),
    TripID VARCHAR(30),
    ShapeID VARCHAR(30),
    TripHeadsign VARCHAR(100),
    DirectionID INT,
    PRIMARY KEY (TripID)
);

CREATE TABLE IF NOT EXISTS gtfs.Sections(
    Origin VARCHAR(30),
    Dest VARCHAR(30),
    PRIMARY KEY (Origin, Dest)
);