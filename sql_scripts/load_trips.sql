LOAD DATA LOCAL INFILE '~/data/rt_trips_DB_2018.txt'
INTO TABLE dublinbus.RT_Trips
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
IGNORE 1 LINES (
    DataSource,
    @DayOfService,
    TripID,
    LineID,
    RouteID,
    Direction,
    PlannedTime_Arr,
    PlannedTime_Dep,
    @ActualTime_Arr,
    @ActualTime_Dep,
    Basin,
    TenderLot,
    @Suppressed,
    @JustificationID,
    @LastUpdate,
    Note
)
SET DayOfService = STR_TO_DATE(@DayOfService, '%d-%b-%y %H:%i:%s'),
    LastUpdate = STR_TO_DATE(@LastUpdate, '%d-%b-%y %H:%i:%s'),
    Suppressed = NULLIF(@Suppressed, ''),
    JustificationID = NULLIF(@JustificationID, ''),
    ActualTime_Arr = NULLIF(@ActualTime_Arr, ''),
    ActualTime_Dep = NULLIF(@ActualTime_Dep, '');