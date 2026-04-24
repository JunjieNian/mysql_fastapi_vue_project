import requests
import json
from config import DASHSCOPE_BASE_URL, DASHSCOPE_API_KEY, RERANK_MODEL

URL = f"{DASHSCOPE_BASE_URL}/rerank"

response = requests.post(URL, json={
    "model": RERANK_MODEL,
    "query": "What is the capital of France?",
    "documents": [
        "The capital of Brazil is Brasilia.",
        "The capital of France is Paris.",
        "Horses and cows are both animals",
    ],
    "top_n": 2,
}, headers={
    "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
    "Content-Type": "application/json",
})  # 从documents中查找与query最相关的top_n条文本

if response.status_code == 200:
    print("Request successful!")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)