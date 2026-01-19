from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any, Dict
from app.db.mongodb import mongodb
from app.core.security import get_current_user
from app.models.user import User
from datetime import datetime, timedelta

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

        # Low Stock (<= 5)
        low_stock_products = await mongodb.db.products.find({"stock": {"$lte": 5}}).limit(5).to_list(5)
        for p in low_stock_products:
            p["_id"] = str(p["_id"])

        # Sales Chart (Last 7 Days)
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        
        pipeline_chart = [
            {"$match": {
                "status": {"$in": ["paid", "shipped"]},
                "created_at": {"$gte": seven_days_ago}
            }},
            {"$group": {
                "_id": {
                    "year": {"$year": "$created_at"},
                    "month": {"$month": "$created_at"},
                    "day": {"$dayOfMonth": "$created_at"}
                },
                "total": {"$sum": "$total_amount"}
            }},
            {"$sort": {"_id.year": 1, "_id.month": 1, "_id.day": 1}}
        ]
        
        chart_data = await mongodb.db.orders.aggregate(pipeline_chart).to_list(7)
        
        # Create a map for quick access
        data_map = {
            f"{entry['_id']['day']:02d}/{entry['_id']['month']:02d}": entry["total"] 
            for entry in chart_data
        }

        # Fill last 7 days
        sales_chart = []
        for i in range(6, -1, -1):
            date_obj = datetime.utcnow() - timedelta(days=i)
            date_key = f"{date_obj.day:02d}/{date_obj.month:02d}"
            sales_chart.append({
                "date": date_key,
                "total": data_map.get(date_key, 0.0)
            })

        return {
            "role": "admin",
            "total_users": total_users,
            "total_products": total_products,
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "recent_orders": recent_orders,
            "low_stock_products": low_stock_products,
            "sales_chart": sales_chart
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
