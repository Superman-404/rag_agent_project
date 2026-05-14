import os
from abc import ABC, abstractmethod
from typing import Optional

from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel

from util.config_handler import rag_conf
from dotenv import load_dotenv
load_dotenv()


# 创建聊天模型/嵌入模型

class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self)-> Optional[Embeddings | BaseChatModel]:
        pass

api_key = os.getenv("DASHSCOPE_API_KEY")
if not api_key:
    raise ValueError("请设置环境变量 DASHSCOPE_API_KEY")

class ChatModelFactory(BaseModelFactory):
    def generator(self) -> BaseChatModel:

        return ChatTongyi(model=rag_conf["chat_model_name"],
                          api_key=api_key)

class EmbeddingModelFactory(BaseModelFactory):
    def generator(self) -> Embeddings:
        return DashScopeEmbeddings(model=rag_conf["embedding_model_name"],
                          dashscope_api_key=api_key)


chat_model = ChatModelFactory().generator()
embedding_model = EmbeddingModelFactory().generator()