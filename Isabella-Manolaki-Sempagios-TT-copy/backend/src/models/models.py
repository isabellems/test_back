import os
from dotenv import load_dotenv
import fastapi

from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

load_dotenv()

# 2️⃣ Get values from environment
endpoint = os.getenv("AZURE_ENDPOINT")
deployment = os.getenv("DEPLOYMENT")
subscription_key = os.getenv("AZURE_KEY")
api_version = os.getenv("API_VERSION")

embed_endpoint = os.getenv("EMBED_AZURE_ENDPOINT")
embed_deployment = os.getenv("EMBED_DEPLOYMENT")
embed_subscription_key = os.getenv("EMBED_AZURE_KEY")
embed_api_version = os.getenv("EMBED_API_VERSION")


llm = AzureChatOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    azure_deployment=deployment,
    api_key=subscription_key
)

embeddings = AzureOpenAIEmbeddings(
    api_version=embed_api_version,
    azure_endpoint=embed_endpoint,
    azure_deployment=embed_deployment,
    api_key=embed_subscription_key 
)

