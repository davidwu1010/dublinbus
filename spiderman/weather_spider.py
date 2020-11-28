import sys
import time
import requests
# from datetime import datetime

import depend_module
import config
from db.mysql import Mysql
from util.mylog import Logger
from util.myerror import MyError

 
class WeatherCrawler:
    
    LOG_NAME = 'wCrawler'

    def __init__(self, config):
        self.db = config['db']
        self.url = config['url']
        self.tb_name = config['tb_name']
        self.log = Logger(WeatherCrawler.LOG_NAME)

    def worker(self):
        self.log.info('Start...')
        weather_json = self._request_ow_api()

        for data in weather_json['hourly']:
            value_dic = self._parse_json(data)
            self._insert_weather_data(value_dic)
        
        for data in weather_json['daily']:
            value_dic = self._parse_daily_json(data)
            self._insert_weather_data(value_dic)
        
        cur_value_dict = self._parse_json(weather_json['current'])
        cur_value_dict = self._updatedt(cur_value_dict)
        self._insert_weather_data(cur_value_dict)
        
        self.log.info('Done!')
    
    def _updatedt(self, value_dict):
        dt = value_dict['dt']
        value_dict['dt'] = (dt // 100) * 100
        return value_dict

    def _request_ow_api(self):
        try:
            r = requests.get(self.url)
        
            if r.status_code != 200 or r.json() == None:
                e = "request ow api failed: {}".format(r.status_code)
                self.log.warn(e)
                raise MyError(e)
            
            ret = r.json()
            self.log.info("response 200 OK: {}".format(ret))
            return ret
        except Exception as e:
            error = "request - {}: {}".format(self.url, e)
            self.log.error(error)
            raise MyError(error)

    def _parse_json(self, data):
        try: 
            ret = {
                'dt': data.get('dt'),
                'temp': data.get('temp'),
                'temp_min': data.get('temp'),
                'temp_max': data.get('temp'),
                'feels_like': data.get('feels_like'),
                'pressure': data.get('pressure'),
                'humidity': data.get('humidity'),
                'wind_speed': data.get('wind_speed'),
                'wind_deg': data.get('wind_deg'),
                'clouds': data.get("clouds"),
                'weather_id': data.get("weather")[0].get("id"),
                'weather_main': data.get("weather")[0].get("main"),
                'weather_desc': data.get("weather")[0].get("description"),
            }
            return ret
        except Exception as e:
            error = "parse_json - {}: {}".format(data, e)
            self.log.error(error)
            raise MyError(error)
    
    def _parse_daily_json(self, data):
        try: 
            ret = {
                'dt': data.get('dt'),
                'temp': data.get('temp').get('day'),
                'temp_min': data.get('temp').get('min'),
                'temp_max': data.get('temp').get('max'),
                'feels_like': data.get('feels_like').get('day'),
                'pressure': data.get('pressure'),
                'humidity': data.get('humidity'),
                'wind_speed': data.get('wind_speed'),
                'wind_deg': data.get('wind_deg'),
                'clouds': data.get("clouds"),
                'weather_id': data.get("weather")[0].get("id"),
                'weather_main': data.get("weather")[0].get("main"),
                'weather_desc': data.get("weather")[0].get("description"),
            }
            return ret
        except Exception as e:
            error = "parse_daily_json - {}: {}".format(data, e)
            self.log.error(error)
            raise MyError(error)

    def _insert_weather_data(self, value_dict):
        keys = list(value_dict.keys())
        values = list(value_dict.values())
        sql = '''INSERT INTO %s (%s) VALUES (%s) ON DUPLICATE KEY UPDATE %s''' % (
                self.tb_name,
                ",".join(keys),
                ",".join(['%s'] * len(keys)),
                (",").join(['%s=%%s' % k for k in keys]))
        para = values * 2
        ret = self.db.execute(sql, para)
        if not ret:
            self.log.error('insert weather failed: {}'.format(value_dict))
        

def get_conf():
    if len(sys.argv) != 2:
        return config.ProductionConfig
    env = sys.argv[1]
    if env == 'production':
        return config.ProductionConfig
    elif env == 'test':
        return config.TestingConfig 


if __name__ == "__main__":
    conf = get_conf()
    db = Mysql(conf.DB_HOST, 
        conf.DB_PORT, 
        conf.DB_USER,
        conf.DB_PWD,
        conf.DB_NAME)
    config = {
        'db': db,
        'url': conf.OW_URL,
        'tb_name': conf.TB_NAME,
        }
    crawler = WeatherCrawler(config)
    crawler.worker()