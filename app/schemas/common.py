from typing import Generic, Optional, TypeVar, Union
from pydantic import BaseModel, validator, Field
from pydantic.generics import GenericModel


M = TypeVar("M", bound=BaseModel)


class Error(BaseModel):
    code: int
    message: str


class BaseGenericResponse(GenericModel):
    success: bool


class DataListResponse(BaseGenericResponse, Generic[M]):
    count: Optional[int]
    data: list[M]

    class Config:
        allow_population_by_field_name = True


class DataResponse(BaseGenericResponse, Generic[M]):
    data: Optional[M]

    class Config:
        allow_population_by_field_name = True


class Pagination(BaseModel):
    skip: int = 0
    limit: int = 100


class CommonQueryParams:
    def __init__(self, q: Union[str, None] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit
