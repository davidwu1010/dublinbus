import sys
from math import sqrt, radians, cos, sin, asin

from fastapi import APIRouter

from app.routers.deps import (
    get_stops_by_route,
    get_section,
    get_stops,
    get_coor,
)


stops_by_route = get_stops_by_route()
coor_json = get_stops()
coordinate_json = get_coor()


router = APIRouter()


@router.get(
    '/{route_id}',
    tags=['stops'],
    summary='Return all the stops of a route',
    description='Given a route_id return all the stops of this route'
)
async def read_stops(route_id: str):
    if route_id in stops_by_route:
        return stops_by_route[route_id]
    else:
        return {'error': 'Not Found'}


@router.get(
    '/',
    tags=['stops'],
    summary='Return all the stops between the origin and the destination',
    description='Given an origin and destination stop,'
                'return all the stops (including the origin and destination) '
                'between the two stops.'
                'Each stop should include the stopNumber,'
                'longitude and latitude of the stop'
)
async def read_stops_between_origin_dest(route_id: str, origin: int, dest: int):
    """
    @retuen {'stops': [
        {'stopNumber': 1, 'lon': 11, 'lat': 12},
        {'stopNumber': 2, 'lon': 12, 'lat': 14},
        {'stopNumber': 3, 'lon': 12, 'lat': 24},
    ]}

    """
    res = {'stops': []}
    
    for k, v in stops_by_route.items():
        outbound = v['outbound']
        inbound = v['inbound']
        section_lst = get_section(outbound, origin, dest)
        if not section_lst:
            section_lst = get_section(inbound, origin, dest)
        if section_lst:
            break
    section_lst = get_coord(section_lst)
    res['stops'].extend(section_lst)
    return res


@router.get(
    '/nearest/',
    tags=['stops'],
    summary='Return nearest the stops',
    description='give a coord return nearest stops'
)
async def get_nearest_stops(lat: float, lon: float, route_id: str):
    res = {
        'stop_id': 0,
    }
    min_distance = sys.maxsize
    for stop_id, stop in coordinate_json[route_id].items():
        distance = geodistance(lat, lon, stop['lat'], stop['lon'])
        if distance < min_distance:
            min_distance = distance
            res['stop_id'] = stop_id
    return res


def get_coord(section_lst):
    for stop in section_lst:
        stop_number = stop['stopNumber']
        stop.update({
            'lon': coor_json[str(stop_number)]['lon'],
            'lat': coor_json[str(stop_number)]['lat'],
        })
    return section_lst


def geodistance(lng1, lat1, lng2, lat2):
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    dlon = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    dis = 2 * asin(sqrt(a)) * 6371 * 1000
    return dis
