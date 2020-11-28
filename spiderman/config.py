import os

from dotenv import load_dotenv
load_dotenv()


class Config:
    OW_URL = os.getenv("OW_URL")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT"))
    DB_USER = os.getenv("DB_USER")
    DB_PWD = os.getenv("DB_PWD")
    TB_NAME = os.getenv("TB_WEATHER_NAME")
 

class ProductionConfig(Config):
	DB_NAME = os.getenv("DB_NAME_PRODUCT")

 
class TestingConfig(Config):
    DB_NAME = os.getenv("DB_NAME_TEST")