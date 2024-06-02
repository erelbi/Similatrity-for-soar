```
docker run -e URL1=https://f1.com -e URL2=https://f1.com  erelbi/web-similarity-for-soar 
[WDM] - Downloading: 19.9kB [00:00, 15.2MB/s]                   
[WDM] - Downloading: 100%|██████████| 3.10M/3.10M [00:01<00:00, 2.96MB/s]
[WDM] - Downloading: 19.9kB [00:00, 390kB/s]                    
Similarity: 100.00%
```

```
docker run  erelbi/web-similarity-for-soar https://f1.com https://f1.com 
[WDM] - Downloading: 100%|██████████| 3.10M/3.10M [00:01<00:00, 2.79MB/s]
[WDM] - Downloading: 19.9kB [00:00, 11.9MB/s]                   
Similarity: 100.00%

```

Screenshot Comparison Script
This script takes screenshots of two web pages and compares the images to determine their similarity using the Structural Similarity Index (SSIM).

Requirements
The script requires the following Python libraries:

selenium
webdriver_manager
pyvirtualdisplay
opencv-python
scikit-image
Code Explanation
Imports and Setup
python
```
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
```
- selenium: For automating web browser interactions.
- webdriver_manager: To automatically manage and install the correct WebDriver.
- pyvirtualdisplay: To create a virtual display for running the browser in a headless mode.
- time: For adding delays.
- cv2 (OpenCV): For image processing.
- random and string: For generating random strings.
- sys and os: For command-line arguments and environment variables.
- ssim from skimage.metrics: For calculating the Structural Similarity Index between images.
Display Setup
python

```
display = Display(visible=0, size=(1024, 768))
display.start()
```
Initializes and starts a virtual display.
WebDriver Options
python
```
options = webdriver.FirefoxOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
```
Configures the Firefox WebDriver to run in headless mode with additional options to handle system resource limitations.
Screenshot Function
python
```
def take_screenshot(url):
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    driver.get(url)
    screenshot_path = f"screenshot_{generate_random_string(6)}.png"
    driver.save_screenshot(screenshot_path)
    time.sleep(5)
    driver.quit()
    return screenshot_path
```
Takes a screenshot of the given URL and saves it as a PNG file.
The filename is generated using a random string.
Random String Generator
```
def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
```
Generates a random string of lowercase letters of the specified length.
Image Comparison Function
```
def compare_images(image1, image2):
    image1 = cv2.imread(image1)
    image2 = cv2.imread(image2)
    image1 = cv2.resize(image1, (300, 300))
    image2 = cv2.resize(image2, (300, 300))
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    similarity_index, _ = ssim(gray_image1, gray_image2, full=True)
    return similarity_index
```
Reads, resizes, and converts the images to grayscale.
Calculates and returns the Structural Similarity Index (SSIM) between the two images.
Main Function
```
def main(url1, url2):
    screenshot1 = take_screenshot(url1)
    screenshot2 = take_screenshot(url2)
    similarity = compare_images(screenshot1, screenshot2)
    print(f"Similarity: {similarity * 100:.2f}%")
```
Takes screenshots of the two provided URLs.
Compares the screenshots and prints the similarity percentage.
Command-Line Execution
```
if __name__ == "__main__":
    url1 = os.getenv('URL1')
    url2 = os.getenv('URL2')
    if not url1 or not url2:
        if len(sys.argv) != 3:
            print("Usage: python compare_screenshots.py <url1> <url2>")
            sys.exit(1)
        url1 = sys.argv[1]
        url2 = sys.argv[2]
    main(url1, url2)
```
Allows the script to be run from the command line with two URL arguments.
Alternatively, the URLs can be provided through environment variables URL1 and URL2.
This script is useful for comparing visual similarities between web pages by taking their screenshots and calculating their SSIM.

