from docx import Document
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load document
document = Document("document.docx")

text = ""

for paragraph in document.paragraphs:
    if paragraph.text.strip():
        text += paragraph.text + "\n"

# Create chunks
words = text.split()

chunk_size = 100
chunks = []

for i in range(0, len(words), chunk_size):
    chunk = " ".join(words[i:i + chunk_size])
    chunks.append(chunk)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create document embeddings
embeddings = model.encode(chunks)
embeddings = np.array(embeddings).astype("float32")

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# User question
question = input("\nEnter your question: ")

# Convert question to embedding
question_embedding = model.encode([question])
question_embedding = np.array(question_embedding).astype("float32")

# Retrieve top 3 chunks
k = 6
distances, indices = index.search(question_embedding, k)

# Combine retrieved chunks
context = ""

for i in range(k):
    context += chunks[indices[0][i]] + "\n\n"

print("RETRIEVED CONTEXT:")
print(context)
from transformers import pipeline

# Load Qwen model
generator = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-0.5B-Instruct"
)

# Give retrieved context to the model
prompt = f"""
You are a document question-answering assistant.

Answer the question using ONLY the information provided in the context.

Rules:
- Use only information explicitly stated in the context.
- Do not use outside knowledge.
- Do not invent facts.
- Do not treat future enhancements or examples as current technologies.
- If a technology is mentioned as a future upgrade, do not list it as a currently used technology.
- Give a short, accurate answer.
- Do not repeat the question.

Context:
{context}

Question:
{question}

Answer:
"""
# Generate answer
result = generator(
    prompt,
    max_new_tokens=200
)

print("\nFINAL ANSWER:")
print(result[0]["generated_text"])