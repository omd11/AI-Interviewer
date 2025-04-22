from RealtimeSTT import AudioToTextRecorder
from RealtimeTTS import TextToAudioStream, SystemEngine , GTTSEngine

def user_turn():
    with AudioToTextRecorder() as recorder:
        recorder.post_speech_silence_duration = 5
        return recorder.text()

def interviewer_turn(text, engine= SystemEngine()):
    stream = TextToAudioStream(engine)
    stream.feed(text)
    stream.play_async()
