from sqlalchemy import create_engine
from model import Base


def create_all(engine):
    Base.metadata.create_all(engine)
