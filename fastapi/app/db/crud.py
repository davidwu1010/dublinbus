from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.db.session import connection
from app.model.weather import Weather
from app.model.user_route import UserRoute



def get_weather(timestamp: int):
    return Session().query(Weather).filter(Weather.dt==timestamp).first()


def insert_route(data: dict):
    raw_sql = """insert into user_route
            (uid, route_id, ori_sid, dest_sid, ori_address, 
            dest_address, ori_location, dest_location) 
            values 
            ("{uid}","{route_id}",{ori_sid},{dest_sid},"{ori_address}",
            "{dest_address}","{ori_location}","{dest_location}")""".format(**data)
    result = connection.execute(text(raw_sql).execution_options(autocommit=True))
    return result


def get_route(uid: int):
    return Session().query(UserRoute).filter_by(uid=uid).all()


def rm_route(
    uid: int,
    route_id: str,
    osid: int,
    dsid: int):
    raw_sql = """delete from user_route where 
            uid="{}" and 
            route_id="{}" and
            ori_sid={} and 
            dest_sid={}
    """.format(uid, route_id, osid, dsid)
    result = connection.execute(text(raw_sql).execution_options(autocommit=True))
    return result
