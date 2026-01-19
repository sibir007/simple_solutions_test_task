from abc import ABCMeta, abstractmethod
from pydantic import BaseModel
from datetime import datetime, timezone
import requests
import inspect

class IndexPrise(BaseModel):
    stock: str
    idx: str
    idx_prise: float
    idx_prise_time: datetime

class ContractSise(BaseModel):
    stock: str
    contract_size: int

class StockBase:

    _stock_name = "stockbase"

    @classmethod
    def call_api_one(cls, stock_name: str, api_name: str, **kw):
        clss_met = cls._get_one_sub_class_met_by_stock_name(stock_name, api_name)
        if not clss_met:
            raise ValueError(f"api: {api_name} for stock {stock_name} not found")
        
        return clss_met[1](**kw)
    
    @classmethod
    def call_api_all(cls, api_name: str, **kw):
        sub_clss_met = cls._get_all_sub_class_met_by_met_name(api_name)
        if not sub_clss_met:
            raise ValueError(f"api: {api_name} not found")
        for cls_met in sub_clss_met:
            cls_met[1](**kw)
        return


    @classmethod
    def _get_one_sub_class_met_by_stock_name(cls, stock_name: str, met_name: str):
        sub_clss_met = cls._get_all_sub_class_met_by_met_name(met_name)
        for scls_met in sub_clss_met:
            if scls_met[0]._get_stock_name() == stock_name:
                return scls_met
        return []


    @classmethod
    def _get_all_sub_class_met_by_met_name(cls, method_name):
        sub_clss = cls._all_subclasses()
        sub_clss_met = []
        for cls_ in sub_clss:
            for met in inspect.getmembers(cls_, predicate=inspect.ismethod):
                if met[0] == method_name:
                    sub_clss_met.append([cls_, met[1]])
                    break
        return sub_clss_met
        

    @classmethod
    def _all_subclasses(cls):
        return (sub_cls for sub_cls in cls.__subclasses__())

    @classmethod
    def get_contract_size(cls) -> ContractSise:
        pass

    @classmethod
    def get_index_price(cls, index_name: str) -> IndexPrise:
        pass

    @classmethod
    def _get_stock_name(cls) -> str:
        return cls._stock_name


class SomeStock(StockBase):
    _stock_name = "somestock"

    @classmethod
    def get_index_price(cls, index_name: str) -> IndexPrise:
        print(f"----------{cls._get_stock_name()}---{index_name}------------------")

class DeriBit(StockBase):

    _stock_name = "deribit"

    @classmethod
    def get_index_price(cls, index_name: str) -> IndexPrise:
        # connect_timeout, read_timeout = 5.0, 30.0
        # url = f"https://test.deribit.com/api/v2/public/get_index_price?index_name={index_name}"
        
        # response = requests.get(url, timeout=(connect_timeout, read_timeout))
        # resp = response.json()
        # if not resp.result:
        #     raise requests.RequestException(resp)
        # return IndexPrise(stock=cls._get_stock_name(), 
        #                   idx=index_name, 
        #                   idx_prise=resp.index_price,
        #                   idx_prise_time=datetime.now(tz=timezone.utc))
        print(f"----------{cls._get_stock_name()}---{index_name}------------------")


if __name__ == '__main__':
    print("call deribit_index_price")
    StockBase.call_api_one('deribit', 'get_index_price', index_name='test')
    print("call somestock get_index_price")
    StockBase.call_api_one('somestock', 'get_index_price', index_name='test')
    print("call all get_index_price")
    StockBase.call_api_all('get_index_price', index_name='test')
