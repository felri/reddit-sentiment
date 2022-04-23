from pydantic import BaseModel
import typing as t


class TickerBase(BaseModel):
    ticket: str


class Ticket(TickerBase):
    id: int

    class Config:
        orm_mode = True


class ChartBase(BaseModel):
    ticket_id: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    date: str


class ChartCreate(ChartBase):
    class Config:
        orm_mode = True


class ChartOut(BaseModel):
    pass


class Chart(ChartBase):
    id: int

    class Config:
        orm_mode = True
