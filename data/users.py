import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    chat_id = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    wiki_requests = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    maps_requests = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    articles = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    # translits_requests = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    overall_rating = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)

