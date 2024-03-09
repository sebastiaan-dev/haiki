import json
import os

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
    sections, citations = fm.article(template, generated)

    return db.upsertArticle(
        topic, {"title": title, "sections": sections, "citations": citations}
    )


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


@app.post("/paper/create")
def create_papers():
    """
    Create a new paper based on a file.
    """
    pages = []

    for index in range(1, 7):
        # write to file
        with open(f"_data_/scrape/page_{index}.json", "r") as f:
            segment = json.load(f)
            pages.extend(segment)

    for dir, _, names in os.walk("_data_/scrape/pdfs/"):
        for name in names:
            # split name into title and extension
            title, ext = os.path.splitext(name)

            # find the paper in the pages

            for paper in pages:
                if paper["title"] == title:
                    print(f"Found paper: {title}")
                    metadata = {}
                    try:
                        metadata = {
                            "title": title,
                            "doi": paper["doi"],
                            "primary_topic_name": paper["primary_topic"][
                                "display_name"
                            ],
                            "primary_topic_subfield": paper["primary_topic"][
                                "subfield"
                            ]["display_name"],
                            "primary_topic_field": paper["primary_topic"]["field"][
                                "display_name"
                            ],
                            "primary_topic_domain": paper["primary_topic"]["domain"][
                                "display_name"
                            ],
                            "cited_by_count": paper["cited_by_count"],
                            "publication_date": paper["publication_date"],
                        }
                    except:
                        metadata = {
                            "title": title,
                            "doi": paper["doi"],
                        }

                    pl.paper("_data_/scrape/pdfs/" + name, metadata=metadata)
                    break

    return {"msg": "Request processed successfully"}
