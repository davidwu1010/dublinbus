from app.db.session import Base


class Weather(Base):
    __tablename__ = 'cur_weather'
    __table_args__ = {'autoload': True}