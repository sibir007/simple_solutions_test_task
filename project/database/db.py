import os

from sqlmodel import create_engine, SQLModel, Session
from . import models
import datetime
# from models import Exchange

# DATABASE_URL = os.environ.get("DATABASE_URL")

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)
# engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)

def drop_db():
    SQLModel.metadata.drop_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

def fill_db():
    exch1 = models.Exchange(name="Binance")
    exch2 = models.Exchange(name="Upbit")
    ix1 = models.Index("aaa")
    ix2 = models.Index("bbb")
    ip = models.IndexPrice(exchange_id=exch1.id, index_id=ix1.id, prise=123.123, )



    with Session(engine) as session:
        session.add(exch1)
        session.add(exch2)
        session.add(exch3)
        session.add(exch4)
        session.commit()



def main():
    # drop_db()
    init_db()
    fill_db()

if __name__ == "__main__":
    main()