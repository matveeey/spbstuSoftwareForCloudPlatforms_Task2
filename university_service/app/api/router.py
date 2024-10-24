from fastapi import APIRouter, HTTPException
from typing import List
import httpx
import os

from app.api.models import StudentIn, StudentOut, GroupOut, GroupIn, GroupUpdate

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
@router.post('/groups', response_model=GroupOut, status_code=201)
async def create_group(payload: GroupIn):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{GROUP_SERVICE_URL}/", json=payload.dict())
        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Error"))
        return response.json()

@router.get('/groups', response_model=List[GroupOut])
async def get_groups():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{GROUP_SERVICE_URL}/")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Error"))
        return response.json()

@router.get('/groups/{id}', response_model=GroupOut)
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
        # Check if group exists
        # Get all groups
        groups_response = await client.get(f"{GROUP_SERVICE_URL}/")
        if groups_response.status_code != 200:
            raise HTTPException(status_code=groups_response.status_code, detail=groups_response.text)
        groups = groups_response.json()

        # Check if the group exists
        group_exists = any(group['id'] == group_id for group in groups)

        # Create group if it doesn't exist
        if not group_exists:
            create_group_payload = GroupIn(id=group_id, students=[student_id])
            create_group_response = await create_group(create_group_payload)
        else:
            get_group_response = await get_group(group_id)
            students = get_group_response["students"]
            students.append(student_id)

            # Update group
            update_group_payload = GroupUpdate(id=group_id, students=students)
            update_group_response = await client.put(f"{GROUP_SERVICE_URL}/{group_id}/", json=update_group_payload.dict())
            if update_group_response.status_code != 200:
                raise HTTPException(status_code=update_group_response.status_code, detail=update_group_response.text)
            
        # Update student
        student_response = await get_student(student_id)
        student_name = student_response["name"]
        update_student_payload = StudentIn(name=student_name, group_id=group_id)
        update_student_response = await client.put(f"{STUDENT_SERVICE_URL}/{group_id}/", json=update_student_payload.dict())
        # if update_student_response.status_code != 200:
        #     raise HTTPException(status_code=update_student_response.status_code, detail=update_student_response.text)

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
        # Get the current group
        group_response = await client.get(f"{GROUP_SERVICE_URL}/{new_group_id}/")
        if group_response.status_code != 200:
            raise HTTPException(status_code=group_response.status_code, detail=group_response.json().get("detail", "Error"))
        
        group = group_response.json()
        students = group.get("students", [])

        # Add student to the group if not already present
        if student_id not in students:
            students.append(student_id)

        # Update the group with the new students list
        update_group_payload = GroupUpdate(id=new_group_id, students=students)
        update_group_response = await client.put(f"{GROUP_SERVICE_URL}/{new_group_id}/", json=update_group_payload.dict())
        if update_group_response.status_code != 200:
            raise HTTPException(status_code=update_group_response.status_code, detail=update_group_response.json().get("detail", "Error"))

        return None