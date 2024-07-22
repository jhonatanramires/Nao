import subprocess
import sys
from playsound import playsound
import asyncio
sys.path.append(".\\utils")
sys.path.append(".\\SpeechToText")
sys.path.append(".\\TextToSpeech")
sys.path.append(".\\Agent")

from EdgeTts import amain,VOICE,OUTPUT_FILE
from Agent import AgentHandler
from tools import toolsAI
from ClassicRealTime import WhisperLoop
from promptFormating import prompt_formating

context = "You are the Nao Virtual Assistent"

nao = AgentHandler(0,toolsAI,context)

def AgentCall(prompt,Nao):
#   TODO ADD HERE THE CONECTION WITH NAO AND MAKE IT TALK USING THE PROMPT AS INPUT
    result = nao.run(prompt)
    result = prompt_formating(result)
    if Nao:
        result = prompt_formating(result)
        NaoSpeak_command = "python .\\Nao\\NaoSpeak.py  " + result
        process = subprocess.Popen(NaoSpeak_command.split(), stdout=subprocess.PIPE)
    else:
        asyncio.run(amain(result))
        playsound('C:\\Users\\Windows 10\\Desktop\\NaoAgent\\TextToSpeech\\test.mp3')
    print(result)


WhisperLoop(AgentCall,"Escuchame Nao")
