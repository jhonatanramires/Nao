from fuzzywuzzy import fuzz

def prompt_formating(transcription):
    prompt = transcription
    
    prompt = ''.join(e for e in prompt if e.isalnum() or e == " ")

    return prompt