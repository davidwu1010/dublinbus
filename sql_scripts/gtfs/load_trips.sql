LOAD DATA LOCAL INFILE '~/data/gtfs/trips.txt'
INTO TABLE gtfs.Trips
FIELDS
    TERMINATED BY ','
    ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES (
    RouteID,
    ServiceID,
    TripID,
    ShapeID,
    TripHeadsign,
    DirectionID
);