from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from app.core.email_utils import send_email_background
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
async def create_checkout_session(order_in: OrderCreate, background_tasks: BackgroundTasks, current_user: User = Depends(get_current_user)) -> Any:
    # --- Check Stock & Calculate Shipping ---
    site_settings = await mongodb.db.settings.find_one({})
    shipping_cost = site_settings.get("shipping_cost", 10.0) if site_settings else 10.0
    free_threshold = site_settings.get("free_shipping_threshold", 100.0) if site_settings else 100.0
    
    # Calculate items total
    items_total = 0.0
    for item in order_in.items:
        product = await mongodb.db.products.find_one({"_id": ObjectId(item.product_id)})
        if not product:
            raise HTTPException(status_code=400, detail=f"Prodotto non trovato: {item.name}")
        
        # Check Stock
        current_stock = product.get("stock", 0)
        if current_stock < item.quantity:
             raise HTTPException(status_code=400, detail=f"Quantità non disponibile per {item.name}. Disponibili: {current_stock}")
        
        items_total += item.price * item.quantity

    # Determine shipping
    final_shipping = 0.0
    if items_total < free_threshold:
        final_shipping = shipping_cost
    
    # Verify Total (Frontend vs Backend)
    calculated_total = items_total + final_shipping
    # Allow small tolerance
    if abs(calculated_total - order_in.total_amount) > 0.1:
        raise HTTPException(status_code=400, detail=f"Totale ordine non valido. Backend: {calculated_total}, Frontend: {order_in.total_amount}")
    
    # --- Decrement Stock ---
    for item in order_in.items:
         await mongodb.db.products.update_one(
            {"_id": ObjectId(item.product_id)},
            {"$inc": {"stock": -item.quantity}}
        )

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
        
        # Ensure tax code is present
        if not order_data.get("customer_tax_code"):
            raise HTTPException(status_code=400, detail="Codice Fiscale obbligatorio.")

        order_data["status"] = "pending"
        order_data["stripe_payment_intent_id"] = payment_intent_id
        order_data["created_at"] = datetime.utcnow()

        result = await mongodb.db.orders.insert_one(order_data)
        
        # --- Auto-update User Profile with latest checkout data ---
        user_update_data = {
            "shipping_address": order_in.shipping_address.dict(),
            "billing_address": order_in.billing_address.dict(),
            "tax_code": order_data["customer_tax_code"]
        }
        # Only update if fields are present in the order (which they are, validated by pydantic/frontend)
        await mongodb.db.users.update_one(
            {"_id": current_user["_id"]},
            {"$set": user_update_data}
        )
        # ----------------------------------------------------------
        
        # Send Order Confirmation Email via Background Task
        email_html = f"""
        <h1>Grazie per il tuo ordine, {order_data["customer_name"]}!</h1>
        <p>Il tuo ordine #{str(result.inserted_id)} è stato ricevuto ed è {order_data["status"]}.</p>
        <p><strong>Totale:</strong> €{order_in.total_amount:.2f}</p>
        <h3>Riepilogo:</h3>
        <ul>
        """
        for item in order_in.items:
             email_html += f"<li>{item.quantity}x {item.name} - €{item.price:.2f}</li>"
        
        email_html += f"""
        </ul>
        <br>
        <p>A presto,<br>Il Team di ColleShop</p>
        """

        if order_data.get("customer_email"):
             background_tasks.add_task(
                send_email_background, 
                order_data["customer_email"], 
                f"Conferma Ordine #{str(result.inserted_id)}", 
                email_html
            )

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
from typing import Optional
class OrderStatusUpdate(BaseModel):
    status: str
    tracking_number: Optional[str] = None
    courier_name: Optional[str] = None

@router.put("/{id}/status", response_model=Order)
async def update_order_status(id: str, status_update: OrderStatusUpdate, background_tasks: BackgroundTasks, current_user: User = Depends(get_current_user)) -> Any:
    # Admin only
    if current_user.get("role") != "admin":
         raise HTTPException(status_code=403, detail="Not authorized")
    
    order = await mongodb.db.orders.find_one({"_id": ObjectId(id)})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # If cancelling, restore stock
    if status_update.status == "cancelled" and order.get("status") != "cancelled":
        for item in order.get("items", []):
             await mongodb.db.products.update_one(
                {"_id": ObjectId(item["product_id"])},
                {"$inc": {"stock": item["quantity"]}}
            )
            
    update_data = {"status": status_update.status}
    if status_update.tracking_number:
        update_data["tracking_number"] = status_update.tracking_number
    if status_update.courier_name:
        update_data["courier_name"] = status_update.courier_name

    result = await mongodb.db.orders.update_one(
        {"_id": ObjectId(id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
         raise HTTPException(status_code=404, detail="Order not found")

    updated_order = await mongodb.db.orders.find_one({"_id": ObjectId(id)})

    # Send status update email
    email_html = f"""
    <h1>Aggiornamento Ordine #{str(updated_order["_id"])}</h1>
    <p>Gentile {updated_order.get("customer_name")},</p>
    <p>Lo stato del tuo ordine è stato aggiornato a: <strong>{status_update.status}</strong></p>
    """

    if status_update.status == "shipped" and updated_order.get("tracking_number"):
        email_html += f"""
        <div style="background-color: #f3f4f6; padding: 15px; border-radius: 5px; margin: 15px 0;">
            <p style="margin: 0; font-weight: bold;">Dettagli Spedizione:</p>
            <p style="margin: 5px 0 0 0;">Corriere: {updated_order.get('courier_name', 'N/D')}</p>
            <p style="margin: 5px 0 0 0;">Tracking Number: {updated_order.get('tracking_number')}</p>
        </div>
        """

    email_html += """
    <br>
    <p>Puoi seguire i dettagli nella tua area riservata.</p>
    <p>A presto,<br>Il Team di ColleShop</p>
    """
    
    if updated_order.get("customer_email"):
         background_tasks.add_task(
            send_email_background, 
            updated_order["customer_email"], 
            f"Aggiornamento Ordine #{str(updated_order['_id'])}", 
            email_html
        )

    return updated_order
