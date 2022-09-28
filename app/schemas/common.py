from typing import Generic, Optional, TypeVar
from pydantic import BaseModel, validator, Field
from pydantic.generics import GenericModel


DataT = TypeVar('DataT')


class Error(BaseModel):
    code: int
    message: str


class DataResponseModel(GenericModel, Generic[DataT]):
    success: bool = True
    error_msg: Optional[Error]
    data: Optional[DataT]

    # @validator('error_msg', always=True)
    # def check_consistency(cls, v, values):
    #     if v is not None and values['data'] is not None:
    #         raise ValueError('must not provide both data and error')
    #     if v is None and values.get('data') is None:
    #         raise ValueError('must provide data or error')
    #     return v

    class Config:
        allow_population_by_field_name = True


class Pagination(BaseModel):
    skip: int = 0
    limit: int = 100
