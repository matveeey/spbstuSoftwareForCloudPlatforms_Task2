from pydantic import BaseModel
from typing import Optional

class StudentIn(BaseModel):
    name: str
    group_id: Optional[int] = None

class StudentOut(StudentIn):
    id: int

class StudentUpdate(StudentIn):
    name: Optional[str] = None
    group_id: Optional[int] = None