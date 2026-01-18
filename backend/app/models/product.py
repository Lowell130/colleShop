
from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from typing import Optional, Annotated
from bson import ObjectId

PyObjectId = Annotated[str, BeforeValidator(str)]

class ProductBase(BaseModel):
    name: str
    type: str # Bianco, Rosso, Rosato, etc.
    price: float
    description: str
    grape: str
    year: str
    alcohol: Optional[str] = None
    temp: Optional[str] = None
    pairing: Optional[str] = None
    image: Optional[str] = None
    stock: int = 0

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    grape: Optional[str] = None
    year: Optional[str] = None
    alcohol: Optional[str] = None
    temp: Optional[str] = None
    pairing: Optional[str] = None
    image: Optional[str] = None
    stock: Optional[int] = None

class Product(ProductBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
