import chromadb


# init
# add docs

# setup vector db
client = chromadb.Client()
collection = client.get_or_create_collection("company_knowledge_base")
# Setup Vector DB (ChromaDB) for Context Retrieval
# Assume the collection is already populated with relevant documents

# Add documents to the collection if its not populated
collection.add(
    documents=[
        "Berlin is the capital of Germany.",
        "Paris is the capital of France.",
        "Rome is the capital of Italy."
    ],
    metadatas=[
        {"source": "european_cities"},
        {"source": "european_cities"},
        {"source": "european_cities"}
    ],
    ids=["doc1", "doc2", "doc3"]
)

# Step 2: Define a Retrieval Function
def retrieve_context(question):
    # Use the vector database to find relevant documents
    results = collection.query(
        query_texts=[question],
        n_results=2
    )
    # Combine retrieved documents into a single context
    context = " ".join([doc for doc in results["documents"]])
    return context


client = chromadb.Client(chromadb.PersistentClientSettings(
    path="knowledge_base/vector_db"
))
collection = client.get_or_create_collection("knowledge_base")