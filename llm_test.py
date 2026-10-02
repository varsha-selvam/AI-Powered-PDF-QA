from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-0.5B-Instruct"
)

result = generator(
    "What is the purpose of this project?",
    max_new_tokens=100
)

print(result[0]["generated_text"])