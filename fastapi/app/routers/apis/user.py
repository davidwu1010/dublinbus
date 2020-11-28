from fastapi import APIRouter, Request

from app.db import crud
from app.model.Items import UserRoutePostItem
from app.routers.deps import (
    get_uid,
    get_coor,
)


stops_json = get_coor()
router = APIRouter()



@router.get(
    '/',
    tags=['user'],
    summary='query user\'s  saves routes',
)
async def get_routes(request: Request):
    token = request.headers['Authorization'].split(' ')[1]
    uid = 'YkgAsiFI31aizOaE4BL0wDoTMGU2' if token == 'TEST' else get_uid(token)
    if not uid:
        return {'status': 'wrong token'}
    query_lst = crud.get_route(uid)
    return parse_res(query_lst)


@router.post(
    '/',
    tags=['user'],
    summary='save routes',
)
async def save_routes(request: Request, request_data: UserRoutePostItem):
    # { "route_id": "39","origin": "783", "dest": "786"}
    token = request.headers['Authorization'].split(' ')[1]
    uid = 'YkgAsiFI31aizOaE4BL0wDoTMGU2' if token == 'TEST' else get_uid(token)
    if not uid:
        return {'status': 'wrong token'}
    route_id = request_data.route_id
    ori_sid = request_data.origin
    dest_sid = request_data.dest
    route_info = stops_json.get(route_id, {})
    data = {
        'uid': uid,
        'route_id': route_id,
        'ori_sid': ori_sid,
        'dest_sid': dest_sid,
        'ori_address': route_info.get(ori_sid, {}).get('address', ''),
        'dest_address': route_info.get(dest_sid, {}).get('address', ''),
        'ori_location': route_info.get(ori_sid, {}).get('location', ''),
        'dest_location': route_info.get(dest_sid, {}).get('location', ''),
    }
    res = crud.insert_route(data)
    if res:
        return {'code': 200}
    else:
        return {'code': 500}


@router.delete(
    '/',
    tags=['user'],
    summary='delete routes',
)
async def rm_routes(
    request: Request,
    route_id: str,
    origin: int,
    dest: int
):
    token = request.headers['Authorization'].split(' ')[1]
    uid = 'YkgAsiFI31aizOaE4BL0wDoTMGU2' if token == 'TEST' else get_uid(token)
    if not uid:
        return {'status': 'wrong token'}
    res = crud.rm_route(uid, route_id, origin, dest)
    if res:
        return {'code': 200}
    else:
        return {'code': 500}


def parse_res(res):
    r = {'routes': []}
    for i in res:
        d = {
            'routeId': i.route_id,
            'origin': {
                'stopNumber': i.ori_sid,
                'address': i.ori_address,
                'location': i.ori_location,
            },
            'dest': {
                'stopNumber': i.dest_sid,
                'address': i.dest_address,
                'location': i.dest_location,
            },
        }
        r['routes'].append(d)
    return r
