from sqlalchemy import Column, Integer, String

from app.db.session import Base


class UserRoute(Base):
    __tablename__ = 'user_route'
    __table_args__ = {'autoload': True}
