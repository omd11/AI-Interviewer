
from RealtimeTTS import TextToAudioStream, SystemEngine , GTTSEngine

def user_turn():
    return input()

def interviewer_turn(text, engine= SystemEngine()):
    stream = TextToAudioStream(engine)
    stream.feed(text)
    stream.play()

def on_character(character):
    print(character)