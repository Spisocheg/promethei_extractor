from uuid import UUID
from datetime import date
from typing import Literal

from pydantic import BaseModel, field_validator, computed_field


class Date(BaseModel):
    month: int
    year: int


class Course(BaseModel):
    id_: UUID
    name: str

    @field_validator("name")
    @classmethod
    def clean_name(cls, raw: str) -> str:
        sub_info = raw.rfind('(ИДДО')
        return raw[:sub_info-1]


class Event(BaseModel):
    id_: UUID
    name: str
    # type_: Literal['Тестирование', 'Экзамен тест', 'Письменная работа', 'Экзамен письм. работа']
    type_: int          # до того как будет точно известен маппинг номера типа с самим типом
    date_start: date
    date_end: date
    course: Course

    @field_validator("name")
    @classmethod
    def clean_name(cls, raw: str) -> str:
        if '_' not in raw:
            last_dot = raw.rfind('.')
            cutted = raw[:last_dot]
            cleaned = str(filter(lambda char: char not in ('<', 'b', '>', '/'), cutted))
        else:
            separated = raw.split('-Б-')[0]
            cleaned = separated.replace('_', ' ')
        return cleaned
