import requests
import json

url = "https://api.doppio.sh/v1/render/pdf/sync"

payload = json.dumps({
  "page": {
    "pdf": {
      "printBackground": True
    },
    "goto": {
      "url": "C:/sudcraultra/informe_alumnos/MAT1111-2024001-0_24086890.html"
    }
  }
})
headers = {
  'Authorization': 'Bearer 79868251ada2bebe6f2702c9',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)