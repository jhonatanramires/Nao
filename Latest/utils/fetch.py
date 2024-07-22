import requests
def fetch(path,debug):
    req = requests.get(path)
    response = req.json()
    return response