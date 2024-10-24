from fastapi import APIRouter, HTTPException
from typing import List
import httpx, os, json

from app.api.models import GroupOut, GroupIn, GroupUpdate, StudentIn, StudentOut
from app.api import db_manager

DATABASE_URI = os.getenv('DATABASE_URI')
STUDENT_SERVICE_URL = os.getenv('STUDENT_SERVICE_URL')

router = APIRouter()

@router.post('/', response_model=GroupOut, status_code=201)
async def create_group(payload: GroupIn):
    group_id = await db_manager.add_group(payload)
    response = {
        'id': group_id,
        'students': []
    }
    return GroupOut(**response)

@router.get('/', response_model=List[GroupOut])
async def get_groups():
    return await db_manager.get_all_groups()

@router.get('/{id}/', response_model=GroupOut)
async def get_group(id: int):
    group = await db_manager.get_group(id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    # Get students list
    students = await db_manager.get_students_in_group(id)
    group_with_students = {
        'id': group['id'],
        'students': students
    }
    return GroupOut(**group_with_students)

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

@router.post('/create', response_model=StudentOut, status_code=201)
async def create_group_for_student(payload: StudentIn):
    group_id = await db_manager.add_group(GroupIn(payload.group_id))
    response = {
        'id': group_id,
        'students': []
    }
    return GroupOut(**response)

@router.put('/{id}/student/{student_id}', response_model=None)
async def add_student_to_group(id: int, student_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{STUDENT_SERVICE_URL}/{student_id}/group/{id}")
        if response.status_code != 200:
            try:
                error_detail = response.json().get("detail", "Error")
            except json.JSONDecodeError:
                error_detail = "Invalid response from student service"
            raise HTTPException(status_code=response.status_code, detail=error_detail)
    return None

@router.delete('/{id}/student/{student_id}', response_model=None)
async def delete_student_from_group(id: int, student_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{STUDENT_SERVICE_URL}/{student_id}/group/remove")
        if response.status_code != 200:
            try:
                error_detail = response.json().get("detail", "Error")
            except json.JSONDecodeError:
                error_detail = "Invalid response from student service"
            raise HTTPException(status_code=response.status_code, detail=error_detail)
    return None