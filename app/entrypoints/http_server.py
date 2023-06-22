# This module is main to spawn an http server.
#
# In this module, we connect all elements together, in order to make the
# server runnable.
import asyncio
import logging
from asyncio import Queue
from typing import Any

from fastapi import FastAPI

from app.infrastructure import web_app
from app.infrastructure.pipeline_provider import init_langchain_provider, init_pipeline_loop


def app_factory() -> FastAPI:
    logging.getLogger().setLevel(logging.INFO)
    app = web_app.create_app()
    q: Queue[tuple[str, Queue[Any]]] = Queue()
    app.model_queue = q
    asyncio.create_task(init_pipeline_loop(q))  # Use start_up event to have something more fluid ?
    init_langchain_provider()
    return app

