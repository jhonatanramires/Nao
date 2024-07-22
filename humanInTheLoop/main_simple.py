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

# Dependencies for Custom Tools
from tools import tools

#LLM Chat Setup
llm = ChatAnthropic(model_name="claude-3-haiku-20240307",api_key="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")
llm_with_tools = llm.bind_tools(tools)

#Memory Management
memory = SqliteSaver.from_conn_string("memory")

# State Class Setup
class State(TypedDict):
  messages: Annotated[list, add_messages]

# ChatBot Function Setup
def chatbot(state: State):
  return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Graph Setup
graph_builder = StateGraph(State)

# ChatBotNode Setup
graph_builder.add_node("chatbot", chatbot)

# ToolNode Setup
tool_node = ToolNode(tools)
graph_builder.add_node("tools", tool_node)

# Graph Conditional Edges Setup
graph_builder.add_conditional_edges(
  "chatbot",
  tools_condition,
)

# Graph Edges Setup
graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("tools", "chatbot")

# Graph Compiling
graph = graph_builder.compile(
    checkpointer=memory
)

#Graph Display
try:
    img_data = graph.get_graph().draw_mermaid_png()
    if img_data:
        img = PILImage.open(io.BytesIO(img_data))
        img.show()
    else:
        print("La imagen no se ha generado correctamente.")
except Exception as e:
    print(f"Error generando la imagen: {e}")

#configurations
config = {"configurable": {"thread_id": "1"}}

#Chat Main Loop
while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    for event in graph.stream({"messages": [("user", user_input)]},{"configurable": {"thread_id": "2"}},stream_mode="values"):
      event["messages"][-1].pretty_print()