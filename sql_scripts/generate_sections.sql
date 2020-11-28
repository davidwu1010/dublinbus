CREATE TABLE IF NOT EXISTS dublinbus.Jan_Sections (PRIMARY KEY (DayOfService, TripID, Origin, Dest))
    SELECT
        LT.DayOfService,
        DAYOFWEEK(LT.DayOfService) AS DayOfWeek,
        LT.TripID,
        ProgrNumber,
        StopPointID AS Origin,
        IF(LT.TripID = LEAD(LT.TripID) OVER w, LEAD(LT.StopPointID) OVER w, -1) AS Dest,
        LT.ActualTime_Dep,
        LineID,
        RouteID,
        VehicleID,
        LEAD(LT.ActualTime_Arr) OVER w - LT.ActualTime_Dep AS TravelTime,
        FROM_UNIXTIME(UNIX_TIMESTAMP(LT.DayOfService) + LT.ActualTime_Dep) AS Time,
        UNIX_TIMESTAMP(LT.DayOfService) + LT.ActualTime_Dep - MOD(LT.ActualTime_Dep, 3600) AS Weatherdt
    FROM dublinbus.Jan_LeaveTimes LT INNER JOIN dublinbus.RT_Trips T
        ON LT.DayOfService = T.DayOfService AND LT.TripID = T.TripID
    WINDOW w AS (ORDER BY LT.DayOfService, LT.TripID, LT.ProgrNumber);