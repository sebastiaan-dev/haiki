from dataclasses import dataclass

from haystack import Pipeline
from haystack.components.builders import PromptBuilder, AnswerBuilder
from haystack_integrations.components.retrievers.chroma import ChromaEmbeddingRetriever
from haystack_integrations.components.embedders.ollama import OllamaTextEmbedder
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
    If type is title, you should write ONLY the title of the section and nothing else. If type is text, you should write the paragraph.
    \nDocuments:
    {% for doc in documents %}
        {{ doc.content }}
    {% endfor %}

    \nTopic: {{topic}}
    \nType: {{type}}
    \nQuery: {{query}}
    \nAnswer:
    """

    result = []

    for subitem in item.items:

        pipe = Pipeline()

        pipe.add_component(name="embedder", instance=OllamaTextEmbedder())
        pipe.add_component(name="retriever", instance=ChromaEmbeddingRetriever(store))
        pipe.add_component(name="prompt", instance=PromptBuilder(template=template))
        pipe.add_component(
            name="llm", instance=OllamaGenerator(model="nous-hermes2:10.7b-solar-q8_0")
        )
        pipe.add_component(name="answer", instance=AnswerBuilder())

        pipe.connect("embedder.embedding", "retriever.query_embedding")
        pipe.connect("retriever", "prompt")
        pipe.connect("prompt", "llm")
        pipe.connect("llm.replies", "answer.replies")
        pipe.connect("llm.metadata", "answer.meta")
        pipe.connect("retriever", "answer.documents")

        result.append(
            pipe.run(
                {
                    "embedder": {
                        "text": f"{subitem.description} {item.description} {topic}"
                    },
                    "prompt": {
                        "topic": topic,
                        "type": subitem.type,
                        "query": f"{subitem.description} {item.description} {topic}",
                    },
                    "answer": {
                        "query": f"{subitem.description} {item.description} {topic}"
                    },
                }
            )
        )

    return result
