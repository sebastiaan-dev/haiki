from typing import Any, Dict, List

from pipelines import Template, Item


def article(template: Template, generated: List[List[Dict[str, Any]]]):
    sections = []

    for i, section in enumerate(template.sections):
        sections.append(format_section(section, generated[i]))

    return sections


def format_section(section: Item, generated: List[Dict[str, Any]]):
    section = {}

    for i, item in enumerate(section.items):
        if item.el == "p":
            if section["p"]:
                section["p"].append(generated[i]["answer"]["answers"][0].data)
            else:
                section["p"] = [generated[i]["answer"]["answers"][0].data]
        else:
            section[item.el] = generated[i]["answer"]["answers"][0].data

    return section
