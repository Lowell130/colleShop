import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import traceback

async def seed_products():
    print(f"Connecting to MongoDB at {settings.MONGO_URI}...")
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client.get_default_database()
    products_collection = db["products"]

    # Clear existing products to avoid duplicates during dev
    print("Clearing existing products...")
    await products_collection.delete_many({})

    products = [
        {
            "name": "Tintilia del Molise DOC",
            "type": "Rosso",
            "price": 24.00,
            "description": "Il re dei vitigni autoctoni molisani. Un rosso strutturato, elegante, con note di frutti di bosco, spezie e un finale balsamico. Affinato 12 mesi in barrique.",
            "grape": "100% Tintilia",
            "year": "2018",
            "alcohol": "14.5%",
            "temp": "16-18°C",
            "pairing": "Carni rosse, selvaggina, formaggi stagionati, piatti al tartufo.",
            "image": "/images/tintilia_bottle.png"
        },
        {
            "name": "Falanghina del Molise DOC",
            "type": "Bianco",
            "price": 18.00,
            "description": "Un bianco fresco e minerale, espressione autentica del territorio. Profumi di agrumi, fiori bianchi e mela verde. Al palato è sapido e persistente.",
            "grape": "100% Falanghina",
            "year": "2022",
            "alcohol": "13%",
            "temp": "10-12°C",
            "pairing": "Pesce alla griglia, crostacei, carni bianche, formaggi freschi.",
            "image": "/images/falanghina_bottle.png"
        },
        {
            "name": "Rosato del Molise DOC",
            "type": "Rosato",
            "price": 20.00,
            "description": "Un rosato vibrante e versatile. Colore rosa cerasuolo, profumi di fragola e rosa canina. Freschezza equilibrata e grande bevibilità.",
            "grape": "100% Montepulciano",
            "year": "2023",
            "alcohol": "13.5%",
            "temp": "10-12°C",
            "pairing": "Aperitivi, antipasti di salumi, pizza, zuppe di pesce.",
            "image": "/images/rosato_bottle.png"
        }
    ]

    print("Seeding products...")
    result = await products_collection.insert_many(products)
    print(f"Inserted {len(result.inserted_ids)} products successfully.")

if __name__ == "__main__":
    try:
        asyncio.run(seed_products())
    except Exception as e:
        traceback.print_exc()
