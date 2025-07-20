from dotenv import load_dotenv
from openai import OpenAI
import os

from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI()


def get_completion(chat_messages: list) -> str:
    completion = client.chat.completions.create(
        model="gpt-4.1",
        messages=chat_messages,
    )
    return completion.choices[0].message.content


messages = [
    ChatCompletionSystemMessageParam(
        content="You you are a helpful assistant named Jeff made by The Agent Forge.",
        role="system"
    ),
    ChatCompletionUserMessageParam(
        role="user",
        content="Who are you?",
    )
]

print(
    get_completion(messages)
)
