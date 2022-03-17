import time
import os
import sqlite3
import logging
import time
import os
import traceback

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from datetime import datetime
from io import BytesIO

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s : %(name)s : %(lineno)s : %(message)s ', datefmt='%m/%d/%Y %I:%M:%S %p')


class Bot_image_maker: 
    
    def __init__(self, image_folder):
        """
        Initializes an instance of the ConfessionTyper class. 
        
            
        Attributes:
            driver (Selenium.webdriver.Chrome): The Chromedriver that is used to automate browser actions
            base_url (str): Base URL to the local site confessions will be typed in.
            actions (ActionsChains): Action chain. I do not believe it's actually used for anything at the moment. Might be used later, 
                                     might as well keep it.
        """ 
        
        
        file_handler = logging.FileHandler('logging.log', mode='w')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        
        
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.url = 'file:///C:/Users/jeray/Documents/Projects/SpottedAutomation/Image_Typing_Site/index.html' 
        self.driver.get(self.url)      
        self.actions = ActionChains(self.driver) 
        self.loop_counter = 0
        self.text_area_id = "text_span" 
        self.block_div_id = "block_div"
        self.image_folder = image_folder

        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, self.text_area_id))
            )
            self.text_area = self.driver.find_element(By.ID, self.text_area_id)
            self.block_div = self.driver.find_element(By.ID, self.block_div_id)
            logger.info("Text area captured")
        except Exception as e:
            logger.error(e)
            logger.exception("Text area fail to capture")

        
        

               

    def type_text(self, text, color="None"):
        script = "arguments[0].innerHTML = '{}'".format(text.replace('\'', '\\\'')).replace('\n', ' ').replace('\r', ' ')
        self.driver.execute_script(script, self.text_area)

        with open("greenValue.txt", "r") as colorFile: 
            greenValue = colorFile.readline()[:-1]
            counter = colorFile.readline()

        # Resets text font size to 30px then shrinks it down as necessary
        self.driver.execute_script(open("Image_Typing_Site/image_typing_site.js").read())
        """
         #Comment out for different colours
        match color:           
            case "Spottings (Red)": # red
                colorscript = "arguments[0].style.borderColor = \"rgb(255, 154, 162)\""  
            case "Romance(Pink)": # pink
                colorscript = "arguments[0].style.borderColor = \"rgb(255, 183, 178)\"" 
            case "School(Orange)": # orange
                colorscript = "arguments[0].style.borderColor = \"rgb(255, 218, 193)\""  
            case "Social(Yellow)": # To be social #yellow
                colorscript = "arguments[0].style.borderColor = \"rgb(240, 240, 142)\"" 
            case "Questions(Green)": # green
                colorscript = "arguments[0].style.borderColor = \"rgb(226, 240, 203)\""  
            case "Complaints(Dark green)": #dark green
                colorscript = "arguments[0].style.borderColor = \"rgb(130, 192, 154)\""  
            case "Weird(Blue)": # blue
                colorscript = "arguments[0].style.borderColor = \"rgb(181, 234, 215)\"" 
            case "Sad(Dark blue)": #dark blue
                colorscript = "arguments[0].style.borderColor = \"rgb(58, 63, 102)\""  
            case "Other(Purple)": # purple
                colorscript = "arguments[0].style.borderColor = \"rgb(199, 206, 234)\""  
            case _:
                colorscript = "arguments[0].style.borderColor = \"rgb(199, 206, 234)\""  
        """
        match color:           
            case "Spottings (Red)": # red
                colorscript = "arguments[0].style.backgroundColor = \"rgb(255, 154, 162)\""  
                colorscript2 = "arguments[0].style.color = \"rgb(0, 0, 0)\"" #Change colour of font to white 
            case "Romance(Pink)": # pink
                colorscript = "arguments[0].style.backgroundColor = \"rgb(255, 183, 178)\"" 
                colorscript2 = "arguments[0].style.color = \"rgb(0, 0, 0)\""
            case "School(Orange)": # orange
                colorscript = "arguments[0].style.backgroundColor = \"rgb(255, 218, 193)\""  
                colorscript2 = "arguments[0].style.color = \"rgb(0, 0, 0)\""
            case "Social(Yellow)": # To be social #yellow
                colorscript = "arguments[0].style.backgroundColor = \"rgb(240, 240, 142)\"" 
                colorscript2 = "arguments[0].style.color = \"rgb(0, 0, 0)\""
            case "Questions(Green)": # green
                colorscript = "arguments[0].style.backgroundColor = \"rgb(226, 240, 203)\""  
                colorscript2 = "arguments[0].style.color =\"rgb(0, 0, 0)\""
            case "Complaints(Dark green)": #dark green
                colorscript = "arguments[0].style.color = \"rgb(130, 192, 154)\""   
                colorscript2 = "arguments[0].style.color = \"rgb(0, 0, 0)\"" #Change colour of font to white 
            case "Weird(Blue)": # blue
                colorscript = "arguments[0].style.backgroundColor = \"rgb(181, 234, 215)\"" 
                colorscript2 = "arguments[0].style.color = \"rgb(0, 0, 0)\""
            case "Sad(Dark blue)": #dark blue
                colorscript = "arguments[0].style.backgroundColor = \"rgb(58, 63, 102)\""  
                colorscript2 = "arguments[0].style.color = \"rgb(255, 255, 255)\"" #Change colour of font to white 
            case "Other(Purple)": # purple
                colorscript = "arguments[0].style.backgroundColor = \"rgb(199, 206, 234)\""  
                colorscript2 = "arguments[0].style.color = \"rgb(0, 0, 0)\"" 
            case _:
                colorscript = "arguments[0].style.backgroundColor = \"rgb(199, 206, 234)\""  
                colorscript2 = "arguments[0].style.color = \"rgb(0, 0, 0)\""
            
        """
        match color:           
            case "Spottings (Red)": # red
                colorscript = "arguments[0].style.backgroundColor = \"rgb(92, 55, 58)\""  
                colorscript2 = "arguments[0].style.color = \"rgb(255, 255, 255)\"" #Change colour of font to white 
            case "Romance(Pink)": # pink
                colorscript = "arguments[0].style.backgroundColor = \"rgb(74, 63, 62)\"" 
                colorscript2 = "arguments[0].style.color = \"rgb(255, 255, 255)\"" #Change colour of font to white  
            case "School(Orange)": # orange
                colorscript = "arguments[0].style.backgroundColor = \"rgb(84, 69, 59)\""  
                colorscript2 = "arguments[0].style.color = \"rgb(255, 255, 255)\"" #Change colour of font to white 
            case "Social(Yellow)": # To be social #yellow
                colorscript = "arguments[0].style.backgroundColor = \"rgb(92, 92, 55)\"" 
                colorscript2 = "arguments[0].style.color = \"rgb(255, 255, 255)\"" #Change colour of font to white 
            case "Questions(Green)": # green
                colorscript = "arguments[0].style.backgroundColor = \"rgb(81, 84, 77)\""  
                colorscript2 = "arguments[0].style.color = \"rgb(255, 255, 255)\"" 
            case "Complaints(Dark green)": #dark green
                colorscript = "arguments[0].style.backgroundColor = \"rgb(1, 58, 18)\""  
                colorscript2 = "arguments[0].style.color = \"rgb(255, 255, 255)\"" #Change colour of font to white 
            case "Weird(Blue)": # blue
                colorscript = "arguments[0].style.backgroundColor = \"rgb(67, 84, 78)\"" 
                colorscript2 = "arguments[0].style.color = \"rgb(255, 255, 255)\"" #Change colour of font to white  
            case "Sad(Dark blue)": #dark blue
                colorscript = "arguments[0].style.backgroundColor = \"rgb(58, 63, 102)\""  
                colorscript2 = "arguments[0].style.color = \"rgb(255, 255, 255)\"" #Change colour of font to white 
            case "Other(Purple)": # purple
                colorscript = "arguments[0].style.backgroundColor = \"rgb(66, 67, 74)\""  
                colorscript2 = "arguments[0].style.color = \"rgb(255, 255, 255)\"" #Change colour of font to white              
            case _:
                colorscript = "arguments[0].style.backgroundColor = \"rgb(199, 206, 234)\""  
                colorscript2 = "arguments[0].style.color = \"rgb(0, 0, 0)\"" 
            """ 

        #if (counter == "2"):
        #    counter = "0"
        #    greenValue = str(int(greenValue)-1)
        #else:
        #    counter = str(int(counter)+1)

        #with open("greenValue.txt", "w") as colorFile: 
        #     colorFile.write(greenValue + "\n")
        #    colorFile.write(counter)

        self.driver.execute_script(colorscript, self.block_div)
        self.driver.execute_script(colorscript2, self.block_div)

    def save_div(self, image_name):
        image_name = self.image_folder + image_name + "_"
        image_name = image_name.replace('/', '-')
        image_name = image_name.replace(':', '-')
        self.block_div.screenshot(image_name + ".png")
        
        im = Image.open(image_name + ".png")
        rgb_im = im.convert('RGB')
        image_name += ".jpg"
        rgb_im.save(image_name)
        return  image_name

    def make_image(self, body_text, id_tag, time_stamp, color="None"):

        if id_tag[0] == '-' and len(id_tag) > 1:
            id_tag = id_tag[1:]

        self.type_text(body_text + "<br><br><br>- " + id_tag, color)
        return self.save_div(time_stamp)
        



if __name__ == '__main__':
    test_string = 'Everytime I FaceTime my bf he barely talks to me and he’s always napping. I tell him I want to ft and talk not just stay quiet and just stare at him. I try to start conversation but all he does is say one words or just gives me kisses and stuff. I wanna talk bc I’m feeling sad and I feel like I have no one to turn to bc he’s always napping on FaceTime or playing games on the computer. Even when he’s awake it still feels distant and I keep trying to start the convo. He gets upset when I don’t talk and serve him the same attitude he serves me. And then questions if I love him bc I’m being quiet like he does to me. It’s so frustrating I try to tell him i want to talk not just be chilling in silence. And when he does try to put in the effort he asks what I want to talk about and I talk but again, it’s like he shows little interest. I just wanna talk :('
    image_maker = Bot_image_maker("Image_Folder\\")
    image_maker.type_text(test_string, "Sad")
    time.sleep(1000)
    image_maker.save_div("Image_Folder/Screenshot")
