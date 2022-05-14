import pyaudio
from numpy import short, frombuffer, log2, log
from scipy import fft
from time import sleep
from gpiozero import LED
import sys


# 7-segment display outputs
A = LED(9)
B = LED(11)
C = LED(5)
D = LED(6)
E = LED(13)
F = LED(19)
G = LED(26)

# other LED outputs
Tuned = LED(25)
Sharp = LED(8)
Flat = LED(7)

def displayReset():
    A.off()
    B.off()
    C.off()
    D.off()
    E.off()
    F.off()
    G.off()

def displayE():
    displayReset()
    A.on()
    B.off()
    C.off()
    D.on()
    E.on()
    F.on()
    G.on()

def displayA():
    displayReset()
    A.on()
    B.on()
    C.on()
    D.off()
    E.on()
    F.on()
    G.on()

def displayD():
    displayReset()
    A.on()
    B.on()
    C.on()
    D.on()
    E.on()
    F.on()
    G.off()

def displayG():
    displayReset()
    A.on()
    B.off()
    C.on()
    D.on()
    E.on()
    F.on()
    G.on()

def displayB():
    displayReset()
    A.on()
    B.on()
    C.on()
    D.on()
    E.on()
    F.on()
    G.on()

#notes in cents
Note_E = 5
Note_A = 0
Note_D = 7
Note_G = 2
Note_B = 10


MIN_FREQUENCY = 60
MAX_FREQUENCY = 700
#Max & Min cent value we care about
MAX_CENT = 11
MIN_CENT = 0
RELATIVE_FREQ = 440.0

SAMPLING_RATE = 48000
NUM_SAMPLES = 48000

if len(sys.argv) > 1:
    if (sys.argv[1] >= 415.0 and sys.argv[1] <= 445.0):
        RELATIVE_FREQ = sys.argv[1]

#Set up audio sampler - 
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
                  channels=1, rate=SAMPLING_RATE,
                  input=True,
                  frames_per_buffer=NUM_SAMPLES)

while True:
    while stream.get_read_available()< NUM_SAMPLES:
        sleep(0.01)
        
    audio_data  = frombuffer(stream.read(stream.get_read_available()), dtype=short)[-NUM_SAMPLES:]

    #window = hamming(NUM_SAMPLES)  
    intensities = abs(fft.fft(audio_data))[:int(NUM_SAMPLES/2)]

    freq_index = intensities[1:len(intensities)-1:].argmax()+1
    adjfreq = 0

    #y0,y1,y2 = log(intensities[freq_index-1:freq_index+2:])
    #interp = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
    freq = freq_index #+interp
    #print(freq)
    if freq < MIN_FREQUENCY or freq > MAX_FREQUENCY:
        adjfreq = -1

    else:
        adjfreq = freq



    if (adjfreq != -1):
        adjfreq = 1200 *log2(RELATIVE_FREQ/adjfreq)/100
        adjfreq = adjfreq % 12
        
        Tuned.off()
        Sharp.off()
        Flat.off()
        #print(adjfreq)
        #Case statements
        if abs(adjfreq - Note_E ) < 1.2:
            displayE()
            #In Tune E
            if abs(adjfreq - Note_E) < 0.2  :
                print("You played an E!")
                Tuned.on()
            #Sharp E
            elif (adjfreq - Note_E) < 0  :
                print("You are sharp E!")
                Sharp.on()
            #Flat E
            elif (adjfreq - Note_E) > 0  :
                print("You are flat E!")
                Flat.on()
        elif abs(adjfreq - Note_B ) < 1.2:
            displayB()
            #In Tune B
            if abs(adjfreq - Note_B) < 0.2  :
                print("You played a B!")
                Tuned.on()
            #Sharp B
            elif (adjfreq - Note_B) < 0  :
                print("You are sharp B!")
                Sharp.on()
            #Flat B
            elif (adjfreq - Note_B) > 0  :
                print("You are flat B!")
                Flat.on()
        elif abs(adjfreq - Note_G ) < 1.2:
            displayG()
            #In Tune g
            if abs(adjfreq - Note_G) < 0.2  :
                print("You played a G!")
                Tuned.on()
            #Sharp G
            elif (adjfreq - Note_G) < 0  :
                print("You are sharp G!")
                Sharp.on()
            #Flat G
            elif (adjfreq - Note_G) > 0  :
                print("You are flat G!")
                Flat.on()
        
        elif abs(adjfreq - Note_D ) < 1.2:
            displayD()
            #In Tune D
            if abs(adjfreq - Note_D) < 0.2  :
                print("You played a D!")
                Tuned.on()
            #Sharp D
            elif (adjfreq - Note_D) < 0  :
                print("You are sharp D!")
                Sharp.on()
            #Flat D
            elif (adjfreq - Note_D) > 0  :
                print("You are flat D!")
                Flat.on()
        elif abs(adjfreq - Note_A ) < 1.2:
            displayA()
            #In tune A
            if abs(adjfreq - Note_A) < 0.2  :
                print("You played an A!")
                Tuned.on()
            #Sharp A
            elif (adjfreq - Note_A) < 0  :
                print("You are sharp A!")
                Sharp.on()
            #Flat A
            elif (adjfreq - Note_A)  > 0  :
                print("You are flat A!")
                Flat.on()
                
        elif abs(adjfreq - 12 ) < 1.2:
            displayA()
            if abs(adjfreq - 12) < 0.2  :
                print("You played an A!")
                Tuned.on()
            elif (adjfreq - 12) < 0  :
                print("You are sharp A!")
                Sharp.on()
            elif (adjfreq - 12)  > 0  :
                print("You are flat A!")
                Flat.on()
    else:
        Tuned.off()
        Sharp.off()
        Flat.off()
        
    sleep(0.01)
