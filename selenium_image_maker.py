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

        
        

               

    def type_text(self, text):
        print(text)
        print(self.text_area)
        self.driver.execute_script("arguments[0].innerHTML = '{}'".format(text.replace('\'', '\\\'')), self.text_area)

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

    def make_image(self, body_text, id_tag, time_stamp):
        self.type_text(body_text + "<br><br><br>- " + id_tag)
        return self.save_div(time_stamp)
        



if __name__ == '__main__':
    test_string = 'Referencing the post which spoke on the use of the word females. Some women find the use of the word to be uncomfortable or somewhat degrading because it feels as though their identity is being reduced to sex cells. Naturally this applies to situations where woman or girl can be used. For example "Females cant be trusted" is a statement Ive personally heard often. Not only is statement already problematic in itself, the use of the word females adds nothing to the statement and women wouldve been more applicable. Furthermore, people dont use male unless its a conversation relating to sex/biology highlighting the double standard. Obviously this does not apply to everyone who identifies as a woman. However, if someone mentions that they are uncomfortable with the use of a word or an action, maybe try understanding why that is before attacking. <br> <br><br>Sender'
    image_maker = Bot_image_maker("Image_Folder\\")
    image_maker.type_text(test_string)
    image_maker.save_div("Image_Folder/Screenshot")
