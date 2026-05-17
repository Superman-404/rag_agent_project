from typing import Callable

from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain.tools.tool_node import ToolCallRequest
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from langgraph.runtime import Runtime

from util.logger_handler import logger
from util.prompts_loader import loader_report_prompts, loader_system_prompts

# 工具执行监控
@wrap_tool_call
def monitor_tool(
        # 请求的数据封装
        request: ToolCallRequest,
        # 执行的函数本身handler接收的参数数据类型[ToolCallRequest]，返回值数据类型[ToolMessage | Command]
        handler: Callable[[ToolCallRequest], ToolMessage | Command]
) -> ToolMessage | Command:
    logger.info(f"[monitor_tool]执行工具：{request.tool_call['name']}")
    logger.info(f"[monitor_tool]传入参数：{request.tool_call['args']}")

    try:
        result = handler(request)
        logger.info(f"[monitor_tool]工具：{request.tool_call['name']}调用成功")
        # 用户需要报告的时候需要调用fill_context_for_report
        if request.tool_call["name"] == "fill_context_for_report":
            request.runtime.context["report"] = True

        return result
    except Exception as e:
        logger.error(f"{request.tool_call['name']}工具执行错误：{str(e)}")
        raise e

# 在模型执行前输出日志
@before_model
def log_before_model(
        state: AgentState,  # 整个agent智能体中的状态记录
        runtime: Runtime  # 记录了整个执行过程中的上下文信息
):
    logger.info(f"[log_before_model]即将开始执行模型：带有{len(state['messages'])}条消息。")

    logger.debug(
        f"[log_before_model]消息内容：{type(state['messages'][-1]).__name__}|{state['messages'][-1].content.strip()}")

    return None

# 动态切换提示词
@dynamic_prompt # 每一次在生成提示词之前，调用此函数
def report_prompt_switch(request: ModelRequest):
    is_report = request.runtime.context.get("report", False)
    if is_report:#  报告生成场景，返回报告生成提示词内容
        return loader_report_prompts()

    return loader_system_prompts()

