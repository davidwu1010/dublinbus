# Delete routes that have no trips

DELETE FROM gtfs.Routes WHERE RouteID IN (
    SELECT RouteID 
    FROM (SELECT * FROM gtfs.Routes) AS R
    WHERE NOT EXISTS (SELECT * FROM gtfs.Trips T WHERE T.RouteID = R.RouteID));