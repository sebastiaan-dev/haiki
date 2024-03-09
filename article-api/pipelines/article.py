from dataclasses import dataclass
from dataclasses_json import dataclass_json

from haystack import Pipeline
from haystack.components.builders import PromptBuilder, AnswerBuilder
from haystack_integrations.components.retrievers.chroma import ChromaEmbeddingRetriever
from haystack_integrations.components.embedders.ollama import OllamaTextEmbedder
from haystack_integrations.components.generators.ollama import OllamaGenerator

from chroma.db import store

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

@dataclass
class Item:
    type: str
    description: str
    items: list["Item"]

@dataclass
class Template:
    title: str
    sections: list[Item]


def article(topic: str, template: Template):

    sections = []

    for section in template.sections:
        sections.append(gen_section(section, topic))

    return sections


def gen_section(section: Item, topic: str):
    assert section.type == "section"

    items = []

    for subitem in section.items:
        items.append(gen_section_item(section, subitem, topic))

    return items


def gen_section_item(section: Item, item: Item, topic: str):
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

    return pipe.run(
        {
            "embedder": {"text": f"{item.description} {section.description} {topic}"},
            "prompt": {
                "topic": topic,
                "type": item.type,
                "query": f"{item.description} {section.description} {topic}",
            },
            "answer": {"query": f"{item.description} {section.description} {topic}"},
        }
    )
