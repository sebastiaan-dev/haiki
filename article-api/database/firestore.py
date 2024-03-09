import firebase_admin
from firebase_admin import credentials, firestore
from pydantic import BaseModel
from pipelines import Template
import json
from dataclasses import asdict

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': 'haiki-93e62',
})

db = firestore.client()


def upsertTemplate(template:Template):
    doc_ref = db.collection("templates").document(template.title)
    # print(template.to_json())

    doc_ref.set(asdict(template))
    return {"message": "Article template created", "id": doc_ref.id}