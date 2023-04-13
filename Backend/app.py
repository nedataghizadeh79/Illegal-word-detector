import datetime
from typing import List, Dict, Tuple, Annotated
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pdf_reader_module import Pdf2txt
from superduper_pipeline import run as run_illegal_finder


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


@app.post("/run")
async def run(inp: InputSchema) -> OutputSchema:
    res = run_illegal_finder(inp.text, inp.illegal_words)
    output = {key: [x[1] for x in value] for key, value in res.items()}
    return OutputSchema(illegals=output)


@app.post("/runpdf")
async def run_pdf(pdf_file: Annotated[UploadFile, File(description="pdf file read as bytes")],
                  illegal_words: Annotated[str, Form()]) -> OutputSchema:
    with open(f"assets/test_pdfs/test_pdf_{datetime.datetime.now()}.pdf", "wb") as file:
        contents = await pdf_file.read()
        file.write(contents)
        file.flush()
        text = Pdf2txt().pdf2txt(pdf_path=file.name)
        res = run_illegal_finder(text, illegal_words.split(','))
        output = {key: [x[1] for x in value] for key, value in res.items()}
        return OutputSchema(illegals=output)


@app.post('/test_pdf')
async def test(pdf_file: Annotated[UploadFile, File(description="pdf file read as bytes")]) -> str:
    with open(f"assets/test_pdfs/test_pdf_{datetime.datetime.now()}.pdf", "wb") as file:
        contents = await pdf_file.read()
        file.write(contents)
        file.flush()
        text = Pdf2txt().pdf2txt(pdf_path=file.name)
        return text
