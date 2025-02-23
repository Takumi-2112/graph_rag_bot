from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from query_cosmos_client import run_gremlin_query  # Import your query function

app = FastAPI()

# Define request body schema
class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_graph(request: QueryRequest):
    """API endpoint to execute a Gremlin query."""
    result = await run_gremlin_query(request.query)  # Ensure run_gremlin_query is async
    if "error" in result:
        raise HTTPException(status_code=500, detail=r