import os

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from util.config_handler import chroma_conf
from model.factory import embedding_model
from util.file_handler import pdf_loader, txt_loader, listdir_with_allowed_type, get_file_md5_hex
from util.logger_handler import logger
from util.path_tool import get_asb_path


class VectorStoreService:
    """
    向量数据库服务
    """

    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            persist_directory=get_asb_path(chroma_conf["persist_directory"]),  # persist_directory: 数据库文件存放目录
            embedding_function=embedding_model
        )

        self.spliter = RecursiveCharacterTextSplitter(chunk_size=chroma_conf["chunk_size"],
                                                      chunk_overlap=chroma_conf["chunk_overlap"],
                                                      separators=chroma_conf["separators"],
                                                      length_function=len)

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})

    def load_document(self):
        """
        从数据文件夹内读取数据文件，转换为向量存入向量库
        要计算文件的md5做去重
        :return: None
        """

        def check_md5_hex(md5_for_check: str):
            if not os.path.exists(get_asb_path(chroma_conf["md5_hex_store"])):
                open(get_asb_path(chroma_conf["md5_hex_store"]), "w", encoding="utf-8").close()
                return False  # md5 没处理过

            with open(get_asb_path(chroma_conf["md5_hex_store"]), "r", encoding="utf-8") as f:
                for line in f.readlines():
                    if md5_for_check == line.strip():
                        return True

                return False

        def save_md5_hex(md5_for_check: str):
            with open(get_asb_path(chroma_conf["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_for_check)
                f.write("\n")

        def get_file_document(read_path: str):
            if read_path.endswith(".pdf"):
                return pdf_loader(read_path)
            if read_path.endswith(".txt"):
                return txt_loader(read_path)

            return []

        allow_file_path: list[str] = listdir_with_allowed_type(get_asb_path(chroma_conf["data_path"]),
                                                               tuple(chroma_conf["allow_knowledge_file_type"]))

        for path in allow_file_path:
            # 获取md5
            md5_hex = get_file_md5_hex(path)
            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]{path}内容已经存在,跳过")
                continue

            try:
                documents: list[Document] = get_file_document(path)
                if not documents:
                    logger.info(f"[加载知识库]{path}内容为空,跳过")
                    continue
                split_document: list[Document] = self.spliter.split_documents(documents)
                # split_documents() - 来自 RecursiveCharacterTextSplitter

                if not split_document:
                    logger.warning(f"[加载知识库]{path}分片后没有有效文本内容,跳过")
                    continue

                # 将内容存入向量库
                self.vector_store.add_documents(split_document)  # add_documents() - 来自 Chroma 向量数据库

                # 记录这个已经处理好的文件的md5，避免下次重复处理
                save_md5_hex(md5_hex)
                logger.info(f"[加载知识库]{path}成功")
            except Exception as e:
                # exc_info=True 为True时，会输出详细的报错堆栈，为False时只输出报错信息本身
                logger.error(f"[加载知识库]{path}失败,{str(e)}", exc_info=True)
                continue


if __name__ == '__main__':
    vs = VectorStoreService()
    vs.load_document()
    retriever = vs.get_retriever()
    res = retriever.invoke("迷路")
    for r in res:
        print(r.page_content)
        print("*" * 20)
