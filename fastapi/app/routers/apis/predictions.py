import time
import holidays
from datetime import datetime, timedelta
import numpy as np
from numpy import nan

from fastapi import APIRouter

from app.db import crud
from app.routers.deps import (
    get_stops_by_route, 
    get_section,
    get_distance_dict,
    get_db,
    get_booster,
    cache,
    )



stops_by_route_dict = get_stops_by_route()
db = get_db()


router = APIRouter()


@router.get(  
    '/{route_id}',
    tags=['predictions'],
    summary='Return the travel time prediction',
)
async def get_prediction(
        route_id: str,
        origin: int,
        dest: int,
        dtime: datetime,
):
    @cache.cache(ttl=3600)
    def handler(route_id, origin, dest, dtime_str):
        dtime = datetime.strptime(dtime_str, '%Y-%m-%d %H:%M:%S')
        stops = get_stops(route_id, origin, dest)
        sections = get_sections(stops)
        travelTime = []
        dt = datetime2dt(dtime)
        weather = crud.get_weather(dt)
        for section in sections:
            input_data = get_input_data(section, dtime, weather)
            data = np.array([list(input_data.values())])
            prediction = bst.inplace_predict(data)[0]
            travelTime.append(prediction)
        return {'travelTime': sum(travelTime)}
    dtime_str = dtime.__str__().split('.')[0]
    bst = get_booster(dtime.month)
    res = handler(route_id, origin, dest, dtime_str)
    return res


def datetime2dt(dtime):
    ts = datetime.timestamp(dtime)
    now = int(time.time())
    limit = 3600 * 24 * 7
    if ts > now + limit:
        day = dtime + timedelta(days=7)
        ts = 13 * 3600 + datetime.timestamp(
            day.replace(hour=0, minute=0, second=0, microsecond=0)
        )
    elif ts < now:
        ts = now // 100 * 100
    elif ts <= now + 3600 * 24 * 2:
        ts = ts - (ts % 1800)
    else:
        ts = 13 * 3600 + datetime.timestamp(
            dtime.replace(hour=0, minute=0, second=0, microsecond=0)
            )
    return int(ts)


def get_stops(route_id, origin, dest):
    outbound = stops_by_route_dict[route_id]['outbound']
    stops = get_section(outbound, origin, dest)
    if stops:
        return stops
    else:
        inbound = stops_by_route_dict[route_id]['inbound']
        stops = get_section(inbound, origin, dest)
        return stops


def get_sections(stops):
    res = []
    for idx, stop in enumerate(stops[:-1]):
        section = (stop['stopNumber'], stops[idx+1]['stopNumber'])
        res.append(section)
    return res


def get_distance(start, end):
    distance_dic = get_distance_dict()
    return distance_dic.get(str(start), {}).get(str(end), 0)


def get_extre_weather(weather_id):
    extreme_weather_id = [202,212,232,502,503,504,602,622,701,711,721,731,741,751,761,762,771,781]
    return weather_id in extreme_weather_id


def get_input_data(section, dtime, weather):
    res = {
        'hour': dtime.hour,
        'first_stop': section[0],
        'second_stop': section[1],
        'dayOfWeek': dtime.weekday(),
        'holiday': dtime in holidays.Ireland(),
        'distance': get_distance(section[0], section[1]),
        'temp': nan,
        'humidity': nan,
        'wind_speed': nan,
        'clouds': nan,
        'extre_weather': nan,
        'weather_clear': nan,
        'weather_clouds': nan,
        'weather_drizzle': nan,
        'weather_fog': nan,
        'weather_mist': nan,
        'weather_rain': nan,
        'weather_snow': nan,
    }
    if not weather:
        return res
    res['temp'] = weather.temp if weather.temp != 99.99 else nan
    res['humidity'] = weather.humidity if weather.humidity != 0.0 else nan
    res['wind_speed'] = weather.wind_speed if weather.wind_speed != 0 else nan
    res['clouds'] = weather.clouds if weather.clouds <= 100 else nan
    res['extre_weather'] = get_extre_weather(weather.weather_id)
    res['weather_clear'] = True if weather.weather_id == 800 else False
    res['weather_clouds'] = True if weather.weather_id != 800 and weather.weather_id // 100 == 8 else False
    res['weather_drizzle'] = True if weather.weather_id // 100 == 3 else False
    res['weather_fog'] = True if weather.weather_id  == 741 else False
    res['weather_mist'] = True if weather.weather_id // 100 == 7 and weather.weather_id != 741 else False
    res['weather_rain'] = True if weather.weather_id // 100 == 5 else False
    res['weather_snow'] = True if weather.weather_id // 100 == 6 else False

    return res