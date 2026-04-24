import requests

RERANK_URL = "http://10.176.64.152:11436/v1/rerank"
RERANK_MODEL = "bge-reranker-v2-m3"


def rerank(query: str, documents: list[str], top_n: int = 10):
    """对候选文档进行精排，返回排序后的 (index, score) 列表。"""
    if not documents:
        return []
    response = requests.post(RERANK_URL, json={
        "model": RERANK_MODEL,
        "query": query,
        "documents": documents,
        "top_n": top_n,
    }, timeout=30)
    response.raise_for_status()
    data = response.json()
    results = data.get("results", [])
    # 按 relevance_score 降序排列
    results.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
    return results
