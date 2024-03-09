# Haiki

This repository contains the AI based knowledgebase. 
Based on research papers stored in a vector database, articles can be generated using predefined templates.
These templates define the sections, titles and paragraphs which should be filled using an LLM.

## Infrastructure

chroma vector database -> selfhosted
firestore noSQL database -> google cloud
web API -> python fast api
frontend -> react
llm framework -> [haystack](https://haystack.deepset.ai)
datasource sientific papers -> [openalex](https://openalex.org)
LLM -> mostly ollama run localy (but interchangable)
ollama -> local hosting llm

## Usage

api back end

'''sh
uvicorn main:app --reload
'''

frontend

'''sh
bun run dev
'''

## Templates

Templates can be created using the appropriate endpoint, they follow
the structure outlined in 'pipelines/sample_template.json'.