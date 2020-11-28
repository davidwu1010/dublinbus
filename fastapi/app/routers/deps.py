import json
import xgboost
from pathlib import Path
from redis_cache import RedisCache
import firebase_admin
from firebase_admin import auth

from app.db.session import SessionLocal, RedisClient


base_path = Path(__file__).parent

stops_by_route_path = (base_path / '../data/stops_by_route.json').resolve()
stops_path = (base_path / '../data/stops.json').resolve()
routes_path = (base_path / '../data/routes.json').resolve()
distance_path = (base_path / '../data/stops_with_distance.json').resolve()
coor_path = (base_path / '../data/coor.json').resolve()



# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_stops_by_route() -> dict:
    with open(stops_by_route_path, 'r') as f:
        stops_by_route_dict = json.load(f)
    return stops_by_route_dict['routes']


def get_stops() -> dict:
    with open(stops_path, 'r') as f:
        stops_dict = json.load(f)
    return stops_dict


def get_routes() -> dict:
    with open(routes_path, 'r') as f:
        routes_dict = json.load(f)
    return routes_dict


def get_distance_dict() -> dict:
    with open(distance_path, 'r') as f:
        distance_dic = json.load(f)
    return distance_dic


def get_section(stops_lst: list, origin: int, dest: int):
    is_append = False
    target_lst = []
    for stop in stops_lst:
        if int(stop['stopNumber']) == origin:
            is_append = True
        if is_append:
            target_lst.append({'stopNumber': int(stop['stopNumber'])})
        if is_append and int(stop['stopNumber']) == dest:
            return target_lst
    target_lst.clear()
    return []


# Dependency
def get_booster(month):
    bst = xgboost.Booster()
    model_path = (base_path / f'../models/General_{month}.model').resolve()
    bst.load_model(model_path)
    return bst


def get_coor() -> dict:
    with open(coor_path, 'r') as f:
        dict = json.load(f)
    return dict


cache = RedisCache(redis_client=RedisClient)


def get_uid(token):
    if not firebase_admin._apps:
        firebase_admin.initialize_app()
    decoded_token = firebase_admin.auth.verify_id_token(token)
    return decoded_token['uid']
