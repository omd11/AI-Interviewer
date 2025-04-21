from RealtimeSTT import AudioToTextRecorder
from RealtimeTTS import TextToAudioStream, SystemEngine , GTTSEngine



def process_text(text):
    print(text)



"""if __name__ == '__main__':
    to_print = ""
    print("wait")
    recorder = AudioToTextRecorder()

    while True:
        recorder.text(process_text)
        if keyboard.is_pressed('q'):
            print(to_print)
            break"""
        
engine = SystemEngine() # replace with your TTS engine
stream = TextToAudioStream(engine)
stream.feed("Hello world! How are you today?")
stream.play()