LOAD DATA LOCAL INFILE '~/data/gtfs/shapes.txt'
INTO TABLE gtfs.Shapes
FIELDS
    TERMINATED BY ','
    ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES (
    ShapeID,
    Lat,
    Lon,
    ShapePtSequence,
    ShapeDistTraveled
);