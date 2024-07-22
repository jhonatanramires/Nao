import speech_recognition as sr
from fuzzywuzzy import fuzz
from datetime import datetime, timedelta
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep

from utils.audio_processing import process_audio
from utils.microphone_setup import setup_microphone
from utils.whisperUtils import load_model, get_parser

def WhisperLoop(LLMCaller, name, debug=True):
    parser = get_parser()
    args = parser.parse_args()

    source = setup_microphone(args)
    if not source:
        return

    recorder = sr.Recognizer()
    recorder.energy_threshold = args.energy_threshold
    recorder.dynamic_energy_threshold = False

    audio_model = load_model("tiny")
    temp_file = NamedTemporaryFile().name
    data_queue = Queue()

    with source:
        recorder.adjust_for_ambient_noise(source)

    def record_callback(_, audio: sr.AudioData) -> None:
        data = audio.get_raw_data()
        data_queue.put(data)

    recorder.listen_in_background(source, record_callback, phrase_time_limit=args.record_timeout)

    print("Model loaded. Ready to start.\n")

    phrase_time = None
    last_sample = bytes()
    transcription = ['']
    active = False
    prompt = ""

    while True:
        try:
            now = datetime.utcnow()
            if not data_queue.empty():
                phrase_complete = False
                if phrase_time and now - phrase_time > timedelta(seconds=args.phrase_timeout):
                    last_sample = bytes()
                    phrase_complete = True
                phrase_time = now

                while not data_queue.empty():
                    data = data_queue.get()
                    last_sample += data

                text = process_audio(audio_model, temp_file, last_sample, source)

                if debug:
                    print("Recognized: " + text)

                if phrase_complete:
                    transcription.append(text)
                    prompt = transcription[-1]

                    if fuzz.ratio(name, prompt) > 50:
                        active = True
                        print(f"Activated! Hello, {name}!")
                    elif active and prompt:
                        response = LLMCaller(prompt, True)
                        print(f"Assistant: {response}")
                        active = False
                else:
                    transcription[-1] = text

                print(f"Current state: Prompt = '{prompt}', Active = {active}")

                sleep(0.25)
        except KeyboardInterrupt:
            break

    print("\n\nConversation:")
    for line in transcription:
        print(line)