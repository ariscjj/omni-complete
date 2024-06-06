import openai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Initialize OpenAI API
openai.api_key = 'your-api-key-here'

# Example storage for precomputed embeddings
query_embedding_store = {} 

# The first is a list of embeddings values, the second is the number of hits 
# For example: 
# Dictionary Datastructure: key three values 
# Value 1; Embeddings 
# Value 2: Completion 
# Value 3: Hit Count 
# {"What is the capital of France?": ([0.123, 0.234, ...], 10)} 
# {"What is": {"embeddings": [,....] "completions": {"javascript" : 3, "UnoCSS": 4}}} 

# Function to get GPT-3 embeddings
def get_gpt3_embeddings(text, model="text-embedding-ada-002"):
    response = openai.Embedding.create(input=text, model=model)
    embeddings = response['data'][0]['embedding']
    return embeddings

# Function to find the closest matching query
def find_closest_query(new_query, threshold=0.8):
    new_query_embedding = get_gpt3_embeddings(new_query)
    # list comprehension to only get embeddings for each query  
    # stored_embeddings = list(query_embedding_store.values())
    stored_embeddings = [value["embeddings"] for value in data.values()]  
    # queries = list(query_embedding_store.keys())

    # Calculate similarity
    similarities = cosine_similarity([new_query_embedding], stored_embeddings)
    max_similarity = np.max(similarities)
    max_index = np.argmax(similarities)
    max_embedding = stored_embeddings[max_index]

    # print(queries[max_index])
    if max_similarity >= threshold:
        # returns query with max_index 
        return queries[max_index], max_embedding  
    else:
        return None, max_embedding  

# Function to add a new query and embedding
def add_new_query(new_query, new_completion, 1):
    embedding = get_gpt3_embeddings(new_query)
    query_embedding_store[new_query]["embedding"] = embedding
    query_embedding_store[new_query]["completions"][new_completion] = 1 
#     [embedding, new_completion, 1)
    return embedding

# Example usage
new_query = "What's the capital of France?"

matched_query, similarity = find_closest_query(new_query)

if matched_query:
    print(f"New query matches with '{matched_query}' with similarity {similarity}")
else:
    new_embedding = add_new_query(new_query)
    print(f"New query '{new_query}' added with embedding {new_embedding[:5]}...")  # Print first 5 values for brevity
