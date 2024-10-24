from pydantic import BaseModel
from typing import Optional

class GroupIn(BaseModel):
    name: str

class GroupOut(GroupIn):
    id: int

class GroupUpdate(GroupIn):
    name: Optional[str] = None