from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: Optional[str] = None):
    response = {
        "item_id": item_id,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "tax": item.tax
    }
    
    if q:
        response["q"] = q 
    
    return response
