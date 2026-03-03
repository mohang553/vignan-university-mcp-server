import os
import uvicorn
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

# ==============================
# LOAD ENV VARIABLES
# ==============================
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME       = os.getenv("PINECONE_INDEX")

# ==============================
# INITIALIZE SERVICES
# ==============================
pc          = Pinecone(api_key=PINECONE_API_KEY)
index       = pc.Index(INDEX_NAME)
embed_model = SentenceTransformer("all-mpnet-base-v2")

app = FastAPI(title="Vignan University MCP Server")

# ==============================
# RETRIEVAL LOGIC
# ==============================
def retrieve(query: str, top_k: int = 5):
    query_embedding = embed_model.encode(query).tolist()

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        namespace="Vignan"
    )

    return [
        {
            "score":       match["score"],
            "text":        match["metadata"].get("text"),
            "source":      match["metadata"].get("source"),
            "chunk_index": match["metadata"].get("chunk_index"),
        }
        for match in results["matches"]
    ]


# ==============================
# LIST TOOLS  (GET /list-tools)
# ==============================
@app.get("/list-tools")
async def list_tools():
    return {
        "server": "VignanUniversity MCP Server",
        "tools": [
            {
                "name":        "VignanUniversity",
                "description": "Retrieve relevant knowledge chunks from the Vignan University namespace in Pinecone via semantic search.",
                "parameters": {
                    "query": {
                        "type":        "string",
                        "required":    True,
                        "description": "The search query to retrieve relevant information from Vignan University knowledge base.",
                    },
                    "top_k": {
                        "type":        "integer",
                        "required":    False,
                        "default":     5,
                        "description": "Number of top results to return.",
                    },
                },
            }
        ],
    }


# ==============================
# CALL TOOL  (POST /callTool)
# ==============================
class ToolCallRequest(BaseModel):
    name:      str
    arguments: Dict[str, Any]


@app.post("/callTool")
async def call_tool(request: ToolCallRequest):
    if request.name == "VignanUniversity":
        query = request.arguments.get("query")
        top_k = request.arguments.get("top_k", 5)
        if not query:
            raise HTTPException(status_code=400, detail="'query' argument is required.")
        return {"result": retrieve(query, top_k)}

    raise HTTPException(status_code=404, detail=f"Unknown tool: {request.name}")


# ==============================
# HEALTH CHECK
# ==============================
@app.get("/health")
async def health():
    return {"status": "healthy"}


# ==============================
# RUN SERVER
# ==============================
if __name__ == "__main__":
    print("🚀 Vignan MCP Server running on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)