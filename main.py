from fastapi import FastAPI
from pydantic import BaseModel
from for_api import Response, prepare_response

app = FastAPI()


class Request(BaseModel):
    program: str
    stdin: str


@app.post("/interpreter", response_model=Response)
async def interpret_code(request: Request):
    return prepare_response(request.program, request.stdin)