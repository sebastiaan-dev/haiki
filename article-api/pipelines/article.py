from dataclasses import dataclass

from haystack import Pipeline
from haystack.components.builders import PromptBuilder, AnswerBuilder
from haystack_integrations.components.retrievers.chroma import ChromaEmbeddingRetriever
from haystack_integrations.components.embedders.ollama import OllamaTextEmbedder
from haystack_integrations.components.generators.ollama import OllamaGenerator

from chroma.db import store

template_text = """
    You are writing the section of a scientific article for which you can only use the given documents. Write in the style of a scientific paper.
    Be extremely exact in your answer. Topic tells you what you should write about. Query tells you what you should answer. Do not include any special characters in your answer.
    Don't reply with a confirmation and immediately start writing the answer.
    \nDocuments:
    {% for doc in documents %}
        {{ doc.content }}
    {% endfor %}

    \nTopic: {{topic}}
    \nQuery: {{query}}
    \nAnswer:
    """

template_title = """
    You are writing the title of a section of a scientific article. Write in the style of a scientific paper. The article will be published in an encyclopedia.
    Give a concise and informative title based on the query. Shorter is better and preferred.
    Topic tells you the subject of the article. Query tells you the specific focus of the section.
    Do not include any special characters in your answer, do NOT include quotes, only include letters or maybe a semicolon if absolutely necessary.

    \nTopic: {{topic}}
    \nQuery: {{query}}
    \nAnswer:
    """

template_clean_list = """
    If there are any lists or iterations in the input, remove them and write the text as a single paragraph.
    Keep the text as close to the original as possible. Keep the text as scientific as possible.
    Don't reply with a confirmation and immediately start writing the answer.

    \nQuery: {{query}}
    \nAnswer:
    """


@dataclass
class Item:
    type: str
    el: str
    description: str
    items: list["Item"]


@dataclass
class Template:
    title: str
    sections: list[Item]


def article(title: str, template: Template):
    sections = []

    for section in template["sections"]:
        sections.append(gen_section(section, title))

    return sections


def gen_section(section: Item, title: str):
    assert section["type"] == "section"

    items = []

    for subitem in section["items"]:
        match subitem["type"]:
            case "title":
                items.append(gen_section_title(subitem, title))
            case "text":
                items.append(gen_section_text(subitem, title))

    return items


def gen_section_title(item: Item, title: str):
    pipe = Pipeline()

    pipe.add_component(name="prompt", instance=PromptBuilder(template=template_title))
    pipe.add_component(
        name="llm", instance=OllamaGenerator(model="nous-hermes2:10.7b-solar-q8_0")
    )
    pipe.add_component(name="answer", instance=AnswerBuilder())

    pipe.connect("prompt", "llm")
    pipe.connect("llm.replies", "answer.replies")
    pipe.connect("llm.metadata", "answer.meta")

    return pipe.run(
        {
            "prompt": {
                "topic": title,
                "query": f"{item['description']} {title}",
            },
            "answer": {"query": f"{item['description']} {title}"},
        }
    )


def clean_section_text(text: str):
    pipe = Pipeline()

    pipe.add_component(
        name="prompt", instance=PromptBuilder(template=template_clean_list)
    )
    pipe.add_component(
        name="llm", instance=OllamaGenerator(model="nous-hermes2:10.7b-solar-q8_0")
    )
    pipe.add_component(name="answer", instance=AnswerBuilder())

    pipe.connect("prompt", "llm")
    pipe.connect("llm.replies", "answer.replies")
    pipe.connect("llm.metadata", "answer.meta")

    return pipe.run(
        {
            "prompt": {
                "query": text,
            },
            "answer": {"query": text},
        }
    )


def gen_section_text(item: Item, title: str):
    pipe = Pipeline()

    pipe.add_component(name="embedder", instance=OllamaTextEmbedder())
    pipe.add_component(name="retriever", instance=ChromaEmbeddingRetriever(store))
    pipe.add_component(name="prompt", instance=PromptBuilder(template=template_text))
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

    text = pipe.run(
        {
            "embedder": {"text": f"{item['description']} {title}"},
            "prompt": {
                "topic": title,
                "query": f"{item['description']} {title}",
            },
            "answer": {"query": f"{item['description']} {title}"},
        }
    )

    return text
