import json
import os

from openai.types.chat import ChatCompletion, ChatCompletionMessageToolCall
from dotenv import load_dotenv
from openai.types.chat.chat_completion import Choice

from llm import get_completion
from tools import list_files, read_file, write_file, append_to_file, ask_for_clarification, submit_final_response, \
    tools_definition
from memory import Memory

load_dotenv()

MAX_ITERATIONS: int = int(os.getenv('MAX_ITERATIONS') or 10)
SYSTEM_PROMPT: str = read_file("system-prompt.md")

memory: Memory = Memory()
messages: list = memory.load_chat_history()

if len(messages) == 0:
    messages.append({
        "role": "system",
        "content": SYSTEM_PROMPT,
    })

functions: dict = {
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
    "append_to_file": append_to_file,
    "ask_for_clarification": ask_for_clarification,
    "submit_final_response": submit_final_response
}

message: str = input('What would you like to do? ')
# message: str = "What's inside my current folder?"

messages.append({
    "role": "user",
    "content": message,
})

iteration_count: int = 0

while True and iteration_count < MAX_ITERATIONS:
    iteration_count += 1

    # Call the llm and retrieve the next tool call
    completion: ChatCompletion = get_completion(messages, tools_definition)

    print(completion)

    first_completion_choice: Choice = completion.choices[0]

    # We parse the response to make sure it's a proper tool call
    if first_completion_choice.finish_reason == "tool_calls" and first_completion_choice.message.tool_calls:
        # We add the tool call to the messages history
        messages.append(completion.choices[0].message.to_dict())

        # We retrieve the tool name & arguments
        tool_call: ChatCompletionMessageToolCall = first_completion_choice.message.tool_calls[0]
        tool_name = tool_call.function.name
        tool_arguments = json.loads(tool_call.function.arguments)

        print(f"\n{"*" * 20}")
        print(f"Tool called: {tool_name}")

        # We call the tool and pass the arguments
        result = functions[tool_name](**tool_arguments)

        # We push the tool call response
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })

        memory.save_chat_history(messages)

        # Whe the LLM calls the 'submit_final_response', we exit the loop
        if tool_name == "submit_final_response":
            break

    else:
        print("Something went wrong. The agent didn't call a tool.")
        print(completion)
        break
        # print(json.dumps(completion.choices[0].message, indent=2))
