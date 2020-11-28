LOAD DATA LOCAL INFILE '~/data/gtfs/routes.txt'
INTO TABLE gtfs.Routes
FIELDS
    TERMINATED BY ','
    ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES (
    RouteID,
    @AgencyID,
    ShortName,
    @LongName,
    @RouteType
);