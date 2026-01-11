import faiss

# from langchain_community.document_loaders.url_selenium import SeleniumURLLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.docstore import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from src.models import embeddings
from langchain.tools import tool
from langchain_core.runnables import RunnableConfig
from langgraph.types import interrupt, Command
from src.store import *

urls = [
    'https://en.wikipedia.org/wiki/Rabobank'
]

docs = WebBaseLoader(web_path=urls[0]).load()
splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=100,
    chunk_overlap=50
)

all_splits = splitter.split_documents(docs)

embedding_size = len(embeddings.embed_query("Hello World"))
index = faiss.IndexFlatL2(embedding_size)
vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={}
)

vector_store.add_documents(all_splits)
retriever = vector_store.as_retriever()

@tool
def retrieve_bank_information(query: str):
    """Searches information matching a specific question about Rabobank
       by utilizing web results in the store.

       query: user's original query
    """
    docs = retriever.invoke(query)

    return "/n/n".join([doc.page_content for doc in docs])

@tool
def transaction_tool(config: RunnableConfig, iban: str, recipient_name: str, amount: float, description: str | None):
    """Submits a fund transaction into the system.

    Args:
        iban: Recipients IBAN
        recipient_name: Full name of the recipient
        amount: Amount of money to be transferred
        description: Optional description for the transaction
    """

    request = {
        "action": "transaction_tool",
        "args": {
            "iban": iban,
            "recipient_name": recipient_name,
            "amount": amount,
            "description": description
        }
    }

    response = interrupt(request)

    if response['type'] == 'edit':
        iban = response["args"]['iban']
        recipient_name = response["args"]['recipient_name']
        amount = response["args"]['amount']
        description = response["args"]['description']
    elif response['type'] == 'reject':
        return 'Transaction was cancelled'

    sender = config['configurable']['user_id']
    add_transaction(sender, iban, recipient_name, amount, description)
    return f'''Transaction was recorded with details: iban: {iban}, 
                recipient {recipient_name},
                amount {amount}
                description {description}'''