from dotenv import load_dotenv
from starlette.responses import JSONResponse

from utils.files import get_folders_from_dir

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import pipelines as pl

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*"
)

@app.get("/article/{id}")
def get_article():
    """
    Fetch the article with the given id. Returns a LaTeX string.
    """
    return {"article": "article"}


@app.post("/article/create")
def create_article():
    """
    Create a new article based on a article template and topic.
    """
    return {"Hello": "World"}


@app.put("/article/refine")
def refine_article():
    """
    Refine an existing article based on new documents in the database.
    """
    return {"Hello": "World"}


class CreatePaper(BaseModel):
    path: str


@app.post("/papers/create")
def create_papers(paper: CreatePaper):
    """
    Create a new paper based on a file.
    """
    get_folders_from_dir(paper.path)
    # pl.papers(paper.path)

    return {"msg": "Request processed successfully"}

@app.get("/topics")
def get_topics():
    """
    Get all the hot topics
    """
    return JSONResponse(content=["Creatine", "Ayaska", "THC", "Ethanol"])
