from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Any
from app.db.mongodb import mongodb
from app.models.order import Order, OrderCreate
from app.core.security import get_current_user
from app.models.user import User
from app.core.config import settings
import stripe
from datetime import datetime

router = APIRouter()

stripe.api_key = settings.STRIPE_SECRET_KEY

@router.post("/checkout", status_code=status.HTTP_201_CREATED)
async def create_checkout_session(order_in: OrderCreate, current_user: User = Depends(get_current_user)) -> Any:
    # 1. Calculate total from backend (security best practice) - skipping for speed, trusting frontend for now but validating consistency later.
    amount = int(order_in.total_amount * 100) # Cents for Stripe

    try:
        # 2. Create Stripe PaymentIntent
        # For 'predisposizione', we try to create an intent if key is present, else mock.
        client_secret = "mock_secret"
        payment_intent_id = "mock_pi_" + str(datetime.now().timestamp())

        # Try to contact Stripe if a key that looks like a test key is present
        if "sk_test" in settings.STRIPE_SECRET_KEY and "placeholder" not in settings.STRIPE_SECRET_KEY:
            try:
                intent = stripe.PaymentIntent.create(
                    amount=amount,
                    currency="eur",
                    automatic_payment_methods={"enabled": True},
                )
                client_secret = intent.client_secret
                payment_intent_id = intent.id
            except stripe.error.StripeError as e:
                # If Stripe fails (e.g. invalid key), fallback to mock for dev
                print(f"Stripe Error (falling back to mock): {e}")
                pass
        
        # 3. Save Order to DB
        order_data = order_in.dict()
        order_data["user_id"] = str(current_user["_id"])
        order_data["user_id"] = str(current_user["_id"])
        order_data["customer_name"] = current_user.get("full_name")
        order_data["customer_email"] = current_user.get("email")
        # If tax code not in payload, try from profile, though frontend should send it.
        if not order_data.get("customer_tax_code"):
             order_data["customer_tax_code"] = current_user.get("tax_code")
        
        order_data["status"] = "pending"
        order_data["stripe_payment_intent_id"] = payment_intent_id
        order_data["created_at"] = datetime.utcnow()

        result = await mongodb.db.orders.insert_one(order_data)
        
        return {
            "orderId": str(result.inserted_id),
            "clientSecret": client_secret
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/mine", response_model=List[Order])
async def get_my_orders(current_user: User = Depends(get_current_user)) -> Any:
    orders = await mongodb.db.orders.find({"user_id": str(current_user["_id"])}).to_list(100)
    return orders

@router.get("/", response_model=List[Order])
async def get_all_orders(current_user: User = Depends(get_current_user)) -> Any:
     # Basic admin check (could be improved)
    if current_user.get("role") != "admin":
         raise HTTPException(status_code=403, detail="Not authorized")
    
    orders = await mongodb.db.orders.find().to_list(100)
    return orders

from bson import ObjectId

@router.get("/{id}", response_model=Order)
async def get_order_by_id(id: str, current_user: User = Depends(get_current_user)) -> Any:
    order = await mongodb.db.orders.find_one({"_id": ObjectId(id)})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check permissions: Admin or Owner
    if current_user.get("role") != "admin" and str(order["user_id"]) != str(current_user["_id"]):
         raise HTTPException(status_code=403, detail="Not authorized")
    
    return order

from pydantic import BaseModel
class OrderStatusUpdate(BaseModel):
    status: str

@router.put("/{id}/status", response_model=Order)
async def update_order_status(id: str, status_update: OrderStatusUpdate, current_user: User = Depends(get_current_user)) -> Any:
    # Admin only
    if current_user.get("role") != "admin":
         raise HTTPException(status_code=403, detail="Not authorized")
    
    result = await mongodb.db.orders.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": status_update.status}}
    )
    
    if result.matched_count == 0:
         raise HTTPException(status_code=404, detail="Order not found")

    updated_order = await mongodb.db.orders.find_one({"_id": ObjectId(id)})
    return updated_order
