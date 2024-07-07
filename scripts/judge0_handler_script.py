import requests

url = 'http://192.168.0.220:2358/'

myobj =   {
            "source_code": "print(\"hello world\")",
            "language_id": 71, # 50 for C, 73 rust, 55 commonl isp
            # "stdin": "world"
           }

x = requests.post((url + 'submissions/?base64_encoded=false&wait=false'), json = myobj)

# Parse the JSON response
response_data = x.json()

# Extract the token from the response
token = response_data.get('token')  # Replace 'token' with the actual key in your JSON response

print(f"token {token}")

import time

# Sleep for 2 seconds
time.sleep(2)


print ("After making request, check that hash for submission stdout")

base64_encoded = False
# fields = 'stdout,stderr,status_id,language_id'
# &fields={fields}

# Send a GET request
response = requests.get((url + f'/submissions/{token}?base64_encoded={base64_encoded}'))
print("url: " + (url + f'submissions/{token}?base64_encoded={base64_encoded}'))

print(response.text)

print(response.status_code)


