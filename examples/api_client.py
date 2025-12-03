import requests
import json

API_URL = "http://your-server.com/api/v1/client/response"
API_KEY = "your_api_key"

def get_ai_response(client_id, message):
    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "client_id": client_id,
        "conversation": [
            {"role": "user", "content": message}
        ]
    }
    
    response = requests.post(API_URL, headers=headers, json=data)
    return response.json()

# 使用示例
if __name__ == "__main__":
    result = get_ai_response("client_djjo")
    print(result)