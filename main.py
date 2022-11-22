from typing import Union, List, Optional, Set
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI
from pydantic import BaseModel
from friend_recommend.Friend_Recommend import Friend_recommend

import json
app = FastAPI()

class Item(BaseModel):
    name: Union[str, None] = None
    price: Union[float, None] = None
    DB: list
    is_offer: Union[bool, None] = None

@app.get("/")
def read_root():
    return {"Hello": "World"}

# 친구 추천 함수 라우트
# @app.put("/test")
# def test_model(item: Item):
#     friend_list = Friend_recommend2(item.DB)
#     # json으로 호환 가능하게 데이터 타입을 바꿔주는 인코더
#     friend_list_jsonable = jsonable_encoder(friend_list)
#     # json.dumps(friend_list_jsonable)
#     return {"friend_recommend_list":friend_list_jsonable}

@app.put("/friend")
def Friend_model(item: Item):
    Friend_dict = Friend_recommend(item.DB)
    Friend_dict_json = jsonable_encoder(Friend_dict)
    return Friend_dict_json

@app.put("/feed")
def Feed_model(item: Item):
    Feed_dict = Feed_recommend(item.DB)
    Feed_dict = jsonable_encoder(Feed_dict)
    return Feed_dict

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.price, "item_id": item_id}
