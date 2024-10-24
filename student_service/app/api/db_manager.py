from app.api.models import StudentIn, StudentOut
from app.api.db import students, database

async def add_student(payload: StudentIn):
    query = students.insert().values(**payload.dict())
    return await database.execute(query=query)

async def get_all_students():
    query = students.select()
    return await database.fetch_all(query=query)

async def get_student(id):
    query = students.select().where(students.c.id == id)
    return await database.fetch_one(query=query)

async def delete_student(id: int):
    query = students.delete().where(students.c.id == id)
    return await database.execute(query=query)

async def update_student(id: int, payload: StudentIn):
    query = (
        students
        .update()
        .where(students.c.id == id)
        .values(**payload.dict())
    )
    await database.execute(query=query)
    return await get_student(id)

async def add_student_to_group(student_id: int, group_id: int):
    query = (
        students
        .update()
        .where(students.c.id == student_id)
        .values(group_id=group_id)
    )
    await database.execute(query=query)
    return await get_student(student_id)

async def delete_student_from_group(student_id: int):
    query = (
        students
        .update()
        .where(students.c.id == student_id)
        .values(group_id=None)
    )
    await database.execute(query=query)
    return await get_student(student_id)