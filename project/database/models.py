from sqlmodel import SQLModel, Field
from datetime import datetime, date, time, timezone


class Exchange(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str



class Index(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str




class IndexPrice(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    exc_id: int = Field(foreign_key="exchange.id")
    idx_id: int = Field(foreign_key="index.id")
    timestamp: datetime = Field(nullable=False)
    prise: float = Field(nullable=False)
