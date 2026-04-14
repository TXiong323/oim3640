import requests

# send first
response = requests.post(
    'https://oim.108122.xyz/message',
    json={'message': 'Hello from spark!'},
    headers={'X-Token': 'sparksprk'}
)

print(response.status_code)
print(response.text)

# then read again
data = requests.get('https://oim.108122.xyz/messages').json()
for msg in data:
    print(msg)