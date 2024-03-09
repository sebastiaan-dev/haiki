from dataclasses import dataclass

from haystack import Pipeline
from haystack.components.builders import PromptBuilder, AnswerBuilder
from haystack_integrations.components.retrievers.chroma import ChromaEmbeddingRetriever
from haystack_integrations.components.embedders.ollama import OllamaDocumentEmbedder
from haystack_integrations.components.generators.ollama import OllamaGenerator


from chroma.db import store


@dataclass
class Item:
    type: str
    description: str
    items: list["Item"]


def article(topic: str, item: Item):
    if item.type != "section":
        raise ValueError("The top level item must be a section")

    template = """
    You are writing the section of a scientific article for which you can only use the given documents.
    Be extremely exact in your answer. Topic tells you what you should write about. Query tells you what you should answer.
    \nDocuments:
    {% for doc in documents %}
        {{ doc.content }}
    {% endfor %}

    \nTopic: {{topic}}
    \nQuery: {{query}}
    \nAnswer:
    """

    for subitem in item.items:

        pipe = Pipeline()

        pipe.add_component(name="embedder", instance=OllamaDocumentEmbedder())
        pipe.add_component(name="retriever", instance=ChromaEmbeddingRetriever(store))
        pipe.add_component(name="prompt", instance=PromptBuilder(template=template))
        pipe.add_component(name="llm", instance=OllamaGenerator())
        pipe.add_component(name="answer", instance=AnswerBuilder())

        pipe.connect("embedder", "retriever")
        pipe.connect("retriever", "prompt")
        pipe.connect("prompt", "llm")
        pipe.connect("llm.replies", "answer.replies")
        pipe.connect("llm.meta", "answer.meta")
        pipe.connect("retriever", "answer.documents")

        return pipe.run(
            {
                "embedder": {"text": f"{subitem.description} + {topic}"},
                "prompt": {"topic": topic, "query": f"{subitem.description}"},
            }
        )
