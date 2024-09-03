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
    time.sleep(0.5)
    image = pyautogui.screenshot(region=region)
    image = image.resize((image.width * 2, image.height * 2), Image.Resampling.LANCZOS)
    # Convert to grayscale
    image = ImageOps.grayscale(image)
    # Apply binary thresholding
    # Enhance the image (contrast/sharpen) to improve OCR accuracy
    image = ImageEnhance.Contrast(image).enhance(2.0)
    image = image.filter(ImageFilter.SHARPEN)
    
    print("screenshot taken")
    image.save("screenshot_rank.png")
    text = pytesseract.image_to_string(image)
    print(text)
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
    while True:  # Keep trying until valid age is obtained
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
        text = pytesseract.image_to_string(image, config=custom_config).strip()

        if text.isdigit():  # Check if the extracted text is a valid number
            return int(text)
        else:
            print("Invalid age detected, retrying...")
            # You might want to add a small delay here to avoid tight looping
            time.sleep(0.5)

def updatePlayer(i,growth):
    time.sleep(0.1)    
    if not growth:
        return 0
    else:
        openPlayer(i)

        age= getPlayerAge()

        # open Editor
        time.sleep(0.1)  
        pyautogui.moveTo(screen_width*0.686, screen_height*0.03)    
        pyautogui.click()
        time.sleep(0.1)  
        # open Attribute Details
        pyautogui.moveTo(screen_width*0.778, screen_height*0.32)    
        pyautogui.click()
        time.sleep(0.1)  
        # Update PA
        print("updating PA")
        pyautogui.moveTo(screen_width*0.50208, screen_height*0.345)
        pyautogui.doubleClick(button='left')
        time.sleep(0.5)  
        # Press 'Ctrl+C' (or 'Command+C' on macOS) to copy the selected text to the clipboard
        pyautogui.hotkey('ctrl', 'c')# Short pause to ensure the clipboard operation is completed
        time.sleep(0.5)  
        # Retrieve the copied text from the clipboard
        PA = int(pyperclip.paste())
        if PA >= 150:
                if PA>=180:
                    growth=1
                growth=min(growth,3)
        PA+=growth
        # Convert the updated CA back to a string
        PA = str(PA)
        print("updating PA to : ", PA)
        # Copy the updated CA to the clipboard
        pyperclip.copy(PA)
        pyautogui.moveTo(screen_width*0.50208, screen_height*0.345)
        pyautogui.doubleClick(button='left')
        time.sleep(0.5)  
        pyautogui.hotkey('ctrl', 'v')

        if age>=30:
            # Update CA
            pyautogui.moveTo(screen_width*0.4953125, screen_height*0.2875)
            pyautogui.doubleClick(button='left')
            time.sleep(0.5)  
            # Press 'Ctrl+C' (or 'Command+C' on macOS) to copy the selected text to the clipboard
            pyautogui.hotkey('ctrl', 'c')# Short pause to ensure the clipboard operation is completed
            time.sleep(0.5)  
            # Retrieve the copied text from the clipboard
            CA = pyperclip.paste()
            CA=int(CA)
            if CA >= 150:
                if CA>=180:
                    growth=1
                growth=min(growth,3)
            CA+=growth
            # Convert the updated CA back to a string
            CA = str(CA)
            print("updating CA to : ", CA)
            # Copy the updated CA to the clipboard
            pyperclip.copy(CA)
            pyautogui.moveTo(screen_width*0.4953125, screen_height*0.2875)
            pyautogui.doubleClick(button='left')
            time.sleep(0.5)  
            pyautogui.hotkey('ctrl', 'v')

        # OK click
        time.sleep(0.1)  
        pyautogui.moveTo(screen_width*0.7583, screen_height*0.7683)
        pyautogui.click(button='left')

        # OK double click to skip staffs
        time.sleep(0.1)  
        pyautogui.moveTo(screen_width*0.7583, screen_height*0.7)
        pyautogui.click(button='left')
        
        # Back to player menu
        time.sleep(0.1)  
        pyautogui.moveTo(screen_width*0.11875, screen_height*0.03583)
        pyautogui.click(button='left')

    return 1

def updateStat():
    growth=5
    updatePlayer(0,growth)
    i=1    
    while growth:
        time.sleep(0.1)
        rank=getRank(i)
        rank = rank.strip()
        time.sleep(0.1)
        print("rank is:",rank)
        print(rank)        
        if rank=="2nd":
            growth=3
        elif rank=="3rd":
            growth=1
        elif rank=="":
            print("tie")
        else:
            growth=0

        if growth == 0:  # If growth is set to 0, exit the loop immediately
            break            
        updatePlayer(i,growth)
        i+=1
    return 0

def scrollDown():
    pyautogui.moveTo(screen_width*0.23541666666666666, screen_height*0.7408333333333333)
    time.sleep(0.5) 
    # Scroll down by 500 units
    pyautogui.scroll(-600)

def scrollUp():
    pyautogui.moveTo(screen_width*0.23541666666666666, screen_height*0.7408333333333333)
    time.sleep(0.5) 
    # Scroll down by 500 units
    pyautogui.scroll(2000)

