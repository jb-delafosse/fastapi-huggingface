import logging
from typing import List

from langchain.chains import RetrievalQA, RetrievalQAWithSourcesChain
from langchain.llms import AzureOpenAI
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainFilter

from app.usecase.comments import get_comments_and_posts
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
    comments_and_posts = get_comments_and_posts(user_jwt, query)

    return [
        Document(
            page_content=next(iter(comment.get("text").values())),
            metadata={"comment_id": comment.get("uid"), "post_id": comment.get("content"), "source": comment.get("content")}
        )
        for comment in comments_and_posts["comments"] if comment.get("text")
    ] + [
        Document(
            page_content=post.text,
            metadata={"comment_id": None, "post_id": post.id, "source": post.id}
        )
        for post in comments_and_posts["posts"] if post.text
    ]


def get_answer(user_jwt: str, query: str, use_prefilter: bool = False) -> str:
    llm = AzureOpenAI(deployment_name="matthias", model_name="text-davinci-003")

    retriever = PotentialAnswersRetriever(user_jwt)
    if use_prefilter:
        _filter = LLMChainFilter.from_llm(llm)
        retriever = ContextualCompressionRetriever(
            base_compressor=_filter,
            base_retriever=retriever,
        )

    qa = RetrievalQAWithSourcesChain.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)
    answer = qa(query)
    logging.warning(answer)
    return answer
