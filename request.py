import requests

url = 'http://127.0.0.1:5000/comment_suggestions'
data = {'url': 'https://www.instagram.com/p/C3sjNmliD3J/?igsh=YjZnMTRmN2VydHZv'}
response = requests.post(url, json=data)

print(response.json())
