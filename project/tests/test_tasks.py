# from selery_app.tasks import create_task, get_index_price
from datetime import datetime
from unittest.mock import patch
import json
from fastapi import Response


# def test_home(test_app):
#     response = test_app.get("/")
#     assert response.status_code == 200
        # t1 = Ticker(id=1, name="
        # ")
        # t2 = Ticker(id=2, name="
        # ")
        # i1 = Index(id=1,name="usd")
        # i2 = Index(id=2,name="eurr")
        # s1 = Stock(id=1, name="deribit")
        # s2 =  Stock(id=2,name="somestock")


def test_case1(client):
    response: Response = client.get("/deribit?ticker=btc") 
    # print("test_case1:", response.json())
    assert response.status_code == 200
    resp: list[dict] = response.json()
    assert len(resp) == 8640 # 3d*24h*60m*2index=8640rows
    assert {'stock': 'deribit', 'ticker': 'btc', 'index': 'eurr', 'price': 1.0, 'date': '2026-01-01T15:25:00'} in resp
    assert {'stock': 'deribit', 'ticker': 'btc', 'index': 'usd', 'price': 1.0, 'date': '2026-01-01T15:25:00'} in resp


def test_case2(client):
    response: Response = client.get("/deribit?ticker=btc&index=usd")
    # print("test_case2:", response.json())
    assert response.status_code == 200
    resp: list[dict] = response.json()
    assert len(resp) == 4320 # 3d*24h*60m*1index=4320rows
    assert not {'stock': 'deribit', 'ticker': 'btc', 'index': 'eurr', 'price': 1.0, 'date': '2026-01-01T15:25:00'} in resp
    assert {'stock': 'deribit', 'ticker': 'btc', 'index': 'usd', 'price': 1.0, 'date': '2026-01-01T15:25:00'} in resp


def test_case3(client):
    response: Response = client.get("/deribit?ticker=btc&index=usd&dates=2026-01-02T00:00:00.000000&dates=2026-01-02T23:59:59.999999")
    assert response.status_code == 200
    resp: list[dict] = response.json()
    # assert len(resp) == 4320 #  1d*24h*60m*1index=1440 
    # # day not math
    # assert not {'stock': 'deribit', 'ticker': 'btc', 'index': 'usd', 'price': 1.0, 'date': '2026-01-01T15:25:00'} in resp
    # # day and index not math
    # assert not {'stock': 'deribit', 'ticker': 'btc', 'index': 'eurr', 'price': 1.0, 'date': '2026-01-01T15:25:00'} in resp
    # # day and index math
    # assert {'stock': 'deribit', 'ticker': 'btc', 'index': 'usd', 'price': 1.0, 'date': '2026-01-02T15:25:00'} in resp


# def test_db(test_db_session):
#     # response = test_app.get("/")
#     assert True


# def test_home(test_app):
#     response = test_app.get("/{stock}/price?ticker=btc")
#     assert response.status_code == 200



# def test_task():
#     assert create_task.run(1)
#     assert create_task.run(2)
#     assert create_task.run(3)


# @patch("selery_app.tasks.create_task.run")
# def test_mock_task(mock_run):
#     assert create_task.run(1)
#     create_task.run.assert_called_once_with(1)

#     assert create_task.run(2)
#     assert create_task.run.call_count == 2

#     assert create_task.run(3)
#     assert create_task.run.call_count == 3

# def test_task_status(test_app):
#     response = test_app.post(
#         "/tasks",
#         data=json.dumps({"type": 1})
#     )
#     content = response.json()
#     task_id = content["task_id"]
#     assert task_id

#     response = test_app.get(f"tasks/{task_id}")
#     content = response.json()
#     assert content == {"task_id": task_id, "task_status": "PENDING", "task_result": None}
#     assert response.status_code == 200

#     while content["task_status"] == "PENDING":
#         response = test_app.get(f"tasks/{task_id}")
#         content = response.json()
#     assert content == {"task_id": task_id, "task_status": "SUCCESS", "task_result": True}

# def test_get_index_price():
#     assert get_index_price.run("btc_usd")

# def test_get_index_price_async():
#     task = get_index_price.delay("btc_usd")
#     print(task.id)
#     assert task.id
