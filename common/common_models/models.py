from pydantic import BaseModel
from typing import List, Optional

class StudentIn(BaseModel):
    name: str
    group_id: Optional[int] = None

class StudentOut(StudentIn):
    id: int

class Group(BaseModel):
    id: int
    students: Optional[List[int]]
