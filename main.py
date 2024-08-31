import pyautogui
import time
import math
import pytesseract
import pyperclip
from PIL import Image, ImageEnhance, ImageOps, ImageFilter


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
    # Resize the image using the updated resampling method
    image = image.resize((image.width * 2, image.height * 2), Image.Resampling.LANCZOS)
    # Convert to grayscale
    image = ImageOps.grayscale(image)

    # Apply binary thresholding
    image = ImageOps.autocontrast(image)
    image = ImageOps.invert(image)
    threshold = 128
    image = image.point(lambda p: 255 if p > threshold else 0)

    # Sharpen the image
    image = image.filter(ImageFilter.SHARPEN)

    # Save the processed image for debugging
    image.save("screenshot_rank_processed.png")

    # Configure tesseract to better recognize numbers
    custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789'

    # Use Tesseract to extract text from the image
    text = pytesseract.image_to_string(image, config=custom_config)
    
    #print("age : ",text)
    #image.show()
    return int(text)

def updatePlayer(i,growth):
    time.sleep(0.1)    
    if not growth:
        return 0
    else:
        openPlayer(i)

        age= getPlayerAge()

        # open Editor
        pyautogui.moveTo(screen_width*0.686, screen_height*0.03)    
        pyautogui.click()
        time.sleep(0.1)
        # open Attribute Details
        pyautogui.moveTo(screen_width*0.778, screen_height*0.32)    
        pyautogui.click()
        time.sleep(0.1)
        if age>=30:
            # Update CA
            pyautogui.moveTo(screen_width*0.50208, screen_height*0.345)
            pyautogui.doubleClick(button='left')
            time.sleep(0.1)
            # Press 'Ctrl+C' (or 'Command+C' on macOS) to copy the selected text to the clipboard
            pyautogui.hotkey('ctrl', 'c')# Short pause to ensure the clipboard operation is completed
            time.sleep(0.1)
            # Retrieve the copied text from the clipboard
            CA = pyperclip.paste()
            CA=int(CA)
            CA+=growth
            # Convert the updated CA back to a string
            CA = str(CA)
            print("updating CA to : ", CA)
            # Copy the updated CA to the clipboard
            pyperclip.copy(CA)
            pyautogui.moveTo(screen_width*0.50208, screen_height*0.345)
            pyautogui.doubleClick(button='left')
            time.sleep(0.1)
            pyautogui.hotkey('ctrl', 'v')

        # Update PA
        print("updating PA")
        pyautogui.moveTo(screen_width*0.4953125, screen_height*0.2875)
        pyautogui.doubleClick(button='left')
        time.sleep(0.1)
        # Press 'Ctrl+C' (or 'Command+C' on macOS) to copy the selected text to the clipboard
        pyautogui.hotkey('ctrl', 'c')# Short pause to ensure the clipboard operation is completed
        time.sleep(0.1)
        # Retrieve the copied text from the clipboard
        PA = int(pyperclip.paste())
        PA+=growth
        # Convert the updated CA back to a string
        PA = str(PA)
        print("updating PA to : ", PA)
        # Copy the updated CA to the clipboard
        pyperclip.copy(PA)
        pyautogui.moveTo(screen_width*0.4953125, screen_height*0.2875)
        pyautogui.doubleClick(button='left')
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'v')

        # OK click
        pyautogui.moveTo(screen_width*0.7583, screen_height*0.7683)
        pyautogui.click(button='left')
        
        # Back to player menu
        pyautogui.moveTo(screen_width*0.11875, screen_height*0.03583)
        pyautogui.click(button='left')

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

    # Close general
    pyautogui.moveTo(screen_width*0.2, screen_height*0.175)    
    pyautogui.click()

def openAttacking():

    # open Attack
    pyautogui.moveTo(screen_width*0.214583, screen_height*0.21583)    
    pyautogui.click()
    
    # open goals

    # open assists

    # close Attack
    pyautogui.moveTo(screen_width*0.214583, screen_height*0.21583)    
    pyautogui.click()




# Get the screen size
screen_width, screen_height = pyautogui.size()

#print(f"Screen width: {screen_width}")
#print(f"Screen height: {screen_height}")
#openGeneral()
print(getRatio())
#print(getRank(2))
#openPlayer(4)
#print(getPlayerAge())
#updatePlayer(0,1)