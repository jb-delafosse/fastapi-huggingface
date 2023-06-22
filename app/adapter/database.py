from typing import Any, Optional


class IFaissDb():
    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[dict[str, Any]] = None,
        fetch_k: int = 20,
        **kwargs: Any,
    ) -> list[Any]:
        """Return docs most similar to query."""

FAISS_DB: IFaissDb