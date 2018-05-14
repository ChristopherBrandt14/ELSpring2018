# This is commented out so the code can be run without using the bot
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
# Uncomment this to run the bot

runWithBot = True # Set to true to make the bot move, set to false to run code as theoretical

import time
from time import sleep

pulse = True # Controls if movement functions stop after a brief period of running

# Change these depending on battery strength
pulseTime = .075 # Controls the amount of time movement functions run for when pulsing
# The amount of pulses when turning/Uturning/checking for S
turnPulses = 25
uTurnPulses = 50
sCheckPulses = 5

pins = [22, 32, 29, 31, 15, 13, 11, 7] # Pins for the sensor bar
run = True
threshold = 0.0007 # The maximum value that can be white as opposed to black
readColors = True # When true ReadAll() will return the color values (0 = White, 1 = Black) and when False ReadAll() will return time data

# -----------

# Global values. I should change this later when I'm better with python
global state
state  = "firstRun"
global path
path = ""

# ======= Motor Functions =======

MLE = 40 # Motor Left E
MLA = 38 # Motor Left A
MLB = 36 # Motor Left B

MRE = 33 # Motor Right E
MRA = 35 # Motor Right A
MRB = 37 # Motor Right B

def gpioSetup(): # Run this at start to set up the GPIO pins for the motors
    if runWithBot == True:
        GPIO.setup(MLE,GPIO.OUT)
        GPIO.setup(MLA,GPIO.OUT)
        GPIO.setup(MLB,GPIO.OUT)

        GPIO.setup(MRE,GPIO.OUT)
        GPIO.setup(MRA,GPIO.OUT)
        GPIO.setup(MRB,GPIO.OUT)
        print("GPIO pins set up")
    else:
        print("GPIO pins would be set up here")

def gpioCleanup():
    if runWithBot == True:
        GPIO.cleanup()
        print("GPIO pins cleaned up")
    else:
        print("GPIO pins would be cleaned up here")

def forward(): # Sets motors to forward, if pulse is true it will stop shortly after
    if runWithBot == True:
        GPIO.output(MLE,GPIO.HIGH)
        GPIO.output(MLA,GPIO.HIGH)
        GPIO.output(MLB,GPIO.LOW)
        
        GPIO.output(MRE,GPIO.HIGH)
        GPIO.output(MRA,GPIO.HIGH)
        GPIO.output(MRB,GPIO.LOW)
        print("Motors set forward")
        if pulse == True:
            sleep(pulseTime)
            stopAll()
            sleep(pulseTime)
    else:
        print("Move forward")

def backward(): # Sets motors to backward, if pulse is true it will stop shortly after
    if runWithBot == True:
        GPIO.output(MLE,GPIO.HIGH)
        GPIO.output(MLA,GPIO.LOW)
        GPIO.output(MLB,GPIO.HIGH)
        
        GPIO.output(MRE,GPIO.HIGH)
        GPIO.output(MRA,GPIO.LOW)
        GPIO.output(MRB,GPIO.HIGH)
        print("Motors set backward")
        if pulse == True:
            sleep(pulseTime)
            stopAll()
            sleep(pulseTime)
    else:
        print("Move backward")

def adjustLeft():
    if runWithBot == True:
        GPIO.output(MLE,GPIO.LOW)
        
        GPIO.output(MRE,GPIO.HIGH)
        GPIO.output(MRA,GPIO.HIGH)
        GPIO.output(MRB,GPIO.LOW)
        print("Motors adjust left")
        if pulse == True:
            sleep(pulseTime)
            stopAll()
            sleep(pulseTime)
    else:
        print("Adjust left")

def adjustRight():
    if runWithBot == True:
        GPIO.output(MLE,GPIO.HIGH)
        GPIO.output(MLA,GPIO.HIGH)
        GPIO.output(MLB,GPIO.LOW)

        GPIO.output(MRE,GPIO.LOW)
        print("Motors adjust right")
        if pulse == True:
            sleep(pulseTime)
            stopAll()
            sleep(pulseTime)
    else:
        print("Adjust right")

def turnLeft():
    if runWithBot == True:
        GPIO.output(MLE,GPIO.HIGH)
        GPIO.output(MLA,GPIO.LOW)
        GPIO.output(MLB,GPIO.HIGH)
        
        GPIO.output(MRE,GPIO.HIGH)
        GPIO.output(MRA,GPIO.HIGH)
        GPIO.output(MRB,GPIO.LOW)
        print("Motors turn left")
        if pulse == True:
            sleep(pulseTime)
            stopAll()
            sleep(pulseTime)
    else:
        print("Turn left")

