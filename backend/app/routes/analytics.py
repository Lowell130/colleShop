from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any, Dict
from app.db.mongodb import mongodb
from app.core.security import get_current_user
from app.models.user import User
from datetime import datetime

router = APIRouter()

@router.get("/dashboard", response_model=Dict[str, Any])
async def get_dashboard_data(current_user: User = Depends(get_current_user)) -> Any:
    
    if current_user.get("role") == "admin":
        # Admin Analytics
        total_users = await mongodb.db.users.count_documents({})
        total_products = await mongodb.db.products.count_documents({})
        total_orders = await mongodb.db.orders.count_documents({})
        
        # Calculate Total Revenue (only paid/shipped)
        pipeline = [
            {"$match": {"status": {"$in": ["paid", "shipped"]}}},
            {"$group": {"_id": None, "total": {"$sum": "$total_amount"}}}
        ]
        revenue_result = await mongodb.db.orders.aggregate(pipeline).to_list(1)
        total_revenue = revenue_result[0]["total"] if revenue_result else 0.0
        
        # Recent Orders
        recent_orders = await mongodb.db.orders.find().sort("created_at", -1).limit(5).to_list(5)
        
        # Convert ObjectId to string for recent orders
        for order in recent_orders:
            order["_id"] = str(order["_id"])
            if "user_id" in order: order["user_id"] = str(order["user_id"])
            
        return {
            "role": "admin",
            "total_users": total_users,
            "total_products": total_products,
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "recent_orders": recent_orders
        }
        
    else:
        # User Analytics
        user_id = str(current_user["_id"])
        total_orders = await mongodb.db.orders.count_documents({"user_id": user_id})
        
        pipeline = [
            {"$match": {"user_id": user_id, "status": {"$in": ["paid", "shipped"]}}},
            {"$group": {"_id": None, "total": {"$sum": "$total_amount"}}}
        ]
        spent_result = await mongodb.db.orders.aggregate(pipeline).to_list(1)
        total_spent = spent_result[0]["total"] if spent_result else 0.0
        
        last_order = await mongodb.db.orders.find_one({"user_id": user_id}, sort=[("created_at", -1)])
        if last_order:
             last_order["_id"] = str(last_order["_id"])
             last_order["user_id"] = str(last_order["user_id"])

        return {
            "role": "user",
            "total_orders": total_orders,
            "total_spent": total_spent,
            "last_order": last_order
        }
