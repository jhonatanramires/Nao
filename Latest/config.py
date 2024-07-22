
from utils.argsToEnv import save_args_to_env
import os
import argparse

defaults = {
    "api_key": os.getenv("OPENAI_API_KEY") ,
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "voice": "com.apple.eloquence.en-US.Grandpa",
    "volume": 1.0,
    "rate": 200,
    "thread_id": "1",
    "ability": "Psychology",
    "base_url": "https://api.openai.com/v1",
}

parser = argparse.ArgumentParser()
parser.add_argument("--list_voices", action="store_true", help="List the available voices for the text-to-speech engine")
parser.add_argument("--test_voice", action="store_true", help="Test the text-to-speech engine")
parser.add_argument("--ptt", action="store_true", help="Use push-to-talk mode")
parser.add_argument("--ability", type=str, help="The ability of the assistant", default=defaults["ability"])
parser.add_argument("--api_key", type=str, help="The OpenAI API key")
parser.add_argument("--model", type=str, help="The name of the model to use", default=defaults["model"])
parser.add_argument("--temperature", type=float, help="The temperature to use for the OpenAI model", default=defaults["temperature"])
parser.add_argument("--voice", type=str, help="The voice to use for the text-to-speech engine", default=defaults["voice"])
parser.add_argument("--volume", type=float, help="The volume to use for the text-to-speech engine", default=defaults["volume"])
parser.add_argument("--rate", type=int, help="The rate at which the words are spoken for the text-to-speech engine", default=defaults["rate"])

#for the chatbot memory
parser.add_argument("--thread_id", type=str, help="The thread ID to use for the chat history", default=defaults["thread_id"])

parser.add_argument("--base_url", type=str, help="The base URL to use for the OpenAI API", default=defaults["base_url"])
args = parser.parse_args()


# Set up the ChatGPT API client
if args.base_url == defaults["base_url"]:
    if "OPENAI_API_KEY" not in os.environ and args.api_key is None:
        raise ValueError("You must set the OPENAI_API_KEY environment variable to use the OpenAI API")
    else:
      api_key = args.api_key or os.getenv("OPENAI_API_KEY")
else:
    if args.api_key is None:
        api_key = 'sk-no_key'
    else:
      api_key = args.api_key
      
args.llm_model = args.model
args.temperature = min(max(args.temperature, 0.0), 1.0)
args.interface_voice = args.voice
args.volume = min(max(args.volume, 0.0), 1.0)
args.rate = min(max(args.rate, 20), 500)
args.thread_id = args.thread_id
args.base_url = args.base_url
args.ptt = args.ptt

save_args_to_env(args)