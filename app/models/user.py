from typing import Optional, List

from models.base import BaseModel


class User(BaseModel):
    telephone: Optional[str] = ""
    avatar: Optional[str] = ""
    department_id: List[str] = []
    role_ids: List[str] = []
