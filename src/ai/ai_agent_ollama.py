import ollama

response = ollama.chat(
    model="llama3.2",
    messages=(
        {"role": "system", "content": "you are a network engineer"},
        {"role": "user", "content": "What is IPv4"},
    ),
)

print(response.message.content)
