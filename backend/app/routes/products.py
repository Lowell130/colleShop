
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Any
from app.models.product import Product, ProductCreate, ProductUpdate
from app.db.mongodb import mongodb
from bson import ObjectId

router = APIRouter()

@router.get("/", response_model=List[Product])
async def get_products(skip: int = 0, limit: int = 100) -> Any:
    products = await mongodb.db.products.find().skip(skip).limit(limit).to_list(100)
    return products

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product_in: ProductCreate) -> Any:
    product_data = product_in.dict()
    result = await mongodb.db.products.insert_one(product_data)
    created_product = await mongodb.db.products.find_one({"_id": result.inserted_id})
    return created_product

@router.get("/{id}", response_model=Product)
async def get_product(id: str) -> Any:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    product = await mongodb.db.products.find_one({"_id": ObjectId(id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{id}", response_model=Product)
async def update_product(id: str, product_in: ProductUpdate) -> Any:
    if not ObjectId.is_valid(id):
         raise HTTPException(status_code=400, detail="Invalid ID format")
    
    product_data = {k: v for k, v in product_in.dict().items() if v is not None}
    
    if len(product_data) >= 1:
        update_result = await mongodb.db.products.update_one(
            {"_id": ObjectId(id)}, {"$set": product_data}
        )
        if update_result.modified_count == 0:
             # Check if product exists
             existing = await mongodb.db.products.find_one({"_id": ObjectId(id)})
             if not existing:
                 raise HTTPException(status_code=404, detail="Product not found")

    updated_product = await mongodb.db.products.find_one({"_id": ObjectId(id)})
    return updated_product

@router.delete("/{id}", response_model=Product)
async def delete_product(id: str) -> Any:
    if not ObjectId.is_valid(id):
         raise HTTPException(status_code=400, detail="Invalid ID format")
         
    product = await mongodb.db.products.find_one({"_id": ObjectId(id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    await mongodb.db.products.delete_one({"_id": ObjectId(id)})
    return product
