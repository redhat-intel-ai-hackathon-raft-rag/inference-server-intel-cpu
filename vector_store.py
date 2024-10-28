import numpy as np
import faiss

class PreviousOutputVectorStore:
    def __init__(self):
        self.index = faiss.IndexFlatL2(768)
        self.input_output_cache = {}
        self.index_to_input_cache = {}
    
    def add_vector(self, vector, input_text, output_text):
        self.index.add(vector)
        self.index_to_input_cache[len(self.index_to_input_cache)] = input_text
        self.input_output_cache[input_text] = output_text
        
    def search_vector(self, vector, k=1):
        return self.index.search(vector, k)
    
    def get_input_text(self, index):
        return self.index_to_input_cache.get(index)

    def get_output_text(self, input_text):
        return self.input_output_cache.get(input_text)

class RaftStore:
    def __init__(self, dimension):
        pass
        
    def add_vector(self, vector):
        pass
        
    def search_vector(self, vector, k=1):
        pass
    
    def _load_data(self, data):
        self.index.add(data)

if __name__ == "__main__":
    # Create a PreviousOutputVectorStore object
    previous_output_vector_store = PreviousOutputVectorStore()
    from embedding import vectorize_input
    # Vectorize the input
    # Add the vector to the PreviousOutputVectorStore
    vector = vectorize_input(" #Question: What is the meaning of life?")
    previous_output_vector_store.add_vector(vector, " #Question: What is the meaning of life?", "The meaning of life is to be happy.")
    vector = vectorize_input(" #Question: What are the benefits of exercise?")
    previous_output_vector_store.add_vector(vector, " #Question: What are the benefits of exercise?", "Exercise has many benefits.")
    vector = vectorize_input(" #Question: What is the meaning of purpose?")
    previous_output_vector_store.add_vector(vector, " #Question: What is the meaning of purpose?", "The meaning of purpose is to have a goal.")
    # Search for the vector in the PreviousOutputVectorStore
    distance, index = previous_output_vector_store.search_vector(vector)
    print(vector in previous_output_vector_store.index)
    input_text = previous_output_vector_store.get_input_text(index[0][0])
    print(input_text)
    output_text = previous_output_vector_store.get_output_text(input_text)
    print(output_text)