import os
from sqlalchemy import (Column, Integer, ARRAY, MetaData, Table, create_engine)
from databases import Database

DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI)
metadata = MetaData()

groups = Table(
    'groups',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('students', ARRAY(Integer))
)

database = Database(DATABASE_URI)