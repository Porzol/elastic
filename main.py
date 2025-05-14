import os
import json
import uvicorn
import argparse
import services
from api import v1
from fastapi import FastAPI

app = FastAPI(title="Elasticsearch Service")
app.include_router(v1.get_router(), prefix="/api/v1")

@app.get("/")
def hello():
    return {"message": "Hello from the Elastic Service!"}

def main():
    env_host = os.getenv("HOST", "0.0.0.0")
    env_port = int(os.getenv("PORT", 8000))

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, help="Enter an ipv4 address, enclose it in quotes")
    parser.add_argument("--port", type=int, help="Enter a port number")
    args = parser.parse_args()

    host = args.host if args.host is not None else env_host
    port = args.port if args.port is not None else env_port

    uvicorn.run("main:app", host = host, port = port, reload=True)

if __name__ == "__main__":
    main()