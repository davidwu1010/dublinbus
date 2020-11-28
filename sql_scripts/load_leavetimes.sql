SET autocommit=0;

LOAD DATA LOCAL INFILE '~/data/rt_leavetimes_DB_2018.txt'
INTO TABLE dublinbus.RT_LeaveTimes
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
IGNORE 1 LINES(   
    @DataSource,
    @DayOfService,
    TripID,
    ProgrNumber,
    StopPointID,
    PlannedTime_Arr,
    @PlannedTime_Dep,
    ActualTime_Arr,
    ActualTime_Dep,
    VehicleID,
    @Passengers,
    @PassengersIn,
    @PassengersOut,
    @Distance,
    @Suppressed,
    @JustificationID,
    @LastUpdate,
    @Note
)
SET DayOfService = DATE(STR_TO_DATE(@DayOfService, '%d-%b-%y %H:%i:%s'));

COMMIT;