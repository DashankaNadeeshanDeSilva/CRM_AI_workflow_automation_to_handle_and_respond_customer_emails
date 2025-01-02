import chromadb

class Knowledge_Base():
    def __init__(self, db_path="app/knowledge_base/vector_db/"):
        self.db_path = db_path
        self.client = chromadb.PersistentClient(path=self.db_path)

    def get_collection(self, collection_name="company_knowledge_base"):
        collection = self.client.get_collection(collection_name)
        return collection # ChromaDB collection object.
    
    def create_collection(self, collection_name="company_knowledge_base"):
        collection = self.client.get_or_create_collection(name=collection_name)
        return collection # ChromaDB collection object.

    def add_to_collection(self, collection, documents):
        '''documnets format: {"document_id":"document text"}
        '''
        if not isinstance(documents, dict):
                raise ValueError("Documents must be a dictionary with format {'document_id': 'document text'}.")
        
        collection.add(
            documents=list(documents.values()),
            ids=list(documents.keys())
        )

    def query(self, collection, query, n_results=2):
        results_raw = collection.query(query_texts=[query], n_results=n_results)
        results = "".join(str(result) for result in results_raw["documents"][0])
        return results


if __name__ == "__main__":
    ## test script ##
    # init knowledge base
    knowledge_base = Knowledge_Base()
    # get collection
    knowledge_base_collection = knowledge_base.get_collection()
    # query collection
    test_query = "I bought a TV last week and now it is not working. Since it is in warranty period, I would like to get it repaired or replace for a new one."
    context = knowledge_base.query(collection=knowledge_base_collection, query=test_query)
    print(context)
     
     