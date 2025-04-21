from openai import OpenAI
import interface

client = OpenAI()

response = client.responses.create(
    model = "gpt-4o-mini",
    input= "placeholder"
    )

print(response.output_text)


main = interface.MainWindow()
main.show()

class Interviewer:
    def __init__(self, role: str, ):
        self.client = OpenAI()
        self.response = None
        self.role = role
        self.personality = str

    def ask_question(self, question):
        self.response = self.client.responses.create(
            model="gpt-4o-mini",
            input=question
        )
        return self.response.output_text