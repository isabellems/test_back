import gradio as gr
import requests
import json
import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
CHAT_ENDPOINT_START=os.getenv('CHAT_ENDPOINT_START')
CHAT_ENDPOINT_CHAT=os.getenv('CHAT_ENDPOINT_CHAT')
CHAT_ENDPOINT_INTER=os.getenv('CHAT_ENDPOINT_INTER')

headers = {
    "Content-Type": "application/json",
}

class MyChatState:
    user_id: str = None
    thread_id: str = None
    args: dict
    interrupt: bool = False

my_state = MyChatState()

def echo(message, history):
    body = {
        "input": message
    }

    if my_state.user_id is not None:
        body["user_id"] = my_state.user_id
        body["thread_id"] = my_state.thread_id

    response = requests.post(url=CHAT_ENDPOINT_CHAT, json=body, headers=headers)
    if response.status_code == 200:
        res = response.json()
        if my_state.user_id is None:
            my_state.user_id = res['user_id']
            my_state.thread_id = res['thread_id']

        if res.get('interrupt', False):

            my_state.args = res['interrupt']['args']
            my_state.interrupt = True
            return f"""
                In order to process your request
                I need confirmation about the following data:

                {json.dumps(res['interrupt']['args'], indent=4)}
                
            """
        else:
            print('here')
            if my_state.interrupt:
                body = {
                    "type": message,
                    # "args": "",
                    "user_id": my_state.user_id,
                    "thread_id": my_state.thread_id
                }
                print(body)

                res = requests.post(url=CHAT_ENDPOINT_INTER, json=body, headers=headers) 

            my_state.interrupt = False
        
        print(res)
        res = res['chatbot_response']
    else:
        return 'Error!'
    return res

demo = gr.ChatInterface(fn=echo, title="RaboChat")
demo.launch()
# demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 8000)))

