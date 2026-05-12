#import openai
import google.generativeai as genai
import numpy as np
from numpy.linalg import norm

#client = openai.OpenAI(api_key="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")
#MODEL = "text-embedding-3-small"
genai.configure(api_key="AIzaSyDuyDLRUer8xHXDLv_ZWRU-dj94tApfCjo")
MODEL = "gemini-embedding-001"

# Prototype words to standardize emotional analysis
prototypes = {
    0: ["neutral", "unemotional", "apathetic", "indifferent", "dispassionate"],
    50: ["emotional", "feeling", "passionate", "moved", "stirred"],
    100: ["overwhelming", "consuming", "all-consuming", "devastating", "ecstatic"]
}

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

def get_emotional_intensity(input_word):
    """Projects word onto the pre-defined intensity scale"""
    word_vec = get_embedding(input_word)

    # Calculate cosine similarity to each intensity
    sim_to_zero = cosine_similarity(word_vec, scale_vectors[0])
    sim_to_fifty = cosine_similarity(word_vec, scale_vectors[50])
    sim_to_hundred = cosine_similarity(word_vec, scale_vectors[100])

    # Weighted scoring
    sum_sims = sim_to_hundred + sim_to_fifty + sim_to_zero
    return (0*sim_to_zero + 50*sim_to_fifty + 100*sim_to_hundred) / sum_sims
"""
test_words = ["apple", "bored", "annoyed", "catastrophic"]
print("\n--- Scoring Results ---")
for word in test_words:
    score = get_emotional_intensity(word)
    print(f"Word: '{word}' -> Emotional Intensity Score: {score:.1f}")
"""
# Testing prototype vector similarities
for intensity, words in prototypes.items():
    avg_vec = scale_vectors[intensity]
    print(f"\nIntensity {intensity} average vector:")
    for other_intensity, other_vec in scale_vectors.items():
        if other_intensity != intensity:
            sim = cosine_similarity(avg_vec, other_vec)
            print(f"  Similarity to {other_intensity}: {sim:.3f}")
