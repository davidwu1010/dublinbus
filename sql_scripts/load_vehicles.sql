LOAD DATA LOCAL INFILE '~/data/rt_vehicles_DB_2018.txt'
INTO TABLE dublinbus.RT_Vehicles
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(DataSource, @DayOfService, VehicleID, Distance, Minutes, @LastUpdate, Note)
SET DayOfService = STR_TO_DATE(@DayOfService, '%d-%b-%y %H:%i:%s'),
    LastUpdate = STR_TO_DATE(@LastUpdate, '%d-%b-%y %H:%i:%s');