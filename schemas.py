from datetime import datetime

from pydantic import BaseModel


class FieldRequest(BaseModel):
    name: str = None
    required: bool = False
    empty_value: str = None


class TemplateResponse(BaseModel):
    class Config:
        orm_mode = True
    id: int
    file_name: str
    file_size: int
    created_at: datetime
    updated_at: datetime = None
    fields: list


class ProcessResponse(BaseModel):
    result: str
