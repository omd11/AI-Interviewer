from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model = "gpt-4o-mini"
    input= userInput
    )

print(response.output_text)