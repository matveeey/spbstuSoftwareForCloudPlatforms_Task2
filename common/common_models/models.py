from pydantic import BaseModel
from typing import List, Optional

class StudentIn(BaseModel):
    name: str
    group_id: Optional[int] = None

class StudentOut(StudentIn):
    id: int

class GroupIn(BaseModel):
    id: int
    students: List[int]

class GroupOut(GroupIn):
    pass

class GroupUpdate(GroupIn):
    students: Optional[List[int]] = None