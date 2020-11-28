import os

from dotenv import load_dotenv
load_dotenv()


class Config:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT"))
    DB_USER = os.getenv("DB_USER")
    DB_PWD = os.getenv("DB_PWD")
    
    DB_NAME = os.getenv("DB_NAME")

    TB_SECTION = os.getenv("TB_SECTION")
    TB_TRIP = os.getenv("TB_TRIPS")
    TB_VEHICLE = os.getenv("TB_VEHICLE")
    TB_JanLT = os.getenv("TB_JanLT")
    TB_STATUS = os.getenv("TB_STATUS")
 

# class RdsConfig(Config):
# 	DB_NAME = os.getenv("DB_NAME_PRODUCT")

 
# class WDConfig(Config):
#     DB_NAME = os.getenv("DB_NAME_TEST")