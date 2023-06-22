from asyncio import Queue
import logging
import os
from pathlib import Path
import logging
import os
from pathlib import Path
from typing import Any
from app.adapter import database

from langchain.document_loaders import CSVLoader, JSONLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from app.adapter.hugging_face_pipeline_provider import HuggingFacePipeline
from app.interface import pipeline_provider as pipeline_provider_interface


async def init_pipeline_loop(q: Queue[tuple[str, Queue[Any]]]) -> None:
    pipeline_provider_interface.MODEL_QUEUE = q
    # Other models can be loaded here.
    pipe = HuggingFacePipeline(model="shahrukhx01/bert-mini-finetune-question-detection")  # Profanity Detection
    pipe = HuggingFacePipeline(model="shahrukhx01/bert-mini-finetune-question-detection")  # Profanity Detection
    while True:
        (string, response_q) = await q.get()
        out = pipe.predict(string)
        await response_q.put(out)

def init_langchain_provider():
    os.environ["OPENAI_API_TYPE"] = "azure"
    os.environ["OPENAI_API_VERSION"] = "2023-03-15-preview"
    os.environ["OPENAI_API_BASE"]="https://test-elie-openai.openai.azure.com/"
    os.environ["OPENAI_API_KEY"]="XXX"

    embeddings = OpenAIEmbeddings(deployment="lumhack2023-embeddings", chunk_size=1)

    FAISS_DIR = Path("local")
    FAISS_LOCAL_PATH = Path("faiss.db")
    if os.path.exists(f"{FAISS_DIR}/{FAISS_LOCAL_PATH}.faiss"):
        database.FAISS_DB = FAISS.load_local(folder_path=str(FAISS_DIR), index_name=str(FAISS_LOCAL_PATH), embeddings=embeddings)
    else:
        # csv_documents = CSVLoader('./local/data/the-posts.csv', csv_args={
        # 'delimiter': ',',
        # }, source_column="id").load()
        csv_documents = JSONLoader(
            file_path='./local/data/the-posts.json',
            jq_schema=".[]",
            content_key="page_content",
            metadata_func=metadata_func
        ).load()
        logging.warning("load to local db")
        database.FAISS_DB = FAISS.from_documents(csv_documents, embeddings)
        database.FAISS_DB.save_local(folder_path=str(FAISS_DIR), index_name=str(FAISS_LOCAL_PATH))

# Define the metadata extraction function.
def metadata_func(record: dict, metadata: dict) -> dict:

    metadata["id"] = record.get("id")
    metadata["title"] = record.get("title")
    metadata["text"] = record.get("text")

    return metadata