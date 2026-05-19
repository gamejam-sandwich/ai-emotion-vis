#import openai
import google.generativeai as genai
import numpy as np
import streamlit as st
import os
from dotenv import load_dotenv
from numpy.linalg import norm


#client = openai.OpenAI(api_key="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")
#MODEL = "text-embedding-3-small"
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-embedding-001"

# Prototype words to standardize emotional analysis
prototypes = {
    0: ["table", "walk", "paper", "number", "rock"],
    50: ["touched", "concerned", "affected", "moved", "unsettled"],
    100: ["overwhelming", "consuming", "devastating", "ecstatic", "anguish"]
}

@st.cache_data
def get_embedding(text):
    """Retrieves vector embedding of the input text"""
    #response = client.embeddings.create(input=text, model=MODEL)
    #return np.array(response.data[0].embedding)
    result = genai.embed_content(model=MODEL, content=text, task_type="semantic_similarity")
    return np.array(result['embedding'])

scale_vectors = {}
for intensity, words in prototypes.items():
    vectors = []
    for w in words:
        # Get embedding of each word at specified intensity level
        vectors.append(get_embedding(w))
    # Average the vectors to create one vector for this intensity
    scale_vectors[intensity] = np.mean(vectors, axis=0)

def cosine_similarity(a, b):
    """Calculates cosine similarity between two points"""
    # (Dot product) divided by (Euclidean norm of A and B)
    return np.dot(a, b) / (norm(a) * norm(b))

axis_vector = scale_vectors[100] - scale_vectors[0]
def get_emotional_intensity(input_word):
    """Projects word onto the 0-->100 emotion axis"""
    word_vec = get_embedding(input_word)
    relative_word = word_vec - scale_vectors[0]
    # Scalar projection onto axis
    projection = np.dot(relative_word, axis_vector) / np.dot(axis_vector, axis_vector)
    score = np.clip(projection, 0, 1) * 100
    return float(score)

# Validation — run this once to sanity-check
print("Midpoint anchor should project near 50:")
mid_proj = get_emotional_intensity("emotional")  # one of your 50-prototypes
print(f"  'emotional' → {mid_proj:.1f}")

print("\nTest words:")
for w in ["apple", "bored", "sad", "furious", "devastating"]:
    print(f"  '{w}' → {get_emotional_intensity(w):.1f}")
