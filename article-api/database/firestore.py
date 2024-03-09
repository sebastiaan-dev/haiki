import firebase_admin
from firebase_admin import credentials, firestore
from pipelines import Template
from dataclasses import asdict

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(
    cred,
    {
        "projectId": "haiki-93e62",
    },
)

db = firestore.client()


def upsertArticle(topic: str, article: dict):
    doc_ref = db.collection(f"articles-{topic}").document(article["title"])
    doc_ref.set(article)
    return {"message": "Article created", "id": doc_ref.id}


def getArticle(topic: str, title: str):
    doc_ref = db.collection(f"articles-{topic}").document(title)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return {"message": "No such document!"}


def getArticleTitles(topic: str):
    docs = db.collection(f"articles-{topic}").stream()
    titles = []
    for doc in docs:
        titles.append(doc.id)
    return titles


def getArticles(topic: str):
    docs = db.collection(f"articles-{topic}").stream()
    articles = []
    for doc in docs:
        articles.append(doc.to_dict())
    return articles


def upsertTemplate(template: Template):
    doc_ref = db.collection("templates").document(template.title)
    # print(template.to_json())

    doc_ref.set(asdict(template))
    return {"message": "Article template created", "id": doc_ref.id}


def getTemplate(title: str):
    doc_ref = db.collection("templates").document(title)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return {"message": "No such document!"}
