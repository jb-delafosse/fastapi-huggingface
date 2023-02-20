from asyncio import Queue
from typing import Any

from app.adapter.hugging_face_pipeline_provider import HuggingFacePipeline
from app.interface import pipeline_provider as pipeline_provider_interface


async def init_pipeline_loop(q: Queue[tuple[str, Queue[Any]]]) -> None:
    pipeline_provider_interface.MODEL_QUEUE = q
    # Other models can be loaded here.
    pipe = HuggingFacePipeline(model="unitary/toxic-bert")  # Profanity Detection
    while True:
        (string, response_q) = await q.get()
        out = pipe.predict(string)
        await response_q.put(out)
