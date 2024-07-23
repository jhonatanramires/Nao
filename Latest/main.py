from dotenv import load_dotenv
import os

from agent.agentHandler import AgentHandler
from agent.tools import tools

# Cargar las variables del archivo .env
load_dotenv()

# Acceder a las variables de entorno
api_key = os.getenv('API_KEY')
model_name = os.getenv('MODEL')

print(api_key,model_name)

chatbot = AgentHandler(api_key,tools,"claude-3-haiku-20240307",1)
chatbot.display_graph()
chatbot.chat()