def turnRight():
    if runWithBot == True:
        GPIO.output(MLE,GPIO.HIGH)
        GPIO.output(MLA,GPIO.HIGH)
        GPIO.output(MLB,GPIO.LOW)
        
        GPIO.output(MRE,GPIO.HIGH)
        GPIO.output(MRA,GPIO.LOW)
        GPIO.output(MRB,GPIO.HIGH)
        print("Motors turn right")
        if pulse == True:
            sleep(pulseTime)
            stopAll()
            sleep(pulseTime)

    else:
        print("Turn right")

def stopAll():
    if runWithBot == True:
        GPIO.output(MLE,GPIO.LOW)
        GPIO.output(MRE,GPIO.LOW)
        print("Motors set stop")
    else:
        print("Stop")
# ===== End Motor Functions =====

# ======= Sensor Functions =======
def readSensors():
    if runWithBot == True:
        readingArray = ReadAllAccurate()
        readingString = ""
        for i in range(0,8):
            readingString = readingString + str(readingArray[i])
        # printReading(readingArray)
        return readingString
    else:
        manualReading = input("Enter a sensor reading: ")
        return manualReading

def ReadAll(): # This function returns readings from the light sensor

    # Reset readings.
    reading = [99, 99, 99, 99, 99, 99, 99, 99]
    check = [False, False, False, False, False, False, False, False]
    
    # Set all sensor pins to output
    for pin in range(0,8):
        GPIO.setup(pins[pin], GPIO.OUT)
    
    # Drive the output high, charging the capacitor
    for pin in range(0,8):
        GPIO.output(pins[pin], True)

    # Wait for the capacitor to charge.
    time.sleep(0.01)

    # Record the starting time
    starttime = time.time()

    # Set pins to input
    for pin in range(0,8):
        GPIO.setup(pins[pin], GPIO.IN)
    
    # This loop runs until every sensor reads low
    while (check[0] and check[1] and check[2] and check[3] and check[4] and check[5] and check[6] and check[7]) == False:
        for i in range(0,8):
            if GPIO.input(pins[i]) == False and check[i] == False:
                endtime = time.time()
                if endtime - starttime < reading[i]:
                    reading[i] = endtime - starttime
                    check[i] = True
    # This compares all of the readings to the time threshold (Found at top of file)
    # to tell if it sees black or white and returns an array of 1's and 0's
    if readColors == True:
        colors = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(0,8):
            if reading[i] < threshold:
                colors[i] = 0
            else:
                colors[i] = 1
        return colors
    # This returns the raw timings recorded by the sensor.
    # This is helpful for changing the threshold
    else:
        return reading

def ReadAllAccurate():
    # This checks the sensor 3 times to make sure it is getting the right reading 
    # before returning data. Does not check if returning times instead of colors

    while readColors: # loops until all three readings are the same.
        reading1 = ReadAll()
        reading2 = ReadAll()
        reading3 = ReadAll()
        reading4 = ReadAll()
        reading5 = ReadAll()
        reading6 = ReadAll()
        if reading1 == reading2 and reading3 == reading4 and reading5 == reading6 and reading1 == reading3 and reading3 == reading5:
            return reading1

    # Just returns the raw times from one check when not returning colors.
    return ReadAll()

def printReading(reading):
    print("Readings:")
    for i in range(0,8):
        print("Sensor " + str(i) + " = " + str(reading[i]))
# ===== End Sensor Functions =====

# ======= State Functions =======

