"""
文件配置工具
"""
import hashlib
import os

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document

from util.logger_handler import logger


def get_file_md5_hex(filepath: str):
    if not os.path.exists(filepath):
        logger.error(f"文件不存在: {filepath}")
        return None
    if not os.path.isfile(filepath):
        logger.error(f"不是文件: {filepath}")
        return None

    md5_obj = hashlib.md5()

    chunk_size = 4096

    try:
        with open(filepath, "rb") as f:  # "rb" 模式：read（只读）+ binary（二进制）为什么要用二进制模式？因为 MD5 计算需要原始字节数据，而不是文本
            chunk = f.read(chunk_size)
            while chunk:
                md5_obj.update(chunk)  # md5.update是追加模式
                chunk = f.read(chunk_size)
            """
            新语法：
            while chunk :=f.read(chunk_size)
                md5_obj.update(chunk)
            """

            md5_hex = md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"文件: {filepath}计算md5错误,{str(e)}")
        return None


def listdir_with_allowed_type(filepath: str, allowed_type: tuple[str]):
    files = []
    if not os.path.isdir(filepath):
        logger.error(f"[listdir_with_allowed_type]{filepath}不是文件夹/目录")
        return allowed_type
    for f in os.listdir(filepath):
        if f.endswith(allowed_type):
            files.append(os.path.join(filepath, f))
    return tuple(files)


def pdf_loader(filepath: str, passwd=None) -> list[Document]:
    return PyPDFLoader(filepath, passwd).load()


def txt_loader(filepath: str) -> list[Document]:
    return TextLoader(filepath, encoding="utf-8").load()


if __name__ == '__main__':
    print(get_file_md5_hex("D:/1.txt"))
