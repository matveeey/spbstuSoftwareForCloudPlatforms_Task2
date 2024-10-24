from fastapi import APIRouter, HTTPException
from typing import List
import httpx
import os

from app.api.models import StudentIn, StudentOut, Group

router = APIRouter()

STUDENT_SERVICE_URL = os.getenv('STUDENT_SERVICE_URL')
GROUP_SERVICE_URL = os.getenv('GROUP_SERVICE_URL')

# Students
@router.post('/students', response_model=StudentOut, status_code=201)
async def create_student(payload: StudentIn):
    async with httpx.AsyncClient() as client:
        # Create student
        response = await client.post(f"{STUDENT_SERVICE_URL}/", json=payload.dict())
        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        student_id = response.json()['id']
        student = StudentOut(id=student_id, name=payload.name, group_id=payload.group_id)

        # Check if group exists
        if payload.group_id:
            # Get all groups
            groups_response = await client.get(f"{GROUP_SERVICE_URL}/")
            if groups_response.status_code != 200:
                raise HTTPException(status_code=groups_response.status_code, detail=groups_response.text)
            groups = groups_response.json()

            # Check if the group exists
            group_exists = any(group['id'] == payload.group_id for group in groups)

            # Create group if it doesn't exist
            if not group_exists:
                create_group_payload = Group(id=payload.group_id, students=[student])
                create_group_response = await create_group(create_group_payload)
                if create_group_response.status_code != 201:
                    raise HTTPException(status_code=500, detail=create_group_response.text)
            else:
                get_group_response = await get_group(payload.group_id)
                students = get_group_response.json()["students"]
                students.append(student)
                update_group_payload = Group(id=payload.group_id, students=students)
                update_group_response = await client.put(f"{GROUP_SERVICE_URL}/{payload.group_id}/", json=update_group_payload)
                if update_group_response.status_code != 200:
                    raise HTTPException(status_code=update_group_response.status_code, detail=update_group_response.text)

        return response.json()

@router.get('/students', response_model=List[StudentOut])
async def get_students():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{STUDENT_SERVICE_URL}/")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Error"))
        return response.json()

@router.get('/students/{id}', response_model=StudentOut)
async def get_student(id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{STUDENT_SERVICE_URL}/{id}/")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Error"))
        return response.json()

@router.delete('/students/{id}', response_model=None)
async def delete_student(id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{STUDENT_SERVICE_URL}/{id}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Error"))
        return None

# Groups
@router.post('/groups', response_model=Group, status_code=201)
async def create_group(payload: Group):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{GROUP_SERVICE_URL}/", json=payload.dict())
        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Error"))
        return response.json()

@router.get('/groups', response_model=List[Group])
async def get_groups():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{GROUP_SERVICE_URL}/")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Error"))
        return response.json()

@router.get('/groups/{id}', response_model=Group)
async def get_group(id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{GROUP_SERVICE_URL}/{id}/")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Error"))
        return response.json()

@router.delete('/groups/{id}', response_model=None)
async def delete_group(id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{GROUP_SERVICE_URL}/{id}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Error"))
        return None

# Add/Remove Student from Group
@router.put('/students/{student_id}/group/{group_id}', response_model=None)
async def add_student_to_group(student_id: int, group_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{STUDENT_SERVICE_URL}/{student_id}/group/{group_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Error"))
        return None

@router.delete('/students/{student_id}/group', response_model=None)
async def remove_student_from_group(student_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{STUDENT_SERVICE_URL}/{student_id}/group/remove")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Error"))
        return None

# Transfer Student from Group A to Group B
@router.put('/students/{student_id}/transfer/{new_group_id}', response_model=None)
async def transfer_student(student_id: int, new_group_id: int):
    async with httpx.AsyncClient() as client:
        # Remove student from current group
        await client.delete(f"{STUDENT_SERVICE_URL}/{student_id}/group/remove")
        # Add student to new group
        response = await client.put(f"{STUDENT_SERVICE_URL}/{student_id}/group/{new_group_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Error"))
        return None