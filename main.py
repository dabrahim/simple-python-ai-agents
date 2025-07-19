from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI()
response = client.responses.create(
    model="gpt-4.1",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)