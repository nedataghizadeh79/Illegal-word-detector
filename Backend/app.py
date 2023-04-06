


from typing import List, Dict, Tuple
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from illegal_word_finder import run as run_illegal_finder


class InputSchema(BaseModel):
    illegal_words: List[str]
    text: str


class OutputSchema(BaseModel):
    illegals: Dict[str, List[Tuple[int, int]]]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/runmock")
async def run_mock(inp: InputSchema) -> OutputSchema:
    out = {
        "تفنگ": [(0, 4)],
        "سرکه": [(6, 14)],
        "اصغر": [(18, 25)]
    }
    return OutputSchema(illegals=out)


@app.post("/run")
async def run(inp: InputSchema) -> OutputSchema:
    res = run_illegal_finder(inp.text, inp.illegal_words)
    return OutputSchema(illegals=res)


@app.get('/test')
async def test():
    return {
        "message": "OK!"
    }
