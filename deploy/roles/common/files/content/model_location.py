import datetime
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
BASE = os.path.dirname(os.path.dirname(__file__))
Base = declarative_base()

DATABASE_PATH = os.path.dirname(__file__) + "/location_vp.db"


class Location(Base):
    __tablename__ = 'location'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    ssid = Column(String(250), nullable=False)
    data = Column(Text(), nullable=False)
    created = Column(DateTime, default=datetime.datetime.now)






# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:////' + DATABASE_PATH)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)