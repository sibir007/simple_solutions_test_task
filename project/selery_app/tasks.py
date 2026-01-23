import time
from .app import app
from celery import Celery
from celery.schedules import crontab
import requests
from .stocks import StockBase
from database.write_data import write_index_price


@app.task
def get_index_price(index_name: str):

    try:
        raw_index_price = StockBase.call_api_one('deribit', 'get_index_price', index_name=index_name)
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return False
    
    write_index_price(raw_index_price)
    return True

@app.on_after_finalize.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    sender.add_periodic_task(60.0, get_index_price.s('btc_usd'), name='get_price_btc_usd')
    sender.add_periodic_task(60.0, get_index_price.s('eth_usd'), name='get_price_eth_usd')
    sender.add_periodic_task(60.0, get_index_price.s('btc_eurr'), name='get_price_btc_eurr')
    sender.add_periodic_task(60.0, get_index_price.s('eth_eurr'), name='get_price_eth_eurr')