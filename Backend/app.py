import datetime
import tempfile
from typing import List, Dict, Tuple, Annotated
from fastapi import FastAPI, UploadFile, File, Form, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from illegal_word_finder import run as run_illegal_finder
from pdf_reader_module import Pdf2txt


class InputSchema(BaseModel):
    illegal_words: List[str]
    text: str


class OutputSchema(BaseModel):
    illegals: Dict[str, List[Tuple[int, int]]]


app = FastAPI()
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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


@app.post("/runpdf")
async def run_pdf(pdf_file: Annotated[UploadFile, File(description="pdf file read as bytes")],
                  illegal_words: list[str]) -> OutputSchema:
    with open(f"assets/test_pdfs/test_pdf_{datetime.datetime.now()}.pdf", "wb") as file:
        contents = await pdf_file.read()
        file.write(contents)
        file.flush()
        text = Pdf2txt().pdf2txt(pdf_path=file.name)
        res = run_illegal_finder(text, illegal_words)
        return OutputSchema(illegals=res)


@app.get('/test')
async def test():
    return {
        "message": "OK!"
    }
