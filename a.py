from mistralai.client import Mistral
from dotenv import load_dotenv
import os

load_dotenv()

client = Mistral(
    api_key=os.environ["MISTRAL_API_KEY"]
)

response = client.chat.complete(
    model="mistral-small-latest",
    messages=[
        {
            "role": "user",
            "content": "Say two unknown fact about cricket."
        }
    ]
)

print(response.choices[0].message.content)