import json
import os

from openai.types.chat import ChatCompletion, ChatCompletionMessageToolCall
from dotenv import load_dotenv

from llm import get_completion
from tools import list_files, read_file, write_file, append_to_file, ask_for_clarification, submit_final_response

load_dotenv()

MAX_ITERATIONS: int = int(os.getenv('MAX_ITERATIONS') or 10)
SYSTEM_PROMPT: str = read_file("system-prompt.md")

messages: list = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT,
    },
]

functions: dict = {
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
    "append_to_file": append_to_file,
    "ask_for_clarification": ask_for_clarification,
    "submit_final_response": submit_final_response
}

message: str = input('What would you like to do? ')
# message: str = "Create a file for me to store my todos in markdown"
messages.append({
    "role": "user",
    "content": message,
})

iteration_count: int = 0

while True and iteration_count < MAX_ITERATIONS:
    iteration_count += 1

    # Call the llm and retrieve the next tool call
    completion: ChatCompletion = get_completion(messages)

    # Wa parse the response to make sure it's a proper tool call
    if completion.choices[0].finish_reason == "tool_calls" and completion.choices[0].message.tool_calls:
        tool_call: ChatCompletionMessageToolCall = completion.choices[0].message.tool_calls[0]
        tool_name = tool_call.function.name
        tool_arguments = json.loads(tool_call.function.arguments)

        print(f"\n{"*" * 20}")
        print(f"Tool called: {tool_name}")

        # We call the tool and pass the arguments
        result = functions[tool_name](**tool_arguments)

        # Whe the LLM calls the 'submit_final_response', we exit the loop
        if tool_name == "submit_final_response":
            break

        # print(json.dumps(dict(toolCall), indent=4)) # error
        # print(json.dumps(result, indent=4))

        # We add the tool call to the messages history
        messages.append(completion.choices[0].message)

        # We push the tool call response
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })

    else:
        print("Something went wrong. The agent didn't call a tool.")
        print(completion)
        break
        # print(json.dumps(completion.choices[0].message, indent=2))

    # pprint(dict(completion.choices[0].message))
