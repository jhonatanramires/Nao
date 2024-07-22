# /////////////////// THIRD-PARTY DEPENDENCIES ///////////////////////////////

# Dependencies for Type Annotations
from typing import Annotated
from typing_extensions import TypedDict

# Dependencies for Graph Tools
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition

# Dependencies for LLM Chat
from langchain_anthropic import ChatAnthropic
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

# Dependencies for Graph Display
from PIL import Image as PILImage
from IPython.display import Image, display
import io

# Dependencies for Memory Management
from langgraph.checkpoint.sqlite import SqliteSaver

# Dependencies for Messages Management (Human Node Depedend on this)
from langchain_core.messages import AIMessage, ToolMessage

# /////////////////// PROJECT-SPECIFIC DEPENDENCIES ///////////////////////////////



class AgentHandler:
    class State(TypedDict):
        messages: Annotated[list, add_messages]

    def __init__(self, api_key,tools,model_name):
        self.llm = ChatAnthropic(model_name=model_name, api_key=api_key)
        self.tools = tools
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.memory = SqliteSaver.from_conn_string("memory")
        self.graph = self._setup_graph()
        self.config = {"configurable": {"thread_id": "1"}}

    def _chatbot(self, state: State):
        return {"messages": [self.llm_with_tools.invoke(state["messages"])]}

    def _setup_graph(self):
        graph_builder = StateGraph(self.State)
        graph_builder.add_node("chatbot", self._chatbot)
        tool_node = ToolNode(self.tools)
        graph_builder.add_node("tools", tool_node)
        graph_builder.add_conditional_edges("chatbot", tools_condition)
        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_edge("tools", "chatbot")
        return graph_builder.compile(checkpointer=self.memory)

    def display_graph(self):
        try:
            img_data = self.graph.get_graph().draw_mermaid_png()
            if img_data:
                img = PILImage.open(io.BytesIO(img_data))
                img.show()
            else:
                print("The image was not generated correctly.")
        except Exception as e:
            print(f"Error generating the image: {e}")

    def chat(self):
        while True:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            for event in self.graph.stream(
                {"messages": [("user", user_input)]},
                {"configurable": {"thread_id": "2"}},
                stream_mode="values"
            ):
                event["messages"][-1].pretty_print()

if __name__ == "__main__":
    # Dependencies for Custom Tools
    from tools import tools
    api_key = "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"
    chatbot = AgentHandler(api_key,tools,"claude-3-haiku-20240307")
    chatbot.display_graph()
    chatbot.chat()