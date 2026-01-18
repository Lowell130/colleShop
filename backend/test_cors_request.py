import requests

def test_cors():
    url = "http://localhost:8000/auth/login"
    headers = {
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "POST"
    }
    
    print(f"Testing OPTIONS {url}...")
    try:
        r = requests.options(url, headers=headers)
        print(f"OPTIONS Status: {r.status_code}")
        print("OPTIONS Headers:")
        for k, v in r.headers.items():
            print(f"  {k}: {v}")
            
        # Test POST
        print(f"\nTesting POST {url}...")
        data = {"username": "newadmin@colleshop.it", "password": "admin123"}
        r_post = requests.post(url, data=data, headers={"Origin": "http://localhost:3000"})
        print(f"POST Status: {r_post.status_code}")
        print("POST Headers:")
        for k, v in r_post.headers.items():
            print(f"  {k}: {v}")
        print(f"POST Body: {r_post.text[:200]}")
            
    except Exception as e:
        print(f"Request failed: {e}")

def test_cors_request_func():
    test_cors()

if __name__ == "__main__":
    test_cors_request_func()
