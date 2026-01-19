from sqlmodel import SQLModel, Field
from datetime import datetime, date, time, timezone

class Exchange(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)

class Index(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    
class IndexPrice(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    exchange_id: int = Field(foreign_key='exchange.id', nullable=False)
    index_id: int = Field(foreign_key="index.id", nullable=False)
    prise: float = Field(nullable=False)
    timestamp: str
    