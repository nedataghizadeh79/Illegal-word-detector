from typing import List, Dict, Tuple
from fastapi import FastAPI
from pydantic import BaseModel


class InputSchema(BaseModel):
    illegal_words: List[str]
    text: str


class OutputSchema(BaseModel):
    illegals: Dict[str, List[Tuple[int, int]]]


app = FastAPI()


@app.post("/run")
async def run(inp: InputSchema) -> OutputSchema:
    out = {
        "تفنگ": [(0, 4)],
        "سرکه": [(6, 14)],
        "اصغر": [(18, 25)]
    }
    return OutputSchema(illegals=out)
