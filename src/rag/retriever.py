from src.rag.vectorstore import get_vectorstore

def retrieve_context(query):
    db = get_vectorstore()
    docs = db.similarity_search(query, k=3)
    return [d.page_content for d in docs]