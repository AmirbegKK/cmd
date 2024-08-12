import os

from mistralai import Mistral
import numpy as np
import time
import faiss
from dotenv import load_dotenv

load_dotenv('.env')
client = Mistral(api_key=os.getenv('MISTRAL_API_KEY'))

with open('faq.txt', 'r') as f:
    text = f.read()

chunk_size = 2048
chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def get_text_embedding(chunk):
    embeddings_batch_response = client.embeddings.create(
          model="mistral-embed",
          inputs=chunk
      )
    time.sleep(1.7)
    return embeddings_batch_response.data[0].embedding


text_embeddings = np.array([get_text_embedding(chunk) for chunk in chunks])
d = text_embeddings.shape[1]
index = faiss.IndexFlatL2(d)
index.add(text_embeddings)


async def run_mistral(user_message, model="mistral-large-latest"):
    question_embeddings = np.array([get_text_embedding(user_message)])
    Dist, Ind = index.search(question_embeddings, k=2)  # distance, index
    retrieved_chunk = [chunks[i] for i in Ind.tolist()[0]]
    prompt = f"""
    Context information is below.
    ---------------------
    {retrieved_chunk}
    ---------------------
    You are a bot assistant.
    Given the context information and not prior knowledge, answer the query on question language.
    Query: {user_message}
    Answer:
    """
    messages = [
        {
            "role": "user", "content": prompt
        }
    ]
    chat_response = await client.chat.complete_async(
        model=model,
        messages=messages
    )
    return chat_response.choices[0].message.content


