from uuid import UUID
from datetime import date
from typing import Literal

from pydantic import BaseModel, field_validator, computed_field, model_validator


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
    str_type: str
    date_start: date
    date_end: date
    course: Course

    # @field_validator("name")
    # @classmethod
    # def clean_name(cls, raw: str) -> str:
    #     if '_' not in raw:
    #         last_dot = raw.rfind('.')
    #         cutted = raw[:last_dot]
    #         cleaned = str(filter(lambda char: char not in ('<', 'b', '>', '/'), cutted))
    #     else:
    #         separated = raw.split('-Б-')[0]
    #         cleaned = separated.replace('_', ' ')
    #     return cleaned

    @model_validator(mode="before")
    def clean_name_gen_type(self) -> dict:
        raw_name = self['name']
        if '_' not in raw_name:
            cutted, t = raw_name.rsplit('. ', maxsplit=1)
            # last_dot = raw_name.rfind('.')
            # cutted = raw_name[:last_dot]
            cleaned = "".join(filter(lambda char: char not in ('<', 'b', '>', '/'), cutted))
        else:
            t = 'Итоговая работа'
            separated = raw_name.split('-Б-')[0]
            cleaned = separated.replace('_', ' ')

        self['str_type'] = t
        self['name'] = cleaned

        return self
