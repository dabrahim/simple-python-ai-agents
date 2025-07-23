from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionToolParam
from tools import tools
import os

load_dotenv()
# TODO : Fix the mypy lint errors
api_key: str = os.getenv('OPENAI_API_KEY')
llm_model: str = os.getenv('LLM_MODEL')

client: OpenAI = OpenAI()


# TODO : Fix the mypy lint errors (commented)
def get_completion(chat_messages: list) -> ChatCompletion:
    completion = client.chat.completions.create(
        model=llm_model,
        messages=chat_messages,
        tools=tools  # type: ignore
    )
    return completion
