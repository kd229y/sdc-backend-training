from fastapi import FastAPI, Query, Body, Cookie, Path, File, Form, UploadFile, HTTPException, status
from typing import Annotated, List, Optional
from decimal import Decimal
from pydantic import BaseModel, Field
from datetime import datetime, time, timedelta
from uuid import UUID
app = FastAPI()

class Item(BaseModel):
    name: str
    description: str| None = None
    price: float
    tax: float| None = None
@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.get("/items/{item_id}")
async def read_item(
        item_id: Annotated[Decimal, Path(ge=1, le=1000, description="Item ID must be between 1 and 1000.")], 
        q: Annotated[str | None, Query(min_length=3, max_length=50, description="Query 'q' must be between 3 and 50 characters.")] = None, 
        sort_order: str = "asc"
    ):
    response = {
        "item_id": item_id,
        "description": f"This is a sample item that matches the query {q}" if q else "This is a sample item.",
        "sort_order": sort_order
    }
    
    return response
@app.put("/items/{item_id}")
async def update_item(
                      item_id: Annotated[Decimal, Path(ge=1, le=1000, description="Item ID must be between 1 and 1000.")], 
                      item: Item = None, 
                      q: Annotated[str | None, Query(min_length=3, max_length=50, description="Query 'q' must be between 3 and 50 characters.")] = None
                      ):
    updated_item = item.model_dump()
    response = {"item_id": item_id, **updated_item}
    if q:
        response.update({"q": q})

    return response

class Item_1(BaseModel):
    name: str
    description: str| None = Field(default=None, title="The description of the item")
    price: float = Field(gt = 0., description="The price of the item must greater than zero")
    tax: float = Field(gt = 0., description="The tax of the item must greater than zero")

@app.post("/items/filter/")
async def read_items(
    price_min: Annotated[int , Query(description = "Minimum price of the item")] = None,
    price_max: Annotated[int , Query(description = "Maximum price of the item")] = None,
    tax_included: Annotated[bool, Query(description = "Boolean indicating whether tax is included in the price")] = None,
    tags: Annotated[list[str], Query(description="List of tags to filter items")] = None
    ):
    return {
        "price_range": [price_min, price_max],
        "tax_included": tax_included,
        "tags": tags,
        "message": "This is a filtered list of items based on the provided criteria."
    }
@app.post("/items/create_with_fields/")
async def add_item(
    item: Annotated[Item_1, Body()],
    importance: Annotated[int , Body()]
):
    return {
        "item": item,
        "importance": importance
    }
@app.post("/offers/")
async def add_offer(
    name: Annotated[str, Body()],
    discount: Annotated[float, Body()],
    items: Annotated[list[Item_1], Body()]
):
    return {
        "offer_name": name,
        "discount": discount,
        "items": items
    }
@app.post("/users/")
async def add_user(
    username: Annotated[str, Body()],
    email: Annotated[str, Body()],
    full_name: Annotated[str, Body()],
):
    return {
        "username": username,
        "email": email,
        "full_name": full_name
    }
@app.post("/items/extra_data_types/")
async def add_extra_data_types(
    start_time: Annotated[datetime, Body()],
    end_time: Annotated[time, Body()],
    repeat_every: Annotated[timedelta, Body()],
    process_id: Annotated[UUID, Body()]
):
    return {
        "message": "This is an item with extra data types.",
        "start_time": start_time,
        "end_time": end_time,
        "repeat_every": repeat_every,
        "process_id": process_id

    }
@app.get("/items/cookies/")
async def read_items_from_cookies(
    session_id: Annotated[str, Cookie()]
):
    return {
        "session_id": session_id,
        "message": "This is the session ID obtained from the cookies."
    }

@app.post("/items/form_and_file/")
async def add_form_and_file(
    name: Annotated[str, Form()],
    price: Annotated[float, Form()],
    file: Annotated[UploadFile, File()] = None,
    description: Annotated[str, Form()] = None,
    tax: Annotated[float, Form()] = None
):
    if price < 0.0:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail = "Price cannot be negative"
            )

    if not file:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail = "The file is missing"
            )

    results = {"name": name, "price": price, "filename": file.filename, "message": "This is an item created using form data and a file."}
    if description:
        results.update({"description": description})
    if tax:
        results.update({"tax": tax})
    return results

class Author(BaseModel):
    name: str = Field(..., example="Jane Doe")
    age: int = Field(..., ge=0, example=45)

class Book(BaseModel):
    title: str = Field(..., example="A Journey to FastAPI")
    author: Author
    summary: Optional[str] = Field(None, example="An introductory book about FastAPI.")


@app.get("/books/", response_model=List[Book])
async def get_books():

    return[ 
        Book(title="Book 1", author=Author(name="Author 1", age=40), summary="A great book about..."),
        Book(title="Book 2", author=Author(name="Author 2", age=38), summary="An interesting journey of..."),
    ]

@app.post("/books/create_with_author/")
async def create_book(book: Book):
    return {"title": book.title, "author": book.author, "summary": book.summary}

@app.post("/books/", status_code=201)
async def create_book(book: Book):
    return {"title": book.title, "author": book.author, "summary": book.summary}