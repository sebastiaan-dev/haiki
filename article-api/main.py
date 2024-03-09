from dotenv import load_dotenv
from starlette.responses import JSONResponse

from pipelines import Template
from utils.files import get_folders_from_dir

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import pipelines as pl
import database as db

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


@app.post("/article/createTemplate")
def create_article_template(template:Template):
    """
    Create a template for different article types
    """
    return db.upsertTemplate(template)

@app.post("/article/create")
def create_article(item: pl.Item):
    """
    Create a new article based on a article template and topic.
    """
    # template = get_article_template()
    # parts = extract_template_parts(template)
    return pl.article("creatine", item)


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
    for folder in get_folders_from_dir(paper.path):
        pl.papers(paper.path + "/" + folder)

    return {"msg": "Request processed successfully"}

@app.get("/topics")
def get_topics():
    """
    Get all the hot topics
    """
    return JSONResponse(content=["Creatine", "Ayaska", "THC", "Ethanol"])
