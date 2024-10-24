import os
from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine)
from databases import Database

DATABASE_URI = 'postgresql://student_db_username:student_db_password@db/student_db_dev'

engine = create_engine(DATABASE_URI)
metadata = MetaData()

students = Table(
    'students',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('group_id', Integer)
)

database = Database(DATABASE_URI)