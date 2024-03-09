from dotenv import load_dotenv
from pipelines import Template
from utils.files import get_folders_from_dir

load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel

import pipelines as pl
import form as fm
import database as db

app = FastAPI()


@app.get("/article/{topic}/{id}")
def get_article():
    """
    Fetch the article with the given id.
    """
    return {"article": "article"}


@app.post("/article/createTemplate")
def create_article_template(template: Template):
    """
    Create a template for different article types
    """
    return db.upsertTemplate(template)


@app.post("/article/create")
def create_article(item: pl.Template):
    """
    Create a new article based on a article template and topic.
    """
    generated = pl.article("creatine", item)
    return fm.article(item, generated)


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
