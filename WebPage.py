import requests

# Make a GET request
response = requests.get('https://api.example.com/data')
print(response.status_code)  # Get the HTTP status code
print(response.json())  # Get the response data in JSON format

# Make a POST request with JSON payload
payload = {'key1': 'value1', 'key2': 'value2'}
response = requests.post('https://api.example.com/submit', json=payload)
print(response.status_code)  # Get the HTTP status code
print(response.json())  # Get the response data in JSON format
