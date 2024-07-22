import speech_recognition as sr
from sys import platform

def setup_microphone(args):
    if 'linux' in platform:
        mic_name = args.default_microphone
        if not mic_name or mic_name == 'list':
            print("Available microphone devices are: ")
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                print(f"Microphone with name \"{name}\" found")   
            return None
        else:
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                if mic_name in name:
                    return sr.Microphone(sample_rate=16000, device_index=index)
    else:
        return sr.Microphone(sample_rate=16000)