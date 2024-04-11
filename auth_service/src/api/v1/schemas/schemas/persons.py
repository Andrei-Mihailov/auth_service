from pydantic import BaseModel, Field

from models.value_objects import FilmID, PersonID, Roles


class PersonFilmShortSchema(BaseModel):
    uuid: FilmID = Field(..., validation_alias="id")
    roles: list[Roles]


class PersonFilmDetailedSchema(PersonFilmShortSchema):
    title: str
    imdb_rating: float


class PersonDetailsSchema(BaseModel):
    uuid: PersonID = Field(..., validation_alias="id")
    full_name: str
    films: list[PersonFilmShortSchema]
