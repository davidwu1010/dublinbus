import sys
import time
import requests
from datetime import datetime

import depend_module
import config
from db.mysql import Mysql
from util.mylog import Logger
from util.myerror import MyError


class DataLoader:

    LOG_NAME = 'sectionLoader'
    TS_20180101 = 1514764800
    STATUS_PROCESSING = 2
    STATUS_SUCCESS = 1
    STATUS_ERROR = 3
    
    def __init__(self, config):
        self.db = config['db']
        
        self.tb_JanLT = config['tb_JanLT']
        self.tb_section = config['tb_section']
        self.tb_trip = config['tb_trip']
        self.tb_vehicle = config['tb_vehicle']
        self.tb_status = config['tb_status']

        self.data = []
        self.trip_lst = []
        self.trip_info = {}

        self.log = Logger(DataLoader.LOG_NAME)

    def do_work(self):
        activate = True
        if not self._is_activate():
            self.log.info("DONE!")
            activate = False
        while activate:
            self._tp_workflow()

    def _tp_workflow(self):
        try:
            self._reset()
            target = self._get_day_and_tid()
            self._update_status(target, DataLoader.STATUS_PROCESSING)
            self.trip_lst = self._get_trip(target)
            self.trip_info = self._get_trip_info(target)
            self._sort_lst()
            self._parse_trip_lst()
            res = self._insert_data(self.data)
            stauts_code = DataLoader.STATUS_SUCCESS if res else DataLoader.STATUS_ERROR
            self._update_status(target, stauts_code)
        except Exception as e:
            self.log.error(e)
            self._update_status(target, DataLoader.STATUS_ERROR)
    
    def _reset(self):
        self.trip_lst = []
        self.data = []
        self.trip_info = {}

    def _update_status(self, ret, stauts_code):
        sql = '''UPDATE %s
            SET status = %s
            WHERE DayOfService=%s and tripid=%s''' % (
                self.tb_status,
                stauts_code,
                ret['DayOfService'],
                ret['TripID'],
            )
        ret = self.db.execute(sql)
        if not ret:
            e = 'update status failed: {}'.format(sql)
            self.log.error(e)
            raise MyError(e)
    
    def _sort_lst(self):
        is_reverse = False if self.trip_info['Direction'] == 1 else True
        sorted(self.trip_lst, key=lambda x: x['ProgrNumber'], reverse=is_reverse)

    def _parse_trip_lst(self):
        try:
            last_dep_time = self.trip_info['ActualTime_Dep']
            last_stopid = 0
            for stop in self.trip_lst:
                """{'DayOfService': datetime.date(2018, 1, 6), 
                'TripID': 5955221, 
                'ProgrNumber': 1, 
                'StopPointID': 248, 
                'PlannedTime_Arr': 37800, 
                'ActualTime_Arr': 37836, 
                'ActualTime_Dep': 37836, 
                'VehicleID': 2693254};
                {'LineID': '14', 
                'Direction': 1, 
                'ActualTime_Dep': 37836, 
                'RouteID': '14_15',}
                """
                day_timestamp = int(stop['DayOfService'].strftime("%s"))
                weatherdt = self._get_weatherdt(day_timestamp+last_dep_time)
                section = [
                    stop['TripID'],
                    day_timestamp,
                    last_stopid,
                    stop['StopPointID'],
                    self.trip_info['LineID'],
                    self.trip_info['RouteID'],
                    stop['VehicleID'],
                    stop['ActualTime_Arr'] - last_dep_time,
                    last_dep_time + day_timestamp,
                    weatherdt,
                ]
                self.data.append(section)
                last_stopid = stop['StopPointID']
                last_dep_time = stop['ActualTime_Dep']
        except Exception as e:
            raise MyError(e)
    
    def _get_weatherdt(self, timestamp):
        ts = timestamp - DataLoader.TS_20180101
        quo = ts // 3600
        res = ts % 3600
        quo = quo + 1 if res > 1800 else 0
        return quo * 3600 + DataLoader.TS_20180101
        
    def _get_trip_info(self, value_dict):
        sql = """SELECT LineID, Direction, ActualTime_Dep, RouteID
                 FROM %s
                 WHERE DayOfService=FROM_UNIXTIME(%s)
                 AND TripID=%s""" % (
                    self.tb_trip,
                    value_dict['DayOfService'],
                    value_dict['TripID'],)
        ret = self.db.query_one(sql)
        if not ret:
            e = 'get trip info failed: {}'.format(sql)
            self.log.error(e)
            raise MyError(e)
        self.log.info('get trip info: {}'.format(value_dict))
        return ret

    def _is_activate(self):
        sql = """SELECT EXISTS (SELECT * FROM %s WHERE status = 0) as is_activate
        """ % (self.tb_status)
        return self.db.query_one(sql)['is_activate']
    
    def _get_day_and_tid(self):
        sql = """
            SELECT DayOfService as DayOfService, TripID 
            FROM %s
            WHERE status=0
            LIMIT 1;
        """ % self.tb_status
        ret = self.db.query_one(sql)
        if not ret:
            e = 'get day and tripid failed: {}',format(sql)
            self.log.error(e)
            raise Exception(e)
        self.log.info("get day and tripID: {}".format(ret))
        return ret
            
    
    def _get_trip(self, value_dict):
        sql = """
            SELECT * 
            FROM %s
            WHERE DayOfService=FROM_UNIXTIME(%s)
            AND TripID=%s""" % (
                self.tb_JanLT,
                value_dict['DayOfService'],
                value_dict['TripID'],)
        ret = self.db.query(sql)
        if not ret:
            e = 'get trip_list failed: {}'.format(value_dict)
            self.log.error(e)
            raise Exception(e)
        return ret
    
    def _insert_data(self, value_lst):
        sql = """INSERT INTO {}
                (tripid, DayOfService, firststopid, secondstopid, 
                lineid, routeID, vehicleid, traveltime, time, weatherdt)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(self.tb_section)
        return self.db.executemany(sql, value_lst)


if __name__ == "__main__":
    conf = config.Config
    db = Mysql(conf.DB_HOST, 
        conf.DB_PORT, 
        conf.DB_USER,
        conf.DB_PWD,
        conf.DB_NAME)
    config = {
        'db': db,
        'tb_JanLT': conf.TB_JanLT,
        'tb_section': conf.TB_SECTION,
        'tb_trip': conf.TB_TRIP,
        'tb_vehicle': conf.TB_VEHICLE,
        'tb_status': conf.TB_STATUS,
        }
    loader = DataLoader(config)
    loader.do_work()