import asyncio
import logging
from typing import Any
from app.endpoints.models import QuestionDto

from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.llms import AzureOpenAI
from langchain.output_parsers import PydanticOutputParser, BooleanOutputParser

from app.interface import pipeline_provider as pipeline_provider_interface


async def predict(input: str) -> Any:
    response_q = asyncio.Queue()
    await pipeline_provider_interface.MODEL_QUEUE.put((input, response_q))
    return await response_q.get()

def has_questions(query: str) -> Any:
    # Try to add as much context in your rephrased questions as possible so they make sense on their own.
    prompt_template = "You are given a text and your job is to detect whether the main intent of the text is to ask questions or not. You are expected to respond only with YES or NO, nothing else.\n\nTEXT:\n{content}\n\nANSWER:"
    parser = BooleanOutputParser()
    prompt = PromptTemplate.from_template(prompt_template)

    llm = AzureOpenAI(deployment_name="matthias", model_name="text-davinci-003", temperature=0)

    _input = prompt.format_prompt(content=query)
    output = llm(_input.to_string())

    has_questions = parser.parse(output)

    return [{
        "label": "LABEL_1" if has_questions else "LABEL_0",
        "score": 1
    }]

def find_questions(query: str) -> Any:
    # Try to add as much context in your rephrased questions as possible so they make sense on their own.
    prompt_template = "Answer the user query.\n{format_instructions}\nIn the following text, try to identify and refrase the multiple questions inside the text. {content}"
    parser = PydanticOutputParser(pydantic_object=QuestionDto)
    prompt = PromptTemplate.from_template(prompt_template, partial_variables={"format_instructions": parser.get_format_instructions()},)

    llm = AzureOpenAI(deployment_name="matthias", model_name="text-davinci-003", temperature=0)

    _input = prompt.format_prompt(content=query)
    output = llm(_input.to_string())

    found_questions = parser.parse(output)
    return found_questions
