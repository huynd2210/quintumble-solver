import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def splitStringIntoGrid(string, gridSize=5):
    return [list(string[i:i + gridSize]) for i in range(0, len(string), gridSize)]
def scrapeForPuzzle():
    url = "https://quintumble.com"
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU for headless mode (optional)
    chrome_options.add_argument("--window-size=1920x1080")  # Optional, set window size to avoid issues

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)

    wait = WebDriverWait(driver, 5)
    wait.until(EC.element_to_be_clickable((By.ID, "startGame"))).click()

    element = driver.find_element(By.ID, "tileContainer")
    return splitStringIntoGrid(element.text.replace("\n", ""))

if __name__ == '__main__':
    print(scrapeForPuzzle())
