from pydantic import BaseModel, Field

from models.value_objects import FilmID


class FilmShortSchema(BaseModel):
    uuid: FilmID = Field(..., validation_alias="id")
    title: str
    imdb_rating: float


class IdNameSchema(BaseModel):
    uuid: FilmID = Field(..., validation_alias="id")
    name: str


class FilmDetailsSchema(BaseModel):
    uuid: FilmID = Field(..., validation_alias="id")
    title: str
    imdb_rating: float
    description: str | None = None
    genres: list[IdNameSchema]
    actors: list[IdNameSchema]
    writers: list[IdNameSchema]
    directors: list[IdNameSchema]
