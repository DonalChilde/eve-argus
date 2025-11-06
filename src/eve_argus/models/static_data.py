from pydantic import BaseModel, Field


class Category(BaseModel):
    _key: int
    name: str
    published: bool
    icon_id: int | None = None
