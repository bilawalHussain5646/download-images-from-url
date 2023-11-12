from selenium import webdriver
from selenium.webdriver.common.by import By
import os 
import pandas as pd
import requests

import tkinter as tk
import tkinter.font as tkFont
import threading
import os
import concurrent.futures
import time
def ProductImagesSaver(driver,sku,folder_name,url):
    driver.get(f'{url}')
    screenshot_folder = f"{folder_name}"
    if not os.path.exists(screenshot_folder):
        os.makedirs(screenshot_folder)



    images_div = driver.find_element(By.CSS_SELECTOR,".c-gallery__thumbnail")
    images = images_div.find_elements(By.TAG_NAME,"a")
    images_url = []
    print(len(images))
    for img in images:
        url = img.get_attribute("data-large-m")
        print(url)
        if url is not None:
            if "https" in url:
                pass
            else: 
                url = "https://lg.com"+url
            images_url.append(url)
    print(images_url)
    img_count = 0
    for img_url in images_url:
        # driver.get(img_url)
        
        # try:
        #     driver.find_element(By.TAG_NAME,"h1")
        #     image_check = False
        # except:
        #     image_check = True
        

        image_url = img_url  # Replace with the actual image URL
        response = requests.get(image_url)

        # if image_check == False:
        #     error_image = " (Not_Found)"
        #     screenshot_file= os.path.join(screenshot_folder, f"{str(sku)+'-'+str(img_count+1)+error_image}.png")
            
        # else:
        screenshot_file= os.path.join(screenshot_folder, f"{str(sku)+'-'+str(img_count+1)}.jpg")
        if response.status_code == 200:  
            with open(screenshot_file, "wb") as file:
                file.write(response.content)

        else:
            print("Failed to download the image.")
        
        img_count+=1
    



def Extractor():        
    list_of_urls = []
    list_of_folders = []
    list_of_sku = []

    # Dont update below code
    df = pd.read_excel("list_of_products.xlsx")

    for dt in df['url']:
        list_of_urls.append(dt)

    for dt in df['folder']:
        list_of_folders.append(dt)

    for dt in df['sku']:
        list_of_sku.append(dt)
    driver = webdriver.Chrome("C:\Program Files\chromedriver.exe")

    for i in range(0,len(list_of_urls)):
        ProductImagesSaver(driver,list_of_sku[i],list_of_folders[i],list_of_urls[i])

    driver.close()
# --------------------------------------------

# Main App 
class App:

    def __init__(self, root):
        #setting title
        root.title("Product Images Extractor")
        
        #setting window size
        width=640
        height=480
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        root.configure(bg='black')

       

        extractor_btn=tk.Button(root)
        extractor_btn["anchor"] = "center"
        extractor_btn["bg"] = "#0279c1"
        extractor_btn["borderwidth"] = "0px"
        ft = tkFont.Font(family='Arial Narrow',size=13)
        extractor_btn["font"] = ft
        extractor_btn["fg"] = "#ffffff"
        extractor_btn["justify"] = "center"
        extractor_btn["text"] = "Extract Images"
        extractor_btn["relief"] = "raised"
        extractor_btn.place(x=90,y=190,width=150,height=70)
        extractor_btn["command"] = self.start_extractor
        
    

    def extractor_btn(self):

        executable_commands = [
            Extractor
            ]
        # list_of_extra = [Search_By_Category_with_extraonly]
        
        thread_list = [threading.Thread(target=func) for func in executable_commands]

        # start all the threads
        for thread in thread_list:
            thread.start()

 

    
    
    def start_extractor(self):
        thread = threading.Thread(target=self.extractor_btn)
        thread.start()   

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()


