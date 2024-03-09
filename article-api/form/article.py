from typing import Any, Dict, List

import pipelines as pl


def article(template: pl.Template, generated: List[List[Dict[str, Any]]]):
    sections = []
    citations = []

    for i, section in enumerate(template["sections"]):
        found, cites = format_section(section, generated[i])
        sections.append(found)
        citations.extend(cites)

    return sections, citations


def format_section(section: pl.Item, generated: List[Dict[str, Any]]):
    parsed = {}
    citations = []

    for i, item in enumerate(section["items"]):
        for doc in generated[i]["answer"]["answers"][0].documents:
            print(doc)
            citations.append(doc.meta["doi"])

        if item["el"] == "p":
            cleaned = pl.clean_section_text(generated[i]["answer"]["answers"][0].data)[
                "answer"
            ]["answers"][0].data
            if parsed.get("p"):
                parsed["p"].append(cleaned)
            else:
                parsed["p"] = [cleaned]
        else:
            parsed[item["el"]] = generated[i]["answer"]["answers"][0].data

    return parsed, citations
