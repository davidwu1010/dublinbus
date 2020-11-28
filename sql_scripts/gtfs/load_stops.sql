LOAD DATA LOCAL INFILE '~/data/gtfs/stops.txt'
INTO TABLE gtfs.Stops
FIELDS
    TERMINATED BY ','
    ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES (
    StopID,
    StopName,
    Lat,
    Lon
)
SET StopNumber = -1;

DELETE FROM gtfs.Stops WHERE StopName Like 'Virtual Stop%';