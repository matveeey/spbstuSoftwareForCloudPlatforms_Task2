from fastapi import APIRouter, HTTPException
from typing import List

from app.api.models import GroupOut, GroupIn, GroupUpdate
from app.api import db_manager

router = APIRouter()

@router.post('/', response_model=GroupOut, status_code=201)
async def create_group(payload: GroupIn):
    group_id = await db_manager.add_group(payload)
    response = {
        'id': group_id,
        **payload.dict()
    }
    return response

@router.get('/', response_model=List[GroupOut])
async def get_groups():
    return await db_manager.get_all_groups()

@router.get('/{id}/', response_model=GroupOut)
async def get_group(id: int):
    group = await db_manager.get_group(id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@router.put('/{id}/', response_model=GroupOut)
async def update_group(id: int, payload: GroupUpdate):
    group = await db_manager.get_group(id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    update_data = payload.dict(exclude_unset=True)
    group_in_db = GroupIn(**group)
    updated_group = group_in_db.copy(update=update_data)

    return await db_manager.update_group(id, updated_group)

@router.delete('/{id}', response_model=None)
async def delete_group(id: int):
    group = await db_manager.get_group(id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return await db_manager.delete_group(id)