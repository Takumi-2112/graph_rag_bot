import os
import asyncio
import httpx  # Use httpx for asynchronous requests
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from config import DEPLOYMENT_NAME, DEPLOYMENT_ENDPOINT

# Set environment variables for your endpoint and deployment name
endpoint = DEPLOYMENT_ENDPOINT
deployment = DEPLOYMENT_NAME

# Initialize Azure OpenAI Service client with Entra ID authentication
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider,
    api_version="2024-05-01-preview",  # Make sure this is the latest API version
)

# Function to send query to FastAPI server (server.py)
async def query_fastapi(gremlin_query):
    api_url = "http://localhost:8000/query"  # This points to FastAPI locally; change if deployed to Azure
    async with httpx.AsyncClient() as client:
        response = await client.post(api_url, json={"query": gremlin_query})
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to get results from API"}

# Define generate_and_query as async
async def generate_and_query():
    # Define the conversation (prompt) for GPT-4-turbo-16k
    chat_prompt = [
        {
            "role": "system",
            "content": "You are an expert at writing Gremlin queries for Azure Cosmos DB Graph that also uses the groovy syntax.\n\nThe schema is:\n\n  - Vertex (node) labels: Customers, SalesTransaction, Products, Pillars, Dates\n\n  - Edges (relationships, links): Customer -[CUSTOMER_TRANSACTION]->SalesTransaction, Pillar -[PILLAR_FROM_TRANSACTION]->SalesTransaction, Product -[PRODUCT_FROM_TRANSACTION]->SalesTransaction, Date -[TRANSACTION_DATE]->SalesTransaction\n\n  - The SalesTransaction Table has properties: sales_transaction_key,date_key,customer_key,pillar_key,product_key,dollar_cost,dollar_rev,dollar_profit,quantity\n\n  - The Customer Table has properties: customer_key,customer_name,location\n\n- The Pillar Table has properties: pillar_key,pillar_name\n\n- The Product Table has properties: product_key,product_name,manufacturer\n\n- The Date Table has properties: date_key,date_of_day,day,month,month_number,year\n\nBased on the question below, please return a valid Gremlin query for Azure Cosmos DB Graph that also uses the groovy syntax:\n\n\"Which pi