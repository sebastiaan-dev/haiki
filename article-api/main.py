from dotenv import load_dotenv
from utils.files import get_folders_from_dir

load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel

import pipelines as pl
import form as fm
import database as db

app = FastAPI()


@app.post("/template/create")
def create_template(template: pl.Template):
    """
    Create a template for different article types
    """
    return db.upsertTemplate(template)


@app.get("/article/{topic}/{id}")
def get_article(topic: str, id: str):
    """
    Fetch the article with the given id.
    """
    return db.getArticle(topic, id)


@app.get("/articles/{topic}")
def get_articles(topic: str):
    """
    Fetch all articles for the given topic.
    """
    return db.getArticles(topic)


@app.get("/articles/{topic}/title")
def get_article_titles(topic: str):
    """
    Fetch all article titles for the given topic.
    """
    return db.getArticleTitles(topic)


@app.post("/article/{topic}/create/{title}")
def create_article(topic: str, title: str):
    """
    Create a new article based on a article template and topic.
    """
    template = db.getTemplate(topic)

    generated = pl.article(title, template)
    sections = fm.article(template, generated)

    return db.upsertArticle(topic, {"title": title, "sections": sections})


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
