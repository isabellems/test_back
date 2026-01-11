
from langchain.messages import HumanMessage, SystemMessage
from langgraph.graph import MessagesState, StateGraph, START, END
from typing import Literal
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from src.models import llm
from src.tools import *
from src.templates import *


class ChatBotState(MessagesState):
    intent: Literal["faq", "transaction", "other"]
    user_id: str
    context_data: dict | None
    user_prompt: str
    # transaction = 


def classify_intent(state: ChatBotState):
    query = state["messages"][-1].content

    prompt = classify_intent_prompt.format(query=query)
    response = llm.invoke([SystemMessage(prompt), HumanMessage(query)])
    print(response)
    intent = response.content

    return {"messages": [response], "intent": intent, "user_prompt": query}

def answer_question(state: ChatBotState):
    context_ = state["messages"][-1].content
    prompt = answer_question_prompt.format(context=context_)
    # response = llm.bind_tools([retrieve_bank_information]).invoke([SystemMessage(prompt), HumanMessage(state["user_prompt"])])
    response = llm.bind_tools([retrieve_bank_information]).invoke([SystemMessage(prompt)] + state['messages'])
    print(response)
    return {"messages": [response]}

# def pii_indentifier(state: ChatBotState):
#     prompt = pii_indentifier,

def perform_transaction(state: ChatBotState):
    print("HEREEEE!!!!")
    prompt = perform_transaction_prompt  
    response = llm.bind_tools([transaction_tool]).invoke([SystemMessage(prompt)] + state['messages'])
    return {"messages": [response]}

def intent_condition(state: ChatBotState) -> str:
    if state["intent"] == "faq":
        return "answer_question"
    elif state["intent"] == "transaction":
        return "perform_transaction"
    else:
        return "answer_question"
        

builder = StateGraph(ChatBotState)
builder.add_node(classify_intent)
builder.add_node(answer_question)
builder.add_node(perform_transaction)
builder.add_node('retriever', ToolNode([retrieve_bank_information]))
builder.add_node('transaction', ToolNode([transaction_tool]))

builder.add_edge(START, "classify_intent")
builder.add_conditional_edges(
    "classify_intent",
    intent_condition
)
# builder.add_edge("classify_intent", "answer_question")
builder.add_conditional_edges(
    "answer_question",
    tools_condition,
    {
        'tools': "retriever",
        "__end__": END
    }
)
builder.add_conditional_edges(
    "perform_transaction",
    tools_condition,
    {
        'tools': "transaction",
        "__end__": END
    }
)
builder.add_edge("retriever", "answer_question")
builder.add_edge("transaction", "perform_transaction")

agent = builder.compile(checkpointer=InMemorySaver()) 