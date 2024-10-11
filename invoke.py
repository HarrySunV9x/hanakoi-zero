import requests
import json

from rich import print

from chathistory import get_hana_chat
from config import llm_config
from prompt import hana_prompt, base_prompt, prompt_chat_hana

url = llm_config.get("OLLAMA_URL")


def chat_invoke(speaker, input_prompt, new_context_id=None, model="llama3.1"):
    hana_chat = get_hana_chat()
    prompt_string = ''
    chat_history = ''
    context_id = None
    if new_context_id is None:
        context_id = hana_chat.get_max_context_id() + 1
    else:
        context_id = new_context_id
    print(context_id)
    if hana_chat.get_history_by_context_id(context_id) is not None:
        chat_history = hana_chat.get_conversation(context_id)
    else:
        chat_history = ''

    prompt_string = prompt_chat_hana.format(speaker=speaker, history=chat_history, prompt=input_prompt)
    print(":smiley:[bold magenta]prompt_string: [/bold magenta]", prompt_string)
    chat_history += f"\n{speaker}: {input_prompt}"

    payload = {
        "model": model,
        "prompt": prompt_string,
        "stream": True
    }

    response = requests.post(url, json=payload)
    # 手动解析返回的多行 JSON 数据
    results = ""
    for line in response.text.splitlines():
        try:
            json_obj = json.loads(line)
            results += json_obj["response"]
        except json.JSONDecodeError:
            return {"error": "Failed to decode JSON response", "invalid_line": line}

    chat_history += f"\nhana: {results}"

    update_id = hana_chat.get_history_by_context_id(context_id)
    if update_id is not None:
        hana_chat.update_record(update_id, chat_history)
    else:
        hana_chat.write_record(chat_history, context_id)

    return results


def normal_invoke(speaker, prompt_type, model, input_prompt):
    prompt_string = ''
    if prompt_type == "hana":
        prompt_string = hana_prompt.format(speaker=speaker, prompt=input_prompt)
    elif prompt_type == "base":
        prompt_string = base_prompt + input_prompt

    payload = {
        "model": model,
        "prompt": prompt_string,
        "stream": True
    }
    response = requests.post(url, json=payload)
    # 手动解析返回的多行 JSON 数据
    results = ""
    for line in response.text.splitlines():
        try:
            json_obj = json.loads(line)
            results += json_obj["response"]
        except json.JSONDecodeError:
            return {"error": "Failed to decode JSON response", "invalid_line": line}

    return results
