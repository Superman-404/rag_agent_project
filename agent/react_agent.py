from langchain.agents import create_agent

from agent.tool.agent_tools import rag_summarize, get_weather, get_user_location, get_user_id, get_current_month, \
    fetch_external_data, fill_context_for_report
from agent.tool.middleware import report_prompt_switch, log_before_model, monitor_tool
from model.factory import chat_model
from util.prompts_loader import loader_system_prompts


class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            system_prompt=loader_system_prompts(),
            tools=[
                rag_summarize,
                get_weather,
                get_user_location,
                get_user_id,
                get_current_month,
                fetch_external_data,
                fill_context_for_report
            ],
            middleware=[
                monitor_tool,
                log_before_model,
                report_prompt_switch
            ]
        )

    def execute_stream(self, query: str):
        """
        执行流式执行
        :param query:
        :return:
        """
        input_dict = {
            "messages": [
                {"role": "user", "content": query}
            ]
        }
        for chunk in self.agent.stream(input_dict, stream_mode="values", context={"report": False}):
            last_message = chunk["messages"][-1]
            if last_message.content:
                yield last_message.content.strip() + "\n"


if __name__ == '__main__':
    agent = ReactAgent()
    for chunk in agent.execute_stream("给我生成我的使用报告"):
        print(chunk, end="", flush=True)
