from docx import Document
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# 1. Load the document
document = Document("document.docx")

text = ""

for paragraph in document.paragraphs:
    if paragraph.text.strip():
        text += paragraph.text + "\n"

# 2. Split document into chunks
words = text.split()

chunk_size = 100
chunks = []

for i in range(0, len(words), chunk_size):
    chunk = " ".join(words[i:i + chunk_size])
    chunks.append(chunk)

# 3. Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 4. Create embeddings for all chunks
embeddings = model.encode(chunks)

# 5. Display results
print("Number of chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)
print("First chunk embedding:")
print(embeddings[0])
# 6. Convert embeddings to float32
embeddings = np.array(embeddings).astype("float32")

# 7. Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

# 8. Add embeddings to FAISS
index.add(embeddings)

print("FAISS index created!")
print("Number of vectors:", index.ntotal)