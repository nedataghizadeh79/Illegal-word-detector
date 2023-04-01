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
    out = {}
    for word in inp.illegal_words:
        if word not in out:
            out[word] = [(0, len(word))]
        else:
            out[word] += (0, len(word))
    print("\n\n")
    for key in out:
        print(key)
        print("\t", out[key])
    print("\n\n")
    return OutputSchema(illegals=out)
