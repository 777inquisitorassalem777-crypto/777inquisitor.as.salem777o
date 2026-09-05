import urllib.request, json
print(urllib.request.urlopen("http://localhost:8000/health").read().decode())
