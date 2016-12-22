

"""Import Libraries"""
import json,pyaudio,wave,os
from urllib.request import urlopen,Request




"""Class Definition"""
class AudioRecorderClass:
    def recordAudio(outputName, length):
        bytes = 1024
        recordLength = length
        format = pyaudio.paInt16
        channels = 1
        outputFile = outputName
        rate = 12000
        audioRecorder = pyaudio.PyAudio()
        recorder = audioRecorder.open(format = format, channels = channels, rate = rate, input = True, frames_per_buffer = bytes)
        myArr = []
        for i in range(0, int(rate/bytes * recordLength)):
            data = recorder.read(bytes)
            myArr.append(data)
        print("Ok I'm Done :( Wait :D")
        recorder.stop_stream()
        recorder.close()
        audioRecorder.terminate()
        waveFile = wave.open(outputFile, "wb")
        waveFile.setnchannels(channels)
        waveFile.setsampwidth(audioRecorder.get_sample_size(format))
        waveFile.setframerate(rate)
        waveFile.writeframes(b''.join(myArr))
        waveFile.close()
        #If You are running me on Mac OS simply do : Brew Install Flac
        os.system("flac -f %s" % outputName)




"""Class Definition"""
class RecognizerClass:
    def sendRequest(audioFile):
        GOOGLEAPIKEY = "INSERT GOOGLE API KEY HERE :)"
        APIURL = 'https://www.google.com/speech-api/v2/recognize?xierr=1&client=chromium&lang=fa-IR&key=' + GOOGLEAPIKEY
        headerParameters = {'Content-Type': 'audio/x-flac; rate=12000'}
        fileContent = open(audioFile, 'rb')
        fileData = fileContent.read()
        requestParam = Request(APIURL, data=fileData, headers=headerParameters)
        response = urlopen(requestParam)
        responseByte = response.read()
        responseString = responseByte.decode("utf-8")
        if len(responseString) > 16:
            responseString = responseString.split('\n', 1)[1]
            a = json.loads(responseString)['result'][0]
            transcript = ""
            confidence = 0
            if 'confidence' in a['alternative'][0]:
                confidence = a['alternative'][0]['confidence']
                confidence = confidence * 100
            if 'transcript' in a['alternative'][0]:
                transcript = a['alternative'][0]['transcript']
                return transcript




"""Class Definition"""
class MainClass:
    print("Start Speaking to me :)")
    filePath = "OutputFile"
    AudioRecorderClass.recordAudio(filePath + ".wav",2)
    with open("response.txt", 'a') as out:
        out.write(RecognizerClass.sendRequest(filePath + ".flac"))
        out.write("\n")
        print("I'm Finished check out response.txt")
