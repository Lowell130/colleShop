import requests
import sys

print("Starting check...", flush=True)
try:
    response = requests.get("http://127.0.0.1:8000/products/", timeout=5)
    print(f"Status: {response.status_code}", flush=True)
    if response.status_code == 200:
        products = response.json()
        print(f"Count: {len(products)}", flush=True)
        if products:
            print("First product keys:", list(products[0].keys()), flush=True)
            print("First product 'id':", products[0].get("id"), flush=True)
            print("First product '_id':", products[0].get("_id"), flush=True)
        else:
            print("No products found.", flush=True)
    else:
        print(f"Error text: {response.text}", flush=True)
except Exception as e:
    print(f"Exception: {e}", flush=True)
