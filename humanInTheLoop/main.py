from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# Dependencies for Graph Display
from PIL import Image as PILImage
from IPython.display import Image, display
import io

class State(TypedDict):
  input: str

def step_1(state):
  print("---Step 1---")
  pass

def step_2(state):
  print("---Step 2---")
  pass

def step_3(state):
  print("---Step 3---")
  pass

builder = StateGraph(State)

# Adding Nodes
builder.add_node("step_1", step_1)
builder.add_node("step_2", step_2)
builder.add_node("step_3", step_3)

# Setting Edges
builder.add_edge(START,"step_1")
builder.add_edge("step_1","step_2")
builder.add_edge("step_2","step_3")
builder.add_edge("step_3",END)

# Set Up Memory
memory = MemorySaver()

# Adding graph
graph = builder.compile(
  checkpointer=memory,
  interrupt_before=["step_3"]
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

# Input
initial_input = {"input": "hello world"}

# Thread
thread = {"configurable": {"thread_id": "1"}}

for event in graph.stream(initial_input,thread,stream_mode="values"):
  print(event)

user_approval = input("Do you want to go to Step 3? (yes/no): ")

if user_approval.lower() == 'yes':
  # If approved, continue the graph execution
  for event in graph.stream(None, thread, stream_mode="values"):
    print(event)
else:
  print("Operation cancelled by user")
