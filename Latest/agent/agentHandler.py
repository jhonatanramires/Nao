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
from dotenv import load_dotenv
import os


class AgentHandler:
    class State(TypedDict):
        messages: Annotated[list, add_messages]

    def __init__(self, api_key,tools,model_name,thread_id):
        self.tools = tools
        self.llm = ChatAnthropic(model_name=model_name, api_key=api_key)
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.memory = SqliteSaver.from_conn_string(":memory:")
        self.graph = self._setup_graph()
        self.config = {"configurable": {"thread_id": f"{thread_id}"}}

    def _chatbot(self, state: State):
        messages = state["messages"]
        print("Debug: Messages before LLM invocation:", messages)
        for message in messages:
            if isinstance(message, ToolMessage):
                # Asegúrate de que el resultado de la herramienta tenga el campo 'type'
                if 'type' not in message.content:
                    message.content['type'] = 'function'  # o el tipo apropiado
        result = self.llm_with_tools.invoke(messages)
        print("Debug: LLM response:", result)
        return {"messages": [result]}

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
        try:
            for event in self.graph.stream({"messages": [("user", user_input)]}, self.config, stream_mode="values"):
                event["messages"][-1].pretty_print()
        except Exception as e:
            print(f"Error occurred: {e}")
            # Aquí podrías agregar más lógica para manejar errores específicos

if __name__ == "__main__":
    # Dependencies for Custom Tools
    from tools import tools
    # Cargar las variables del archivo .env
    load_dotenv()

    # Acceder a las variables de entorno
    api_key = os.getenv('API_KEY')
    model_name = os.getenv('MODEL')
    chatbot = AgentHandler(api_key,tools,"claude-3-haiku-20240307",1)
    #chatbot.display_graph()
    chatbot.chat()

