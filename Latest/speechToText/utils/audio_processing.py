import io
import speech_recognition as sr

def process_audio(audio_model, temp_file, last_sample, source):
    audio_data = sr.AudioData(last_sample, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
    wav_data = io.BytesIO(audio_data.get_wav_data())

    with open(temp_file, 'w+b') as f:
        f.write(wav_data.read())

    segments, _ = audio_model.transcribe(temp_file, beam_size=5)
    segment = list(segments)
    
    try: 
        return segment[0].text
    except IndexError:
        return ""