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
from tools import tools, RequestAproval

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
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# Graph Setup
graph_builder = StateGraph(State)

# ChatBotNode Setup
graph_builder.add_node("chatbot", chatbot)

# ToolNode Setup
tool_node = ToolNode(tools)
graph_builder.add_node("tools", tool_node)

# Define nodes and conditional edges


# Define the function that determines whether to continue or not
def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]
    # If there is no function call, then we finish
    if not last_message.tool_calls:
        return "end"
    # Otherwise if there is, we continue
    else:
        return "continue"

# Set The Condition To Pass Between Nodes
def select_next_node(state: State):
  if state["ask_human"]:
    return "human"
  # Otherwise, we can route as before
  return tools_condition(state)

# Graph Conditional Edges Setup
graph_builder.add_conditional_edges(
  "chatbot",
  select_next_node,
  {"human": "human", "tools": "tools", "__end__": "__end__"},
)

# Graph Edges Setup
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("human", "chatbot")
graph_builder.add_edge(START,"chatbot")

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
user_input = "I need expert assistance"
# The config is the **second positional argument** to stream() or invoke()!
events = graph.stream(
  {"messages": [("user", user_input)]}, config, stream_mode="values"
)
for event in events:
  event["messages"][-1].pretty_print()