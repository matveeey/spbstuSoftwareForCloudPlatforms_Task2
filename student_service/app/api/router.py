from fastapi import APIRouter, HTTPException
from typing import List
import httpx, os

from app.api.models import StudentOut, StudentIn
from app.api import db_manager

router = APIRouter()

GROUP_SERVICE_URL = os.getenv('GROUP_SERVICE_URL')

@router.post('/', response_model=StudentOut, status_code=201)
async def create_student(payload: StudentIn):
    student_id = await db_manager.add_student(payload)
    response = {
        'id': student_id,
        **payload.dict()
    }

    # If there is group_id, add student to the group
    if payload.group_id:
        async with httpx.AsyncClient() as client:
            # Check if group exists
            group_response = await client.get(f"{GROUP_SERVICE_URL}/{payload.group_id}")
            if group_response.status_code == 404:
                # Create group if it doesn't exist
                create_group_response = await client.post(f"{GROUP_SERVICE_URL}/create", json=payload.dict())
                if create_group_response.status_code != 201:
                    raise HTTPException(status_code=500, detail="Failed to create group")
                payload.group_id = create_group_response.json()['id']

            await client.put(f"{GROUP_SERVICE_URL}/{payload.group_id}/student/{student_id}")

    return StudentOut(**response)

@router.get('/', response_model=List[StudentOut])
async def get_students():
    return await db_manager.get_all_students()

@router.get('/{id}/', response_model=StudentOut)
async def get_student(id: int):
    student = await db_manager.get_student(id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.put('/{id}/', response_model=StudentOut)
async def update_student(id: int, payload: StudentIn):
    student = await db_manager.get_student(id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    update_data = payload.dict(exclude_unset=True)
    student_in_db = StudentIn(**student)
    updated_student = student_in_db.copy(update=update_data)

    return await db_manager.update_student(id, updated_student)

@router.delete('/{id}', response_model=None)
async def delete_student(id: int):
    student = await db_manager.get_student(id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return await db_manager.delete_student(id)

@router.put('/{id}/group/{group_id}', response_model=StudentOut)
async def add_student_to_group(id: int, group_id: int):
    student = await db_manager.get_student(id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student_in_db = StudentIn(**student)
    updated_student = student_in_db.copy(update={'group_id': group_id})

    updated_student_db = await db_manager.update_student(id, updated_student)
    return StudentOut(**updated_student_db)

@router.delete('/{id}/group/remove', response_model=StudentOut)
async def delete_student_from_group(id: int):
    student = await db_manager.get_student(id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student_in_db = StudentIn(**student)
    updated_student = student_in_db.copy(update={'group_id': None})

    updated_student_db = await db_manager.update_student(id, updated_student)
    return StudentOut(**updated_student_db)