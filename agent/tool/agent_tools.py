import os
import random

from langchain_core.tools import tool

from rag.rag_service import RagSummarizeService
from util.config_handler import agent_conf
from util.logger_handler import logger
from util.path_tool import get_asb_path

user_ids = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010"]
month_arr = ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06", "2025-07", "2025-08", "2025-09",
             "2025-10", "2025-11", "2025-12"]
rag = RagSummarizeService()

external_data = {}


@tool(description="从向量储存中检索内容，并生成总结")
def rag_summarize(query: str) -> str:
    return rag.rag_summarize(query)


@tool(description="获取指定城市的天气，以字符串的形式返回")
def get_weather(city: str) -> str:
    return f"{city}的天气是晴天,气温26摄氏度，空气湿度25%"


@tool(description="获取用户所在城市的名称，以字符串的形式返回")
def get_user_location() -> str:
    return random.choice(["北京", "上海", "广州", "深圳", "杭州"])


@tool(description="获取用户的ID，以纯字符串形式返回")
def get_user_id() -> str:
    return random.choice(user_ids)


@tool(description="获取当前月份，以纯文字形式返回")
def get_current_month() -> str:
    return random.choice(month_arr)


def generate_external_data():
    # dic ={
    #     "user_id":{
    #         "month":{"特征":"...","结果":"...","数据":"..."},
    #         "month":{"特征":"...","结果":"...","数据":"..."},
    #         "month":{"特征":"...","结果":"...","数据":"..."}
    #     },
    #     "user_id":{
    #         "month":{"特征":"...","结果":"...","数据":"..."},
    #         "month":{"特征":"...","结果":"...","数据":"..."},
    #         "month":{"特征":"...","结果":"...","数据":"..."}
    #     },
    #     ...
    # }
    if not external_data: # if not X 的意思并不是“如果 X 不存在”,而是看 X 的布尔值，空字典，字符串，列表，元组等都是false值

        external_data_path = get_asb_path(agent_conf["external_data_path"])

        if not os.path.exists(external_data_path):
            logger.error(f"[外部数据源]目录不存在:{external_data_path}")
            raise FileNotFoundError(f"外部数据文件{external_data_path}不存在")

        with open(external_data_path, "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                arr: list[str] = line.strip().split(",")

                user_id: str = arr[0].replace('"', '')
                feature: str = arr[1].replace('"', '')
                efficiency: str = arr[2].replace('"', "")
                consumables: str = arr[3].replace('"', "")
                comparison: str = arr[4].replace('"', "")
                time: str = arr[5].replace('"', "")

                if user_id not in external_data:
                    external_data[user_id] = {}

                external_data[user_id][time] = {
                    "特征": feature,
                    "清洁效率": efficiency,
                    "耗材": consumables,
                    "对比": comparison
                }

@tool(description="从外部数据获取指定用户在指定月份的使用记录，返回字符串，如果没有数据则返回空字符串")
def fetch_external_data(user_id: str, mouth: str) -> str:
    """

    :param user_id:
    :param mouth:
    :return:
    """
    generate_external_data()
    try:
        return external_data[user_id][mouth]
    except KeyError:
        logger.warning(f"[外部数据源]没有该用户或该用户没有该月份的数据:{user_id},{mouth}")
        return ""


@tool(description="无入参，无返回值，调用后触发中间件自动为报告生成的场景动态注入上下文信息，为后续提示词切换提供上下文信息")
def fill_context_for_report():
    return "fill_context_for_report已调用"

if __name__ == '__main__':
    # 注意：invoke 接收的是一个字典，键名必须与函数参数名一致
    result = fetch_external_data.invoke({"user_id": "1005", "mouth": "2025-01"})
    print(result)