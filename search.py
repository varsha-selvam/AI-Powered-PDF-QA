from docx import Document
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# 1. Load document
document = Document("document.docx")

text = ""

for paragraph in document.paragraphs:
    if paragraph.text.strip():
        text += paragraph.text + "\n"

# 2. Create chunks
words = text.split()

chunk_size = 100
chunks = []

for i in range(0, len(words), chunk_size):
    chunk = " ".join(words[i:i + chunk_size])
    chunks.append(chunk)

# 3. Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 4. Create embeddings
embeddings = model.encode(chunks)

embeddings = np.array(embeddings).astype("float32")

# 5. Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

# 6. Ask a question
question = "What is the purpose of this project?"

# 7. Convert question into embedding
question_embedding = model.encode([question])
question_embedding = np.array(question_embedding).astype("float32")

# 8. Search FAISS
k = 3

distances, indices = index.search(question_embedding, k)

# 9. Display relevant chunks
print("\nQuestion:", question)

for i in range(k):
    print("\n-----------------------------")
    print("RESULT", i + 1)
    print("-----------------------------")
    print(chunks[indices[0][i]])
    print("Distance:", distances[0][i])