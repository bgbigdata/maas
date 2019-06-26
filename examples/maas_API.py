import json
import requests

def operateKey(url, userAddress, carKey, keyOperation):
    response = requests.post(url,
                             json.dumps({'userAddress':userAddress,
                                         'carKey':carKey,
                                         'operation':keyOperation}),
                                         headers={'Content-Type':'application/json'})
    print(response.status_code)
    if response.status_code == 200:
        print(response.json())
        return True
    return False
