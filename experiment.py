import pyaudio
import wave
import speech_recognition as sr
import os
import csv
import numpy
import sys

# All data was found on EPA's website, at https://www.epa.gov/climate-indicators
# I have used external libraries such as CMU's Sphynx, a free tool for voice recognition
# All other libraries I have used are listed above as imported
# This is a little game that lets you know how much the world has changed since you were born. Categories include: precipitation anomaly, numbers of hurricanes, temperature anomaly, and number of heat-related deaths
# I hope that is it educational!
# I pledge my honor that I have abided by the Stevens Honor System

def record(name):
    CHUNK = 2048
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = name+".wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def readFile(name):
    # obtain path to "english.wav" in the same folder as this script
    from os import path
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)),name+ ".wav")

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file
    return [r, audio]

def birthday():
   os.system("say What year were you born?")
   record("birthday")
   resbirthday = readFile("birthday")
   response = "Since your birth you have been a witness to many things. These are some of your experiences regarding the climate."
   os.system("say you were born in" + resbirthday[0].recognize_sphinx(resbirthday[1]))
   d = {'zero':0,'one':1, 'two':2, 'three':3,'four':4, 'five':5,
          'six':6, 'seven':7, 'eight':8, 'nine':9, 'any':9,'ten':10,
        "eleven":11, "twelve":12,"thirteen":13,"fourteen":14,"fifteen":15,"sixteen":16,
        "seventeen":17,"eighteen":18,"nineteen":19, "twenty":20,"thirty":3,"fourty":4,"fifty":5,"sixty":6,
        "seventy":7,"eighty":8,"ninety":9}
   bdday = resbirthday[0].recognize_sphinx(resbirthday[1])
   num = ""
   for word in bdday.split():
       num += str(d[word])
   year = int(num)
   if year <1888 or year >2015:
       os.system("say sorry we do not have any data for the year" + str(year) + ". Goodbye.")
       sys.exit('listofitems not long enough')
   with open('precipitationAnomalies.csv', 'rb') as precfile:
       lst = precfile.readlines()
       for rows in lst:
           row = numpy.fromstring(rows, dtype=float, sep=",")
           if row[0]== float(year):
               x = numpy.fromstring(lst[len(lst)-1], dtype=float, sep=",")
               os.system("say The precipitation anomaly in " + str(int(row[0]))  + " was " + str(row[1]) + ". The precipitation anomaly for the last year recorded " + str(int(x[0])) + " was " + str(x[1]))
               response +="The precipitation anomaly in " + str(int(row[0]))  + " was " + str(row[1]) + ". The precipitation anomaly for the last year recorded " + str(int(x[0])) + " was " + str(x[1]) + '\n'

   with open('hurricanes.csv', 'rb') as hurrfile:
       lst = hurrfile.readlines()
       for rows in lst:
           row = numpy.fromstring(rows, dtype=float, sep=",")
           if row[0]== float(year):
                x = numpy.fromstring(lst[len(lst)-1], dtype=float, sep=",")
                os.system("say The amount of total hurricanes (adjusted) in the North Atlantic in " +  str(int(row[0]))  + " was " + str(row[1]) +  ". The amount of hurricanes (adjusted) in the North Atlantic for the last year recorded " + str(int(x[0])) + " was " + str(x[1]))
                response +="The amount of total hurricanes (adjusted) in the North Atlantic in " +  str(int(row[0]))  + " was " + str(row[1]) +  ". The amount of hurricanes (adjusted) in the North Atlantic for the last year recorded " + str(int(x[0])) + " was " + str(x[1]) + '\n'

   with open('temperaturechange.csv','rb') as tempfile:
       lst = tempfile.readlines()
       for rows in lst:
           row = numpy.fromstring(rows, dtype=float, sep=",")
           if row[0]== float(year):
                x = numpy.fromstring(lst[len(lst)-1], dtype=float, sep=",")
                os.system("say The temperature anomaly in the contiguous 48 states in " + str(int(row[0]))  + " was " + str(row[1]) + ". The temperature anomaly in the contiguous 48 states for the last year recorded " + str(int(x[0])) + " was " + str(x[1]))
                response += "The temperature anomaly in the contiguous 48 states in " + str(int(row[0]))  + " was " + str(row[1]) + ". The temperature anomaly in the contiguous 48 states for the last year recorded " + str(int(x[0])) + " was " + str(x[1]) + '\n'

   with open('heatrelateddeats.csv','rb') as heatfile:
       lst = heatfile.readlines()
       death = 0
       x = numpy.fromstring(lst[len(lst)-1], dtype=float, sep=",")
       for rows in lst:
           row = numpy.fromstring(rows, dtype=float, sep=",")
           if row[0]>=float(year):
                death += row[1]
       if death > 0:
           os.system("say The amount of heat related deaths since your birth until " + str(int(x[0])) + " is " + str(death))
           response += "The amount of heat related deaths since your birth until " + str(int(x[0])) + " is " + str(death) + '\n'
   print("**********SUMMARY***********\n" + response)
                                          
                   
def triviagame():
    os.system("say Would you like to learn about the climate the year you were born?") 
    record("response")
    res = readFile("response")

    # recognize speech using Sphinx
    try:
        if res[0].recognize_sphinx(res[1])=="yes":
            birthday()
        elif res[0].recognize_sphinx(res[1])=="no":
            os.system("say Goodbye sir or madam.")
        else:
            os.system("say Sorry I did not understand. Try again later. Good bye.")
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))


triviagame()
