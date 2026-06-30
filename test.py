from groq import Groq

client = Groq(api_key="your_key")

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user",
         "content": "Create roadmap for becoming Data Scientist"}
    ]
)

print(response.choices[0].message.content)