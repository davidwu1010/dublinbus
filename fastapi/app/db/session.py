from redis import StrictRedis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.config import setting


engine = create_engine(setting.SQLALCHEMY_DATABASE_URI)
Base = declarative_base(engine)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
connection = engine.connect()

RedisClient = StrictRedis(host=setting.REDIS_HOST, decode_responses=True)