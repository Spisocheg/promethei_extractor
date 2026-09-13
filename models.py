from pydantic import BaseModel


class Date(BaseModel):
    month: int
    year: int



