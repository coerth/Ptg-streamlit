from pydantic import BaseModel


class Army(BaseModel):
    name: str
    faction: str