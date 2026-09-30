from uuid import UUID
from datetime import date
import re

from pydantic import BaseModel, field_validator, model_validator


class Date(BaseModel):
    month: int
    year: int


class Course(BaseModel):
    id_: UUID
    name: str

    @field_validator("name")        # noqa : способ приведен на оф. сайте
    @classmethod
    def clean_name(cls, raw: str) -> str:
        sub_info = raw.rfind('(ИДДО')
        if sub_info != -1:
            return raw[:sub_info-1]
        return raw


class Event(BaseModel):
    id_: UUID
    name: str
    type_: str          # числовой тип ивента; маппинг неизвестен, сейчас ивент берется из name
    str_type: str
    date_start: date
    date_end: date
    course: Course

    @model_validator(mode="before")
    def clean_name_gen_type(self) -> dict:
        raw_name = re.sub(r'<[^>]+>', '', self['name']).strip()

        if '_' not in raw_name:
            parts = raw_name.rsplit('. ', maxsplit=2)
            if len(parts) == 3:
                cutted = '. '.join(parts[:2])
                t = parts[2]
            else:
                cutted, t = raw_name, ''
            cleaned = cutted.strip()
        else:
            t = 'Итоговая работа'
            separated = raw_name.split('-Б-')[0]
            cleaned = separated.replace('_', ' ')

        self['str_type'] = t
        self['name'] = cleaned

        return self     # noqa : способ приведен на оф. сайте
