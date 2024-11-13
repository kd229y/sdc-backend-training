from typing import Annotated
from fastapi import Path, Query, FastAPI
app=FastAPI()
@app.get("/")
async def empty():
    return {"message": "Hello World"}
@app.get("/items/{item_id}")
async def HW3_1(
    item_id: Annotated[int, Path(ge=1, le=1000)], 
    q: Annotated[str | None, Query(min_length=3, max_length=50)] = None, 
    sort_order: str | None = "asc"):
    
    results = {"item_id": item_id}
    
    if q:
        results.update({"description": f"This is a sample item that matches the query {q}"})
    else:
        results.update({"description": "This is a sample item."})
    
    results.update({"sort_order": sort_order})
    
    return results

# 2. PUT "/items/{item_id}" Endpoint
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float

@app.put("/items/{item_id}")
async def HW3_2(
    item_id: Annotated[int, Path(ge=1, le=1000)],
    item: Item,
    q: Annotated[str | None, Query(min_length=3, max_length=50)] = None):
    
    results = {
		"item_id": item_id,
		**item.model_dump()
	}
    if q:
        results.update({"q": q})
    
    return results