import requests
import numpy as np
from config import DASHSCOPE_BASE_URL, DASHSCOPE_API_KEY, EMBEDDING_MODEL

URL = f"{DASHSCOPE_BASE_URL}/embeddings"

sentences = [
    "What is the capital of France?",
    "The capital of Brazil is Brasilia.",
    "The capital of France is Paris.",
    "Horses and cows are both animals",
]

response = requests.post(URL, json={
    "model": EMBEDDING_MODEL,
    "input": sentences,
}, headers={
    "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
    "Content-Type": "application/json",
}).json()  # 将input中的每条文本转换为向量

for data in response["data"]:
    print(len(data["embedding"]))  # embedding是第i条文本的向量，这里打印向量维度
print()

embeddings = [np.array(data["embedding"]) for data in response["data"]]

for i in range(0, 1):
    for j in range(1, 4):
        print(sentences[i])
        print(sentences[j])
        print('distance:', np.sum((embeddings[i] - embeddings[j])**2))
        print()