import asyncio
from typing import Any

from app.interface import pipeline_provider as pipeline_provider_interface


async def predict(input: str) -> Any:
    response_q = asyncio.Queue()
    await pipeline_provider_interface.MODEL_QUEUE.put((input, response_q))
    return await response_q.get()
