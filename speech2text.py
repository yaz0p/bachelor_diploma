import speech_recognition as sr
import soundfile as sf
import os

def recognize_speech(audio_file):
    data, samplerate = sf.read(audio_file)
    sf.write('voice.wav', data, samplerate)

    recognizer = sr.Recognizer()
    
    with open('voice.wav', 'rb') as audio_file:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            recognizer.adjust_for_ambient_noise(source)
        
        try:
            text = recognizer.recognize_google(audio_data, language='ru-RU')
            os.remove('voice.wav')
            return text
        except sr.UnknownValueError:
            return "Попробуй ещё раз. Не могу разобрать, что ты говоришь."
        except sr.RequestError:
            return "Ну здесь наши полномочия все :(."
    
