from util.config_handler import prompts_conf, rag_conf
from util.logger_handler import logger
from util.path_tool import get_asb_path


def loader_system_prompts():
    try:
        system_prompt_path = get_asb_path(prompts_conf["main_prompt_path"])
    except KeyError as e:
        logger.error(f"[loader_system_prompts]在yaml配置中没有main_prompt_path配置项")
        raise e

    try:
        return open(system_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[loader_system_prompts]解析系统提示文件失败,{str(e)}")
        raise e

def loader_rag_prompts():
    try:
        rag_prompt_path = get_asb_path(prompts_conf["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error(f"[loader_rag_prompts]在yaml配置中没有rag_summarize_prompt_path配置项")
        raise e

    try:
        return open(rag_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[loader_rag_prompts]解析系统提示文件失败,{str(e)}")
        raise e

def loader_report_prompts():
    try:
        system_prompt_path = get_asb_path(prompts_conf["report_prompt_path"])
    except KeyError as e:
        logger.error(f"[loader_report_prompts]在yaml配置中没有report_prompt_path配置项")
        raise e

    try:
        return open(system_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[loader_report_prompts]解析系统提示文件失败,{str(e)}")
        raise e

if __name__ == '__main__':
    print(loader_system_prompts())
    print(loader_rag_prompts())
    print(loader_report_prompts())

    # 错误总结：rag_prompt_path = get_asb_path(prompts_conf["rag_summarize_prompt_path"]) 这里容易把prompts_conf写成rag_conf