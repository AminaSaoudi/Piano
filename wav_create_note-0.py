# -*- coding: Utf-8 -*-
# http://blog.acipo.com/wave-generation-in-python/
# https://www.tutorialspoint.com/read-and-write-wav-files-using-python-wave
import wave, struct, math, random

obj = wave.open('sound.wav','w')
sampleRate = 44100.0                # hertz
duration = 2.0                      # seconds
frequency = 261.625565300599
############440.0                   # hertz
obj.setnchannels(1)                 # mono
obj.setsampwidth(2)
obj.setframerate(sampleRate)
for i in range(99999):
   value = random.randint(-32767, 32767)
   data = struct.pack('<h', value)
   obj.writeframesraw( data )
obj.close()

