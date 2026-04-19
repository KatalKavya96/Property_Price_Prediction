from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

docs = [
    "High quality houses appreciate faster.",
    "Large living area increases property value.",
    "Newer homes have better resale potential.",
    "Investment depends on market demand.",
    "Always verify legal documents before buying.",
]

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = Chroma.from_texts(
    texts=docs,
    embedding=embedding,
    persist_directory="db",
)

print("RAG DB created")