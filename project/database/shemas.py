from pydantic import BaseModel
from datetime import datetime, timezone


# derbit true get_index_price
# {
#   "jsonrpc": "2.0",
#   "result": {
#     "estimated_delivery_price": 90999.22,
#     "index_price": 90999.22
#   },
#   "usIn": 1768916400505372,
#   "usOut": 1768916400505576,
#   "usDiff": 204,
#   "testnet": true
# }

class GetIndexPriceResponse(BaseModel):
    jsonrpc: str
    result: dict[str, float]