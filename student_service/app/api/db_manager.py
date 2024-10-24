from app.api.models import StudentIn, StudentOut, StudentUpdate
from app.api.db import students, database

async def add_student(payload: StudentIn):
    query = students.insert().values(**payload.dict())
    return await database.execute(query=query)

async def get_all_students():
    query = students.select()
    return await database.fetch_all(query=query)

async def get_student(id):
    query = students.select(students.c.id==id)
    return await database.fetch_one(query=query)

async def delete_student(id: int):
    query = students.delete().where(students.c.id==id)
    return await database.execute(query=query)

async def update_student(id: int, payload: StudentIn):
    query = (
        students
        .update()
        .where(students.c.id == id)
        .values(**payload.dict())
    )
    return await database.execute(query=query)