from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import mysql.connector

# Database Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "database": "test_db"
}

# Initialize FastAPI app
app = FastAPI()

# Pydantic models
class Item(BaseModel):
    id: int = None  # Auto-incrementing primary key
    name: str
    description: str
    price: float

class ItemCreate(BaseModel):
    name: str
    description: str
    price: float

# Database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Routes
@app.post("/items", response_model=Item)
def create_item(item: ItemCreate):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO items (name, description, price) VALUES (%s, %s, %s)"
    cursor.execute(query, (item.name, item.description, item.price))
    connection.commit()
    item_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return {**item.dict(), "id": item_id}

@app.get("/items", response_model=List[Item])
def read_items():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM items"
    cursor.execute(query)
    items = cursor.fetchall()
    cursor.close()
    connection.close()
    return items

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM items WHERE id = %s"
    cursor.execute(query, (item_id,))
    item = cursor.fetchone()
    cursor.close()
    connection.close()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemCreate):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE items SET name = %s, description = %s, price = %s WHERE id = %s"
    cursor.execute(query, (item.name, item.description, item.price, item_id))
    connection.commit()
    cursor.close()
    connection.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {**item.dict(), "id": item_id}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM items WHERE id = %s"
    cursor.execute(query, (item_id,))
    connection.commit()
    cursor.close()
    connection.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}

# Run using `uvicorn server:app --reload`
