
url = 'http://localhost:5005/submit'
import requests
# data = {"orderid": 5, "sku": "fff", "qty": 20}
data = {"text": "Test problem ipsem", "category": "tests and fire"}

r = requests.post(url, json=data)

print(r.text)

# result invalid sku

