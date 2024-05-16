import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import requests  
import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.image_processing import gaussian_blur, contrast_enhancement, edge_detection  # Import the image processing functions
download_dir = os.path.abspath('Downloads')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('prefs', {
    'download.default_directory': download_dir,
    'download.prompt_for_download': False,
    'download.directory_upgrade': True,
    'safebrowsing.enabled': True
})



# Path to folder containing images
image_folder_path = os.path.abspath('Tests/Images')

# List of image files
image_files = os.listdir(image_folder_path)
# print(image_files)
# Number of tabs to open
num_tabs = 4

class TestImageUpload(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_upload_images(self):
        driver = self.driver

        # Open multiple tabs
        for i in range(num_tabs):
            if i > 0:
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[i])
                # print("hi")

            # Navigate to the form page
            driver.get('file:///D:/Distributed%20Computing/Distributed-Image-Processing-1/frontend/index.html')

            # Upload images
            for image in image_files:
                self.upload_image(driver, os.path.join(image_folder_path, image))
                #time.sleep(100)  # Add a short delay to ensure the file upload is completed
          

        # # Add assertions if needed
        # # Example assertion: check if a success message appears after uploading images
        # success_message = driver.find_element(By.XPATH,"//div[@class='success-message']")
        # self.assertTrue(success_message.is_displayed(), "Success message not found")
        
    def upload_image(self,driver, image_path):
        file_input = driver.find_element(By.XPATH,"//input[@type='file']")
        file_input.send_keys(image_path)
        select_element = driver.find_element(By.XPATH, "//div[@id='imageFilters']//select")
        select = Select(select_element)
        select.select_by_visible_text('Edge Detection')
        # print("Hello")
          # Wait for the option to be selected (add a delay if necessary)
        driver.implicitly_wait(5)
       
    # Find the submit button element
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        # Click the submit button
        submit_button.click()

         # Wait for the image to be downloaded
        max_wait_time = 60  # Maximum wait time in seconds
        polling_interval = 1  # Polling interval in seconds
        image_filename = "image 1.png"
        image_path = os.path.join("C:\\Users\\Sarah\\Downloads", image_filename)
        wait_time = 0

        while not os.path.exists(image_path):
            time.sleep(polling_interval)
            wait_time += polling_interval

            if wait_time >= max_wait_time:
                self.fail(f"Image download took too long. Expected file '{image_filename}' was not found.")

        # Assertion: Check if the file exists
        self.assertTrue(os.path.exists(image_path), f"Processed image not found: {image_path}")


if __name__ == "__main__":
    unittest.main()
