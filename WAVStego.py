import wave, sys

# Helper Functions
## isolate the bit in a char with the specified index
def isolateBit(currChar, index):
  temp = ord(currChar)
  for i in range(0, index):
    temp = temp // 2

  return temp % 2

## return the LSB from the average of the samples in the frame
def averageLSB(frame):

  sum = 0
  for i in range(0,4):
    sum += frame[i]

  return (sum // 4) % 2

## adjust a frame so that the average LSB is flipped
def adjustFrame(frame):
  newFrame = ''
  upperBoundFlag = False
  lowerBoundFlag = False
  for sample in frame:
    if sample == 256:
      upperBoundFlag = True
    elif sample == 0:
      lowerBoundFlag = True

  if not upperBoundFlag and not lowerBoundFlag:
    for i in range(0,4):
      newFrame += chr(frame[i] + 1)

  elif upperBoundFlag and not lowerBoundFlag:
    for i in range(0,4):
      newFrame += chr(frame[i] - 1)

    

# hiding function
def hide(textFile, waveFile, stegoFile):

  #read and extract data from text file
  text = open(textFile, 'r')
  stringData = text.read()

  # get the number of characters in the text file
  textLength = len(stringData)
  if (textLength == 0):
    print("The text file is empty")
    sys.exit()

  #open .wav file for reading and create the .wav we are going to write to
  inputWave = wave.open(waveFile,'r')
  outputWave = wave.open(stegoFile, 'w')
  outputWave.setparams(inputWave.getparams())

  # get the number of frames in the wav file
  numFrames = inputWave.getnframes()
  if (textLength > 99999999):
    print("Text file too large")
    sys.exit()
  if (textLength * 8 > numFrames - 1):
    print("Sound file is not large enough")
    sys.exit()

  temp = textLength
  inputWave.readframes(1)
  frame = ''

  for i in range(0,4):
    if (temp > 0):
      frame += chr(temp%100)
    else:
      frame += chr(0)
    
    temp = temp // 100
  # write the length of the text file in the first frame  
  outputWave.writeframes(str.encode(frame))

  # read char from text file and loop through each bit 
  for i in range(0, textLength):
    for j in range(0,8):
      currentBit = isolateBit(stringData[i], 7-j)
      frame = inputWave.readframes(1)
      # calculate average of samples and compare LSB to current char bit.
      averageLSBVal = averageLSB(frame)

      # if not equal, change selected samples so that the average value LSB matches current char bit
      if averageLSBVal != currentBit:
        # create frame with new sample values
        newFrame = adjustFrame(frame)
        outputWave.writeframes(str.encode(str(newFrame)))
      else:
        # if equal make no changes 
        outputWave.writeframes(frame)

  # write remaining audio data
  outputWave.writeframes(inputWave.readframes(numFrames % textLength))
  inputWave.close()
  outputWave.close()
  text.close()
        

#extracting function

def extract(stegoFile,message):
    textMessage = open(message, 'w')
    inputWave = wave.open(stegoFile,'r')
    numFrames = inputWave.getnframes() #number frames in wav file
    frame = inputWave.readframes(1)
    textLength = frame[0] + 100*(frame[1]) + 10000*(frame[2]) + 1000000*(frame[3]) #grabs text length from first frame of audio
   
    value = 0
    for i in range(0, textLength):
      for j in range(0,8):
        value += averageLSB(inputWave.readframes(1))
        value << 1
      textMessage.write(chr(value))
    inputWave.close()
    textMessage.close()

def main(argv):
    textFile = ''
    waveFile = ''
    stegoFile = ''
    message = ''
    if (len(sys.argv) == 5 and sys.argv[1] == 'hide'):
        textFile = sys.argv[2]
        waveFile = sys.argv[3]
        stegoFile = sys.argv[4]
        hide(textFile,waveFile,stegoFile)
    elif (len(sys.argv) == 4 and sys.argv[1] == 'extract'):
        hiddenfile = sys.argv[2]
        message = sys.argv[3]
        extract(hiddenfile,message)
    else:
        print('Usage: WAVStego.py hide <textfile> <wavefile> <stegowavefile>\nUsage: WAVStego.py extract <stegowavefile> <resulttextfile>')
    
if __name__ == '__main__':
    main(sys.argv[1:])