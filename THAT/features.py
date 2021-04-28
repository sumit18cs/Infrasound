
import time
import string
# import pyaudio
import speech_recognition as sr
from plyer import notification 
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#--------------------------------------------------------------------------------------------------------------------- 
# Utility Function to convert speech to text
#---------------------------------------------------------------------------------------------------------------------
def recognize_speech_from_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
      
    response = {"success": True,"error": None,"transcription": None}

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

def perform_this_task(latency,wait_parameter, start_time,array_RoS):
    wait_count=0
    text=""
    while 1:
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        guess = recognize_speech_from_mic(recognizer, microphone)

        if guess["transcription"] == None:
            print("\n\nYou are not speaking...okay then bye")
            if wait_count < wait_parameter:
                wait_count = wait_count + 1   
                continue
            else:
                return

        wait_count = 0
        text=text+ guess["transcription"] 
        time_of_speech = time.time() - start_time - latency   #Subtracting latency
        words_in_speech = sum([i.strip(string.punctuation).isalpha() for i in guess["transcription"].split()])
        rate_of_speech = (words_in_speech*60)/ time_of_speech

        # Printing messages to test results. Comment the lines after final testing.
        print("\nYou said      : ",guess["transcription"])
        print("Words in speech : ", words_in_speech) 
        print("Time Taken      : ", str(round(time_of_speech,2))+" seconds.")      
        print("Rate of Speech  : " + str(round(rate_of_speech,2)) +" WPM.\n") # Rate of speech in Words per minute

        array_RoS.append(round(rate_of_speech,2))
        return array_RoS, words_in_speech, text        


def getRoS():
    array_RoS = list()
    average_RoS = 0
    array_RoS,words_in_speech, text = perform_this_task(3,0,time.time(),array_RoS)
    
    if array_RoS != None:
        for ros in array_RoS:
            average_RoS = average_RoS + ros
        average_RoS = average_RoS / len(array_RoS)
        
    return average_RoS, str(words_in_speech), text  




import os
from os import path
import moviepy.editor as mp
def convertmp4towav(path) :
    print(path)
    clip = mp.VideoFileClip(path)
    clip.audio.write_audiofile("video.wav",codec='pcm_s16le')
    return "video.wav"


def getTranscript(path):
    text=[]
    filename=convertmp4towav(path)
    r = sr.Recognizer()
    audio_file = sr.AudioFile(filename)
    with audio_file as source:
        audio = r.record(source) 

    try:
        text= r.recognize_google(audio)
    except sr.UnknownValueError:
        print("1")
    except sr.RequestError as e:
        print("2 ", e)    
        
    print(text)
    return text