def followLine():
    # This follows the line or handles an intersection
    global state
    try: 
        reading = readSensors()
    except KeyboardInterrupt:
        reading = ""
    # ///// These are for staying on the line /////
    # ----- Adjust cases for 1 black -----
    # Adjust left
    if reading == "10000000":
        adjustLeft()
    elif reading == "01000000":
        adjustLeft()
    elif reading == "00100000":
        adjustLeft()
    # Forward
    elif reading == "00010000":
        forward()
    elif reading == "00001000":
        forward()
    # Adjust right
    elif reading == "00000100":
        adjustRight()
    elif reading == "00000010":
        adjustRight()
    elif reading == "00000001":
        adjustRight()
    
    # ----- Adjust cases for 2 black -----
    # Adjust left
    elif reading == "11000000":
        adjustLeft()
    elif reading == "01100000":
        adjustLeft()
    elif reading == "00110000":
        adjustLeft()
    # Forward
    elif reading == "00011000":
        forward()
    # Adjust right
    elif reading == "00001100":
        adjustRight()
    elif reading == "00000110":
        adjustRight()
    elif reading == "00000011":
        adjustRight()
    
    # ----- Adjust cases for 3 black -----
    # Adjust left
    elif reading == "11100000":
        adjustLeft()
    elif reading == "01110000":
        adjustLeft()
    # Forward
    elif reading == "00111000":
        forward()
    elif reading == "00011100":
        forward()
    # Adjust right
    elif reading == "00001110":
        adjustRight()
    elif reading == "00000111":
        adjustRight()

    # ----- Cases where an intersection may be there -----
    # Intersection with left choice
    elif reading == "11110000":
        makeDecision(reading)
    elif reading == "11111000":
        makeDecision(reading)
    elif reading == "11111100":
        makeDecision(reading)
    # Intersection with left and right choice
    elif reading == "11111111":
        makeDecision(reading)
    # Intersection with right choice
    elif reading == "00111111":
        makeDecision(reading)
    elif reading == "00011111":
        makeDecision(reading)
    elif reading == "00001111":
        makeDecision(reading)
    # Came to the end of the line
    elif reading == "00000000":
        makeDecision(reading)
    # Manual readings
    elif reading == "L":
        makeDecision(reading)
    elif reading == "R":
        makeDecision(reading)
    elif reading == "LR":
        makeDecision(reading)

    # ----- End state cases -----
    elif reading == "10000001":
        state = "Finish"
    elif reading == "11000001":
        state = "Finish"
    elif reading == "10000011":
        state = "Finish"
    elif reading == "11000011":
        state = "Finish"
    
    elif reading == "10001001":
        state = "Finish"
    elif reading == "11001001":
        state = "Finish"
    elif reading == "10001011":
        state = "Finish"
    elif reading == "11001011":
        state = "Finish"
        
    elif reading == "10010001":
        state = "Finish"
    elif reading == "11010001":
        state = "Finish"
    elif reading == "10010011":
        state = "Finish"
    elif reading == "11010011":
        state = "Finish"

    elif reading == "10011001":
        state = "Finish"
    elif reading == "11011001":
        state = "Finish"
    elif reading == "10011011":
        state = "Finish"
    elif reading == "11011011":
        state = "Finish"

    # Used for manual testing to end the maze solving loop
    elif reading == "end":
        state = "Finish"
    # Handles unexpected results
    else:
        stopAll()
        print("Encountered an unknown result")
# ===== End State Functions =====

# ======= Decision Functions =======
def makeDecision(reading):
    global path
    global state
    doubleCheck = "" # input("I'm reading " + reading + ", is this correct? (enter/n)")
    if doubleCheck == "":
        if reading == "00000000":
            if state == "firstRun":
                if doubleCheck == "":
                    makeUTurn()
                    path = path + "U"
                    print("Path taken was updated by adding choice U")
                    print("Path: " + path)
                    input()
                elif doubleCheck == "n":
                    print("Let's try that again")
            elif state == "secondRun":
                if doubleCheck == "":
                    input("This shouldn't happen")
                elif doubleCheck == "n":
                    input("Put me back on the line and press enter.")
                
        
        # ----- Intersections with left choice and/or straight option
        elif reading == "11110000" or reading == "11111000" or reading == "11111100" or reading =="L":
            intersectionL()
        # ----- Intersections with left and right and/or straight option
        elif reading == "11111111" or reading == "LR":
            intersectionLR()
        # ----- Intersections with right and maybe straight
        elif reading == "00011111" or reading == "00001111" or reading == "00111111" or reading == "R":
            intersectionR()
        # Handles unexpected results.
        else:
            print("Encountered an unknown result but it should have already been caught...")
    elif doubleCheck == "n":
        input("Trying again")

# Handles an intersection with an L
def intersectionL():
    global path
    if checkForS() == True:
        print("Option(s) given are: Left and Straight")
        if state == "firstRun":
            makeLeftTurn()
            addPath("L")
        elif state == "secondRun":
            pathList = list(path)
            choice = pathList.pop(0)
            path = ''.join(pathList)
            if choice == "L":
                makeLeftTurn()
            elif choice == "S":
                makeStraight()
    else:
        print("Option(s) given are: Left")
        makeLeftTurn()

