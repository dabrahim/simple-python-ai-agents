from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionToolParam
from typing import List, Dict
import os

load_dotenv()

api_key: str | None = os.getenv('OPENAI_API_KEY')
llm_model: str | None = os.getenv('OPEN_AI_MODEL_NAME')

client: OpenAI = OpenAI()


# TODO : Fix the mypy lint errors
def get_completion(chat_messages: list, tools: List[Dict]) -> ChatCompletion:
    if api_key is None or llm_model is None:
        raise Exception("API key and model name are required")

    completion = client.chat.completions.create(
        model=llm_model,
        messages=chat_messages,
        tools=tools  # type: ignore
    )
    return completion
