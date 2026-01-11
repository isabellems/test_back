import os
from dotenv import load_dotenv

from typing import Literal
from src.agents import agent
from langchain.messages import HumanMessage

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from pydantic import BaseModel, Field
from uuid import uuid4
from langgraph.types import Command
from src.agents import *


app = FastAPI(title='My Chatbot app')

class Message(BaseModel):
    input: str
    user_id: str = Field(default_factory = lambda: str(uuid4()))
    thread_id: str = Field(default_factory = lambda: str(uuid4()))

class Decision(BaseModel):
    type: Literal['approve', 'reject', 'edit']
    # args: dict | None
    user_id: str = Field(default_factory = lambda: str(uuid4()))
    thread_id: str = Field(default_factory = lambda: str(uuid4())) 

@app.get('/')
def landing():
    return """Welcome to my chatbot app! Let me know what you want to talk about today"""

@app.post('/chat')
def chat(message: Message):
    config = {"configurable": {"thread_id": message.thread_id, "user_id": message.user_id}}
    try:
        res = agent.invoke({"messages": [HumanMessage(message.input)]}, config)
        if "__interrupt__" in res:
            inter_ = res['__interrupt__'][0].value
            return JSONResponse(content={'chatbot_response': '', 
                                         'interrupt': {
                                            'action': inter_['action'],
                                            'args': inter_['args']
                                         },
                                        'thread_id': message.thread_id,
                                        'user_id': message.thread_id
            })
        else:
            return JSONResponse(content={'chatbot_response': res['messages'][-1].content,
                                        'thread_id': message.thread_id,
                                        'user_id': message.thread_id})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": e, 'thread_id': message.thread_id,
                                        'user_id': message.thread_id})


@app.post('/interrupt')
def interrupt_decition(decision: Decision):
    config = {"configurable": {"thread_id": decision.thread_id, "user_id": decision.user_id}}
    try:
        if decision.type == 'edit':
            # input = Command(resume={"type": decision.type, "args": decision.args})
            input = Command(resume={"type": decision.type, "args": {}})
        else:
            input = Command(resume={"type": decision.type})
        
        res = agent.invoke(input, config)
        return JSONResponse(content={'chatbot_response': res['messages'][-1].content,
                                        'thread_id': decision.thread_id,
                                        'user_id': decision.thread_id})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": e, 'thread_id': decision.thread_id,
                                        'user_id': decision.thread_id})

