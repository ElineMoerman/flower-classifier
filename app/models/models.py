from pydantic import BaseModel
from typing import Optional

class Flower(BaseModel):
    id: Optional[int]
    name: str
    description: Optional[str] = None
    species: str
    color: str

    class Config:
        orm_mode = True