from typing import Any

from transformers import pipeline

from app.interface.pipeline_provider import IPredictionPipeline


class HuggingFacePipeline(IPredictionPipeline):

    def __init__(self, model: str) -> None:
        self.hf_pipeline = pipeline(model=model)

    def predict(self, input: Any) -> Any:
        return self.hf_pipeline(input)