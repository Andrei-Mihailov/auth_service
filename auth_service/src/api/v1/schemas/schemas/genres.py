from pydantic import BaseModel, Field

from models.value_objects import GenreID


class GenreDetailsSchema(BaseModel):
    uuid: GenreID = Field(..., validation_alias="id")
    name: str
    description: str | None = None
