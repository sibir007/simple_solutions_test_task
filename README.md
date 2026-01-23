# simple_solutions_test_task

# SRS

1. Написать клиент для криптобиржи Deribit (https://docs.deribit.com/). Клиент должен каждую минуту забирать с биржи текущую цену btc_usd и eth_usd (index price валюты) после чего сохранять в базу данных тикер валюты, текущую цену и время в UNIX timestamp.

**Выполнено:**

**Celery worker задача:**
```py
# simple_solutions_test_task/project/selery_app/tasks.py
...
@app.task
def get_index_price(index_name: str):

    try:
        raw_index_price = StockBase.call_api_one('deribit', 'get_index_price', index_name=index_name)
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return False
    
    write_index_price(raw_index_price)
    return True
...
```
**Celery beat периодизация:**
```py
# simple_solutions_test_task/project/selery_app/tasks.py
...

@app.on_after_finalize.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    sender.add_periodic_task(60.0, get_index_price.s('btc_usd'), name='get_price_btc_usd')
    sender.add_periodic_task(60.0, get_index_price.s('eth_usd'), name='get_price_eth_usd')
    sender.add_periodic_task(60.0, get_index_price.s('btc_eurr'), name='get_price_btc_eurr')
    sender.add_periodic_task(60.0, get_index_price.s('eth_eurr'), name='get_price_eth_eurr')
...
```

2. Написать внешнее API для обработки сохраненных данных на FastAPI.

**Выполнено**

**Fastapi app:**
```py
# simple_solutions_test_task/project/fastapi_app/main/py
...

@app.get("/{stock}")
async def home(
    stock: Annotated[
        Literal["deribit", "somestock"],
        Path(title="Stock", description="Stock for request"),
    ],
    ticker: Annotated[
        Literal["btc", "eth"], Query(title="Ticker", description="Ticker for request")
    ],
    index: Annotated[
        Literal["usd", "eurr"] | None,
        Query(title="Index", description="Index for request"),
    ] = None,
    dates: Annotated[
        list[datetime] | None,
        Query(title="Dates", description="Dates for request", max_length=2),
    ] = None,
):
    
    query_items = get_trick_index_info({"stock":stock, "ticker":ticker, "index":index, "dates":dates})
    return query_items

...

```

Обязательные требования:
1. API должно включать в себя следующие методы:

***Выполнено одним методом (entrypoint)***
- Получение всех сохраненных данных по указанной валюте
```py
# simple_solutions_test_task/project/tests/test_tasks.py
...
# all prices for ticker by all indexes
def test_case1(client):
    response: Response = client.get("/deribit?ticker=btc") 
    assert response.status_code == 200
    resp: list[dict] = response.json()
    assert len(resp) == 8640 # 3d*24h*60m*2index=8640rows
    assert {'stock': 'deribit', 'ticker': 'btc', 'index': 'eurr', 'price': 1.0, 'date': '2026-01-01T15:25:00'} in resp
    assert {'stock': 'deribit', 'ticker': 'btc', 'index': 'usd', 'price': 1.0, 'date': '2026-01-01T15:25:00'} in resp
...
```
- Получение последней цены валюты
- Получение цены валюты с фильтром по дате
Все методы должны быть GET и у каждого метода должен быть обязательный query-параметр “ticker”.
2. В качестве БД использовать PostgreSQL.
3. Код выложить на gitlab с подробным readme и документацией по разворачиванию. В readme добавить секцию Design decisions.
4. Для периодического получения цен использовать Celery.
Необязательные требования:
1. Написать unit тесты для основных методов
2. Развернуть приложение в двух контейнерах для приложения и базы данных. 
3. Применить aiohttp при написании клиента.







https://testdriven.io/blog/fastapi-and-celery/
https://python.plainenglish.io/asynchronous-task-queuing-with-celery-d9709364e686
https://testdriven.io/blog/fastapi-sqlmodel/


```sh
(.venv) sibir007@sibir007:~/repos/simple_solutions-_test_task$ sudo docker compose up -d
WARN[0000] /home/sibir007/repos/simple_solutions-_test_task/compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion WARN[0000] No services to build                         
[+] up 3/3
 ✔ Volume simple_solutions-_test_task_pgdata     Created              0.0s 
 ✔ Container simple_solutions-_test_task-redis-1 Running              0.0s 
 ✔ Container postgres_db                         Created              0.1s 
(.venv) sibir007@sibir007:~/repos/simple_solutions-_test_task$ sudo dosker ps
[sudo] password for sibir007: 
sudo: dosker: command not found
(.venv) sibir007@sibir007:~/repos/simple_solutions-_test_task$ sudo docker ps
CONTAINER ID   IMAGE             COMMAND                  CREATED          STATUS          PORTS                                         NAMES
41da061eaaa3   postgres:latest   "docker-entrypoint.s…"   11 minutes ago   Up 11 minutes   0.0.0.0:5430->5432/tcp, [::]:5430->5432/tcp   postgres_db
4d6415e4ab01   redis:latest      "docker-entrypoint.s…"   2 hours ago      Up 2 hours      6379/tcp                                      simple_solutions-_test_task-redis-1
(.venv) sibir007@sibir007:~/repos/simple_solutions-_test_task$ psql -h localhost -p 5430 -d postgres -U postgres
Password for user postgres: 
postgres=# CREATE DATABASE celery;
CREATE DATABASE
postgres=# SELECT datname, dattablespace FROM pg_catalog.pg_database;
  datname  | dattablespace 
-----------+---------------
 postgres  |          1663
 celery    |          1663
 template1 |          1663
 template0 |          1663
(4 rows)
postgres=# \c celery
You are now connected to database "celery" as user "postgres".
celery=# \dt
Did not find any relations.
celery=# \q
(.venv) sibir007@sibir007:~/repos/simple_solutions-_test_task$ 
```

```sh
sudo docker compose up -d --no-deps --build <service_name>
```

```sh
sudo docker compose exec web python -m pytest
```

```sh
(.venv) sibir007@sibir007:~/repos/simple_solutions_test_task$ redis-cli ping
PONG
```

```sh
sudo docker compose exec web python -m pytest -k "test_mock_task"
```

```sh
sudo docker exec web python -m pytest -s -k test_get_index_price # -s выод print to terminal
```