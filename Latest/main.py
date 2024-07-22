from dotenv import load_dotenv
import os

from agent.agentHandler import AgentHandler

# Cargar las variables del archivo .env
load_dotenv()

# Acceder a las variables de entorno
api_key = os.getenv('API_KEY')
model_name = os.getenv('MODEL')
db_pass = os.getenv('DB_PASS')

chatbot = AgentHandler(api_key,tools,"claude-3-haiku-20240307")
chatbot.display_graph()
chatbot.chat()