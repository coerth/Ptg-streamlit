from pydantic import BaseModel

class Unit(BaseModel):
    name: str
    size: int
    path: str
    rank: int
    abilities: list[str]
    enchantments: list[str]
    battle_wounds: int
    battle_scars: list[str]
    points: int
