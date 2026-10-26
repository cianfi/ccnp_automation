import os

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.responses.create(
    model="chatgpt-4o-latest",
    input=[
        {"role": "system", "content": "you are an egg"},
        {"role": "user", "content": "hello"},
    ],
)

print(response.output_text)