# Handles an intersection with an R
def intersectionR():
    global path
    if checkForS() == True:
        print("Option(s) given are: Right and Straight")
        if state == "firstRun":
            makeStraight()
            addPath("S")
        elif state == "secondRun":
            pathList = list(path)
            choice = pathList.pop(0)
            path = ''.join(pathList)
            if choice == "R":
                makeRightTurn()
            elif choice == "S":
                makeStraight()
    else:
        print("Option(s) given are: Right")
        makeRightTurn()

# Handles an intersection with an L and R
def intersectionLR():
    global path
    if checkForS() == True:
        print("Option(s) given are: Left, Right, and Straight")
        if state == "firstRun":
            makeLeftTurn()
            addPath("L")
        elif state == "secondRun":
            pathList = list(path)
            choice = pathList.pop(0)
            path = ''.join(pathList)
            if choice == "L":
                makeLeftTurn()
            elif choice == "S":
                makeStraight()
            elif choice == "R":
                makeRightTurn()
    else:
        print("Option(s) given are: Left and Right")
        if state == "firstRun":
            makeLeftTurn()
            addPath("L")
        elif state == "secondRun":
            pathList = list(path)
            choice = pathList.pop(0)
            path = ''.join(pathList)
            if choice == "L":
                makeLeftTurn()
            elif choice == "R":
                makeRightTurn()

def addPath(choice):
    global path
    path = path + choice
    print("Path is now: " + path)

def checkForS():
    if runWithBot == True:
        for i in range (0,sCheckPulses):
            forward()
            sleep(.1)
        reading = readSensors()
        if reading != "00000000":
            return True
        elif reading:
            return False
    elif runWithBot == False:
        isS = input("Is straight an option? (y/n): ")
        if isS == "y":
            return True
        elif isS == "n":
            return False
        else:
            print("Please enter a valid answer")
            return checkForS()

def makeUTurn():
    if runWithBot == True:
        for i in range (0, uTurnPulses):
            turnLeft()
            sleep(.1)
        input("Please turn me around and press Enter to continue")
    else:
        print("Make U-turn")

def makeStraight():
    # input("Please move me slightly forward onto the S option and press Enter to continue")
    if runWithBot == True:
        pass
    else:
        print("Continue straight")

def makeLeftTurn():
    # input("Please turn me to the left and press Enter to continue")
    if runWithBot == True:
        for i in range (0, turnPulses):
            turnLeft()
            sleep(.1)
    else:
        print("Make left turn")

def makeRightTurn():
    # input("Please turn me to the right and press Enter to continue")
    if runWithBot == True:
        for i in range (0, turnPulses):
            turnRight()
            sleep(.1)
    else:
        print("Make right turn")
# ===== End Decision Functions =====

def fasterPath(shorterPath):
    global path
    print("Was given path: " + shorterPath)
    shorterPath = list(shorterPath)
    while shorterPath.count("U") > 0:
        i = shorterPath.index("U")
        if shorterPath[i - 1] == "L":
            if shorterPath[i + 1] == "L":
                shorterPath[i] = "S"
                del shorterPath[i + 1]
                del shorterPath[i - 1]
            elif shorterPath[i + 1] == "S":
                shorterPath[i] = "R"
                del shorterPath[i + 1]
                del shorterPath[i - 1]
                
        elif shorterPath[i - 1] == "S":
            if shorterPath[i + 1] == "L":
                shorterPath[i] = "R"
                del shorterPath[i + 1]
                del shorterPath[i - 1]
                
            elif shorterPath[i + 1] == "S":
                shorterPath[i] = "U"
                del shorterPath[i + 1]
                del shorterPath[i - 1]
                
        elif shorterPath[i - 1] == "R":
            if shorterPath[i + 1] == "L":
                shorterPath[i] = "U"
                del shorterPath[i + 1]
                del shorterPath[i - 1]
        print(''.join(shorterPath))
    print("Found that this path was faster: " + ''.join(shorterPath))
    path = ''.join(shorterPath)

if __name__ == "__main__":
    gpioSetup()
    input("Starting Maze First run")
    while state != "Finish":
        followLine()
    print("Found end of maze!")
    print("The path taken was: " + path)
    fasterPath(path)
    input("Press enter to start second run")
    state = "secondRun"
    while state != "Finish":
        followLine()

    gpioCleanup()
