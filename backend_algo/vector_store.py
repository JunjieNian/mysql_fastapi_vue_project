import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from config import DASHSCOPE_BASE_URL, DASHSCOPE_API_KEY, EMBEDDING_MODEL

CHROMA_HOST = "localhost"
CHROMA_PORT = 8002
COLLECTION_NAME = "papers"

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=DASHSCOPE_API_KEY,
    api_base=DASHSCOPE_BASE_URL,
    model_name=EMBEDDING_MODEL,
)

client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)


def get_collection():
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=openai_ef,
    )


def index_papers(papers: list[dict]):
    """批量索引论文到 ChromaDB。
    papers: list of dict with keys: id, title, abstract, keywords
    """
    collection = get_collection()
    ids = [str(p["id"]) for p in papers]
    documents = [
        f"{p['title']}. {p['abstract']}. {p.get('keywords', '')}"
        for p in papers
    ]
    collection.upsert(ids=ids, documents=documents)
    return len(ids)


def search(query: str, top_k: int = 20):
    """向量检索，返回 paper id 列表和对应文档。"""
    collection = get_collection()
    results = collection.query(query_texts=[query], n_results=top_k)
    ids = results["ids"][0] if results["ids"] else []
    documents = results["documents"][0] if results["documents"] else []
    return ids, documents


def get_embeddings_by_ids(paper_ids: list[str]):
    """获取指定论文的 embedding 向量。"""
    collection = get_collection()
    results = collection.get(ids=paper_ids, include=["embeddings"])
    return results.get("embeddings", [])
