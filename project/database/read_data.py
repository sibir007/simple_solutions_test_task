from sqlmodel import Session, select
from .db import engine
from shemas.selery_app_shemas import RawIndexPrise, RawContractSise
from shemas.db_models import Stock, Index, IndexPrice, Ticker
from datetime import datetime


def select_st():
    return (
            select(
                Stock.name,
                Ticker.name,
                Index.name,
                IndexPrice.price,
                IndexPrice.timestamp,
            )
            .join(Stock, isouter=True)
            .join(Ticker, isouter=True)
            .join(Index, isouter=True)
        )

def pack_to_dict_list(tuple_list):
    return [{"stock": stock, "ticker": ticker, "index": index, "price": price,  "date": dates} for 
                          stock, ticker, index, price, dates in tuple_list]

def get_index_case_1(stock, ticker):
    with Session(engine) as s:
        select_st_where = select_st()\
            .where(Stock.name == stock)\
                .where(Ticker.name == ticker)
        res_rows = s.exec(select_st_where).all()
    return pack_to_dict_list(res_rows)
    
def get_index_case_2(stock, ticker, index):
    with Session(engine) as s:
        select_st_where = select_st()\
            .where(Stock.name == stock)\
                .where(Ticker.name == ticker)\
                    .where(Index.name == index)
        res_rows = s.exec(select_st_where).all()
    return pack_to_dict_list(res_rows)

def get_trick_index_info(request):
    with Session(engine) as session:
        match request:
            # case_1 client.get("/deribit?ticker=btc")
            case {"stock": stock, "ticker": ticker, "index": None, "dates": None}:
                return get_index_case_1(stock, ticker)
            # case_2 client.get("/deribit?ticker=btc&index=usd")
            case {"stock": stock, "ticker": ticker, "index": index, "dates": None}:
                return get_index_case_2(stock, ticker, index)
            case {"stock": stock, "ticker": ticker, "index": index, "dates": dates}:
                match dates:
                    # case_3 client.get("/deribit?ticker=btc&index=usd&dates=2026-01-02T00:00:00.000000&dates=2026-01-02T23:59:59.999999")
                    case [date1, date2]:
                        return [
                            {
                                "stock": stock,
                                "ticker": ticker,
                                "index": index,
                                "dates": [date1, date2],
                            }
                        ]
                    # case_4
                    case [date]:
                        return [
                            {
                                "stock": stock,
                                "ticker": ticker,
                                "index": index,
                                "dates": [date],
                            }
                        ]
            case {"stock": stock, "ticker": ticker, "index": None, "dates": dates}:
                match dates:
                    # case_5
                    case [date1, date2]:
                        return [
                            {
                                "stock": stock,
                                "ticker": ticker,
                                "index": None,
                                "dates": [date1, date2],
                            }
                        ]
                    # case_6
                    case [date]:
                        return [
                            {
                                "stock": stock,
                                "ticker": ticker,
                                "index": None,
                                "dates": [date],
                            }
                        ]
            case _:
                return [{"stock": None, "ticker": None, "index": None, "dates": None}]


