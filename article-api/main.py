from dotenv import load_dotenv

from utils.files import get_folders_from_dir

load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel

import pipelines as pl

app = FastAPI()


@app.get("/article/{id}")
def get_article():
    """
    Fetch the article with the given id. Returns a LaTeX string.
    """
    return {"article": "article"}


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
