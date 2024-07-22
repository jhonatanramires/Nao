import sys

sys.path.append(".\\utils")
sys.path.append(".\\SpeechToText")
sys.path.append(".\\TextToSpeech")
sys.path.append(".\\Agent")

from tools import toolsAI
import subprocess
import asyncio
from AgentOllama import AgentHandler

nao = AgentHandler(toolsAI)

def AgentCall(prompt):
  result = nao.run(prompt)
  result = result
  print(result)

AgentCall("give me the temperature")