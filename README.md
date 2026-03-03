# Vignan University MCP Server

A FastAPI-based Model Context Protocol (MCP) server that enables semantic search over the Vignan University knowledge base using Pinecone vector storage and Sentence Transformers.

---

## Overview

This server exposes a simple tool interface that allows clients to retrieve semantically relevant chunks of information from the Vignan University namespace stored in Pinecone. It uses the `all-MiniLM-L6-v2` sentence transformer model to embed queries and perform similarity search.

---

## Prerequisites

- Python 3.8+
- A [Pinecone](https://www.pinecone.io/) account with an index populated under the `Vignan` namespace
- The index must use 384-dimensional vectors (matching `all-MiniLM-L6-v2` output)

---

## Installation

1. **Clone the repository** and navigate to the project directory.

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** by creating a `.env` file in the project root:

   ```env
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_INDEX=your_index_name
   ```

---

## Running the Server

```bash
python vignan_mcp_server.py
```

The server will start at `http://localhost:8000`.

---

## API Endpoints

### `GET /list-tools`

Returns metadata about all available tools exposed by this MCP server.

**Response:**
```json
{
  "server": "VignanUniversity MCP Server",
  "tools": [
    {
      "name": "VignanUniversity",
      "description": "...",
      "parameters": { ... }
    }
  ]
}
```

---

### `POST /callTool`

Invokes a tool by name with the provided arguments.

**Request body:**
```json
{
  "name": "VignanUniversity",
  "arguments": {
    "query": "query",
    "top_k": 5
  }
}
```

| Field               | Type    | Required | Description                                      |
|---------------------|---------|----------|--------------------------------------------------|
| `name`              | string  | Yes      | Must be `"VignanUniversity"`                     |
| `arguments.query`   | string  | Yes      | Natural language query to search the knowledge base |
| `arguments.top_k`   | integer | No       | Number of results to return (default: `5`)       |

**Response:**
```json
{
  "result": [
    {
      "score": 0.91,
      "text": "Relevant chunk text...",
      "source": "document_name.pdf",
      "chunk_index": 3
    }
  ]
}
```

---

### `GET /health`

Health check endpoint.

**Response:**
```json
{ "status": "healthy" }
```

---

## Project Structure

```
.
├── vignan_mcp_server.py   # Main server application
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables
```

---

## Dependencies

| Package               | Purpose                                      |
|-----------------------|----------------------------------------------|
| `fastapi`             | Web framework for building the API           |
| `uvicorn`             | ASGI server to run the FastAPI app           |
| `fastmcp`             | MCP protocol utilities                       |
| `pinecone`            | Pinecone vector database client              |
| `sentence-transformers` | Embedding model (`all-MiniLM-L6-v2`)       |
| `python-dotenv`       | Load environment variables from `.env`       |
| `httpx`               | HTTP client (async support)                  |

