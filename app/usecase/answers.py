from typing import List

from langchain.chains import RetrievalQA
from langchain.llms import AzureOpenAI
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainFilter

from app.usecase.comments import get_comments
from langchain.docstore.document import Document
from langchain.schema import BaseRetriever


class PotentialAnswersRetriever(BaseRetriever):

    def __init__(self, user_jwt):
        self.user_jwt = user_jwt

    def get_relevant_documents(self, query: str) -> list[Document]:
        return get_comments_as_documents(self.user_jwt, query)

    async def aget_relevant_documents(self, query: str) -> List[Document]:
        return self.get_relevant_documents(query)


def get_comments_as_documents(user_jwt: str, query: str) -> list[Document]:
    comments = get_comments(user_jwt, query)
    return [
        Document(
            page_content=comment.get("text").values[0],
            metadata={"comment_id": comment.get("uid"), "post_id": comment.get("content")}
        )
        for comment in comments if comment.get("text")
    ]


def get_answer(user_jwt: str, query: str, use_prefilter: bool = True) -> str:
    llm = AzureOpenAI(deployment_name="matthias", model_name="text-davinci-003")

    retriever = PotentialAnswersRetriever(user_jwt)
    if use_prefilter:
        _filter = LLMChainFilter.from_llm(llm)
        retriever = ContextualCompressionRetriever(
            base_compressor=_filter,
            base_retriever=retriever,
        )

    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    return qa.run(query)