def openGeneral():
    time.sleep(0.1) 
    # open general
    pyautogui.moveTo(screen_width*0.2, screen_height*0.175)    
    pyautogui.click()

    # open Appearance
    time.sleep(0.1) 
    pyautogui.moveTo(screen_width*0.25, screen_height*0.2)    
    pyautogui.click()
    updateStat()

    time.sleep(0.1) 
    # open Player of the Match
    pyautogui.moveTo(screen_width*0.25, screen_height*0.465)    
    pyautogui.click()
    updateStat()

    time.sleep(0.1) 
    # open Distance Covered
    pyautogui.moveTo(screen_width*0.25, screen_height*0.525)    
    pyautogui.click()
    updateStat()

    time.sleep(0.1) 
    # open Headers Won
    pyautogui.moveTo(screen_width*0.25, screen_height*0.655)    
    pyautogui.click()
    updateStat()

    time.sleep(0.1) 
    # open Possesion Won
    pyautogui.moveTo(screen_width*0.25, screen_height*0.705)    
    pyautogui.click()
    updateStat()

    # Close general
    time.sleep(0.1) 
    pyautogui.moveTo(screen_width*0.2, screen_height*0.175)    
    pyautogui.click()

def openAttacking():
    time.sleep(0.1) 
    # open Attack
    pyautogui.moveTo(screen_width*0.214583, screen_height*0.21583)    
    pyautogui.click()
    
    # open goals
    time.sleep(0.1) 
    pyautogui.moveTo(screen_width*0.19739583, screen_height*0.2475)    
    pyautogui.click()
    updateStat()

    # open assists
    time.sleep(0.1) 
    pyautogui.moveTo(screen_width*0.234375, screen_height*0.8075)    
    pyautogui.click()
    updateStat()

    # open Key Passes
    time.sleep(0.1) 
    pyautogui.moveTo(screen_width*0.2671875, screen_height*0.8983)    
    pyautogui.click()
    updateStat()

    scrollDown()

    # open Chances created
    time.sleep(0.1) 
    pyautogui.moveTo(screen_width*0.26822916, screen_height*0.2283)    
    pyautogui.click()
    updateStat()

    scrollDown()

    # open Dribbles made
    time.sleep(0.1) 
    pyautogui.moveTo(screen_width*0.25572916, screen_height*0.43916)    
    pyautogui.click()
    updateStat()

    scrollDown()
    scrollDown()

    # open Progressive passes
    time.sleep(0.1) 
    pyautogui.moveTo(screen_width*0.2583, screen_height*0.6)    
    pyautogui.click()
    updateStat()

    scrollDown()
    scrollDown()

    # open high intensity sprints
    time.sleep(0.1) 
    pyautogui.moveTo(screen_width*0.265625, screen_height*0.6383)    
    pyautogui.click()
    updateStat()

    scrollUp()

    # close Attack
    time.sleep(0.1) 
    pyautogui.moveTo(screen_width*0.214583, screen_height*0.21583)    
    pyautogui.click()

def openDefending():
    time.sleep(0.1) 
    # open Defending
    pyautogui.moveTo(screen_width*0.20572916, screen_height*0.2575)    
    pyautogui.click()

    # open Tackles Won
    time.sleep(0.1) 
    pyautogui.moveTo(screen_width*0.25989583, screen_height*0.3283)    
    pyautogui.click()
    updateStat()

    # open Key Tackles
    time.sleep(0.1) 
    pyautogui.moveTo(screen_width*0.26927083, screen_height*0.4583)    
    pyautogui.click()
    updateStat()

    # open Key Headers
    time.sleep(0.1) 
    pyautogui.moveTo(screen_width*0.239583, screen_height*0.5008333333333334)    
    pyautogui.click()
    updateStat()

    # open Interceptions made
    time.sleep(0.1) 
    pyautogui.moveTo(screen_width*0.27760416, screen_height*0.5483)    
    pyautogui.click()
    updateStat()

    # open Blocks
    time.sleep(0.1) 
    pyautogui.moveTo(screen_width*0.277083, screen_height*0.59)    
    pyautogui.click()
    updateStat()

    # open Clearances
    time.sleep(0.1) 
    pyautogui.moveTo(screen_width*0.26145833333333335, screen_height*0.635)    
    pyautogui.click()
    updateStat()

    # open Shots Blocked
    time.sleep(0.1) 
    pyautogui.moveTo(screen_width*0.27552083, screen_height* 0.716)    
    pyautogui.click()
    updateStat()

    # open Pressure Completed
    time.sleep(0.1) 
    pyautogui.moveTo(screen_width*0.2822916, screen_height* 0.8483333333333334)    
    pyautogui.click()
    updateStat()

    # close Defending
    time.sleep(0.1) 
    pyautogui.moveTo(screen_width*0.20572916, screen_height*0.2575)    
    pyautogui.click()

def openGoalkeeping():
    time.sleep(0.1) 
    # open GoalKeeping
    pyautogui.moveTo(screen_width*0.2416, screen_height*0.29416)    
    pyautogui.click()

    # open Clean sheets
    time.sleep(0.1) 
    pyautogui.moveTo(screen_width*0.26197916, screen_height*0.3675)    
    pyautogui.click()
    updateStat()

    # open Saves Held
    time.sleep(0.1) 
    pyautogui.moveTo(screen_width*0.29583, screen_height*0.4075)    
    pyautogui.click()
    updateStat()

    # open Saves Parried
    time.sleep(0.1) 
    pyautogui.moveTo(screen_width*0.277083, screen_height*0.45916666666666667)    
    pyautogui.click()
    updateStat()

    # close Goalkeeping
    pyautogui.moveTo(screen_width*0.2416, screen_height*0.29416)    
    pyautogui.click()



# Get the screen size
screen_width, screen_height = pyautogui.size()

def main():
    time.sleep(0.1) 
    openGeneral()
    time.sleep(0.1)  
    openAttacking()
    time.sleep(0.1)  
    openDefending()
    time.sleep(0.1) 
    openGoalkeeping()

if __name__ == "__main__":
    main()
