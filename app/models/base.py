from typing import Optional

from pydantic import BaseModel as PydanticBaseModel, Field


class BaseModel(PydanticBaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    name: str
    description: Optional[str] = ""

    def __str__(self):
        desc = " ".join([f"{k}='{v}'" for k, v in self.__dict__.items()])
        return f"<{self.__class__.__name__} {desc}>"

    __repr__ = __str__
