LOAD DATA LOCAL INFILE '~/data/gtfs/stop_times.txt'
INTO TABLE gtfs.Stop_Times
FIELDS
    TERMINATED BY ','
    ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES (
    TripID,
    ArrivalTime,
    DepartureTime,
    StopID,
    StopSequence,
    StopHeadsign,
    PickupType,
    DropOffType,
    ShapeDistTraveled
);