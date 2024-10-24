from app.api.models import GroupIn, GroupOut, GroupUpdate
from app.api.db import groups, database

async def add_group(payload: GroupIn):
    query = groups.insert().values(**payload.dict()).returning(groups.c.id)
    return await database.execute(query=query)

async def get_all_groups():
    query = groups.select()
    return await database.fetch_all(query=query)

async def get_group(id):
    query = groups.select().where(groups.c.id == id)
    return await database.fetch_one(query=query)

async def delete_group(id: int):
    query = groups.delete().where(groups.c.id == id)
    return await database.execute(query=query)

async def update_group(id: int, payload: GroupIn):
    query = (
        groups
        .update()
        .where(groups.c.id == id)
        .values(**payload.dict())
    )
    return await database.execute(query=query)