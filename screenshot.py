from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from pyvirtualdisplay import Display
import time
import cv2
import random
import string
import sys
import os



from skimage.metrics import structural_similarity as ssim


display = Display(visible=0, size=(1024, 768))
display.start()

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')



def take_screenshot(url):

#    if url:
#          display2 = init_display(640, 480)
        

    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    driver.get(url)
    screenshot_path = f"screenshot_{generate_random_string(6)}.png"
    driver.save_screenshot(screenshot_path)
    

 

    time.sleep(5)

    driver.quit()

    return screenshot_path

 

def generate_random_string(length):

    letters = string.ascii_lowercase

    return ''.join(random.choice(letters) for i in range(length))

 

def compare_images(image1, image2):

    # Resimleri yükle

    image1 = cv2.imread(image1)

    image2 = cv2.imread(image2)

 

    # Resimleri aynı boyuta yeniden boyutlandır

    image1 = cv2.resize(image1, (300, 300))

    image2 = cv2.resize(image2, (300, 300))

 

    # Resimleri gri tonlamalı olarak yükle

    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)

    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

 

    # SSIM kullanarak benzerlik oranını hesapla

    similarity_index, _ = ssim(gray_image1, gray_image2, full=True)

 

    return similarity_index

 

def main(url1, url2):

    # Ekran görüntülerini al

    screenshot1 = take_screenshot(url1)

    screenshot2 = take_screenshot(url2)

 

    # Resimleri karşılaştır

    similarity = compare_images(screenshot1, screenshot2)

 

    # Benzerlik oranını ekrana yazdır

    print(f"Similarity: {similarity * 100:.2f}%")


if __name__ == "__main__":

    url1 = os.getenv('URL1')
    url2 = os.getenv('URL2')
    if not url1 or not url2:
        if len(sys.argv) != 3:

            print("Usage: python compare_screenshots.py <url1> <url2>")

            sys.exit(1)
        
        url1 = sys.argv[1]

        url2 = sys.argv[2]


    main(url1,url2)
