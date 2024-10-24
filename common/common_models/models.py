from pydantic import BaseModel
from typing import List, Optional

class StudentIn(BaseModel):
    name: str
    group_id: Optional[int] = None

class StudentOut(StudentIn):
    id: int

class StudentUpdate(StudentIn):
    name: Optional[str] = None
    group_id: Optional[int] = None

class GroupIn(BaseModel):
    name: str

class GroupOut(GroupIn):
    id: int

class GroupUpdate(BaseModel):
    name: Optional[str] = None