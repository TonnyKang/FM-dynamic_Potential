import pyautogui
import time
import math
import pytesseract
from PIL import Image
from PIL import ImageEnhance

def getLocation():
    
    time.sleep(3)
    return pyautogui.position()

def getRatio():
    
    x,y=getLocation()
    return (x/screen_width,y/screen_height)

def getRank(i):
    gap=i*0.051
    region = (math.floor(0.321*screen_width), math.floor((0.19+gap)*screen_height), math.ceil(0.025*screen_width), math.ceil(0.04*screen_height))
    image = pyautogui.screenshot(region=region)
    image = image.resize((image.width * 2, image.height * 2), Image.ANTIALIAS)
    #print("screenshot taken")
    image.save("screenshot_rank.png")
    text = pytesseract.image_to_string(image)
    #print("translated")
    #image = Image.open("screenshot_rank.png")
    
    #image.show()

    return text

def openPlayer(i):
    time.sleep(1)
    gap=i*0.0525
    pyautogui.moveTo(screen_width*0.436458, screen_height*(gap+0.2008))
    pyautogui.click()
    return 1

def getPlayerAge():
    
    region = (math.floor(0.19*screen_width), math.floor((0.135)*screen_height), math.ceil(0.018*screen_width), math.ceil(0.027*screen_height))
    image = pyautogui.screenshot(region=region)
    image = image.resize((image.width * 2, image.height * 2), Image.ANTIALIAS)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.5)
    image.save("screenshot_rank.png")
    text = pytesseract.image_to_string(image)
    
    print(text)
    image.show()
    return text

def updatePlayer(i,growth):    
    if not growth:
        return 0
    else:
        openPlayer(i)

        # open Editor
        pyautogui.moveTo(screen_width*0.686, screen_height*0.03)    
        pyautogui.click()

        # open Attribute Details
        pyautogui.moveTo(screen_width*0.778, screen_height*0.32)    
        pyautogui.click()

        print("grown by : ",growth)
    return 1

def updateStat():
    growth=5
    updatePlayer(growth)
    i=1    
    while growth:
        rank=getRank(i)
        rank = rank.strip()
        print(rank)        
        if rank=="2nd":
            growth=3
        elif rank=="3rd":
            growth=1
        elif rank=="":
            print("tie")
        else:
            growth=0            
        updatePlayer(growth)
        i+=1

def openGeneral():

    time.sleep(3)
    
    # open general
    pyautogui.moveTo(screen_width*0.2, screen_height*0.175)    
    pyautogui.click()

    # open Appearance
    pyautogui.moveTo(screen_width*0.25, screen_height*0.2)    
    pyautogui.click()
    updateStat()

    time.sleep(1)
    # open Player of the Match
    pyautogui.moveTo(screen_width*0.25, screen_height*0.465)    
    pyautogui.click()
    updateStat()

    time.sleep(1)
    # open Distance Covered
    pyautogui.moveTo(screen_width*0.25, screen_height*0.525)    
    pyautogui.click()
    updateStat()

    time.sleep(1)
    # open Headers Won
    pyautogui.moveTo(screen_width*0.25, screen_height*0.655)    
    pyautogui.click()
    updateStat()

    time.sleep(1)
    # open Possesion Won
    pyautogui.moveTo(screen_width*0.25, screen_height*0.705)    
    pyautogui.click()
    updateStat()





# Get the screen size
screen_width, screen_height = pyautogui.size()

#print(f"Screen width: {screen_width}")
#print(f"Screen height: {screen_height}")
#openGeneral()
#print(getRatio())
#print(getRank(2))
#openPlayer(4)
print(getPlayerAge())