from docx import Document

document = Document("document.docx")

# 1. Get all text
text = ""

for paragraph in document.paragraphs:
    if paragraph.text.strip():
        text += paragraph.text + "\n"

# 2. Split text into chunks
words = text.split()

chunk_size = 100

chunks = []

for i in range(0, len(words), chunk_size):
    chunk = " ".join(words[i:i + chunk_size])
    chunks.append(chunk)

# 3. Display chunks
for i, chunk in enumerate(chunks):
    print("\n-----------------------------")
    print("CHUNK", i + 1)
    print("-----------------------------")
    print(chunk)