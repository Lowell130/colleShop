from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from typing import Optional, List, Annotated
from bson import ObjectId
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]

from app.models.user import Address

class OrderItem(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int

class OrderBase(BaseModel):
    items: List[OrderItem]
    total_amount: float
    status: str = "pending" # pending, paid, shipped
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_tax_code: Optional[str] = None
    shipping_address: Address
    billing_address: Address
    stripe_payment_intent_id: Optional[str] = None
    tracking_number: Optional[str] = None
    courier_name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class OrderCreate(BaseModel):
    items: List[OrderItem]
    total_amount: float # Optionally calculated on backend for security
    shipping_address: Address
    billing_address: Address
    customer_tax_code: Optional[str] = None
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None

class Order(OrderBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
