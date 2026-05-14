from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from model.factory import chat_model
from rag.vector_store import VectorStoreService
from util.logger_handler import logger
from util.prompts_loader import loader_rag_prompts


def print_prompt(prompt):
    print("*" * 20)
    print(prompt.to_string())
    print("*" * 20)
    return prompt


class RagSummarizeService:
    """
    rag 总结服务
    """

    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        self.prompt_text = loader_rag_prompts()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self._init_chain()

    def _init_chain(self):
        return self.prompt_template | print_prompt | self.model | StrOutputParser()

    def retriever_document(self, query: str):
        return self.retriever.invoke(query)

    def rag_summarize(self, query: str):
        if not query or not query.strip():
            raise ValueError("查询内容不能为空")

        context_doc = self.retriever_document(query)

        if not context_doc:
            logger.warning(f"[Rag总结]未找到相关文档：{query}")
            return "抱歉，未找到与您的问题相关知识库参考资料"

        # # 错误写法 join(生成器表达式) 不是 字符串
        # context = ""
        # for doc in context_doc:
        #     context = "\n\n".join(f"参考资料:{doc.page_content}")

        context = "\n\n".join(doc.page_content for doc in context_doc)

        try:

            return self.chain.invoke(
                {
                    "input": query,
                    "context": context
                }
            )
        except Exception as e:
            logger.error(f"[Rag总结]执行错误,{str(e)}", exc_info=True)
            raise


if __name__ == '__main__':
    rs = RagSummarizeService()
    print(rs.rag_summarize("小户型适合哪些扫地机器人？"))
