

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import wordle 
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://www.nytimes.com/games/wordle/index.html")

driver.find_element(By.CSS_SELECTOR, '[data-testid="Play"]').click()


close_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '[data-testid="icon-close"]')
    )
)
close_button.click()
WebDriverWait(driver, 10).until(
    EC.invisibility_of_element_located(
        (By.CSS_SELECTOR, '[data-testid="icon-close"]')
    )
)

def find_colours(row_num):
    
    row = driver.find_element(By.CSS_SELECTOR,f'[aria-label="Row {row_num}"]')

    tiles = row.find_elements(By.CSS_SELECTOR,'[aria-roledescription="tile"]')
    states=[]
    for tile in tiles:
        states.append(tile.get_attribute('data-state'))
    colours=""
    for state in states:
        if state == "absent":
            colours += "b"
        elif state == "present":
            colours += "y"
        elif state == "correct":
            colours+="g"

    return colours
            
def solve():
    actions = ActionChains(driver)

# do guesses here
    best_word="stoae"
    for i in range(6):
        actions.send_keys(str(best_word))
        actions.send_keys(Keys.ENTER)
        actions.perform()
        time.sleep(2)
        colours=find_colours(i+1)
        if colours=="ggggg":
            print("solved")
            break
        best_word=wordle.auto_guess(best_word,colours)

    
solve()
running=True
while running==True:
    running=False if input("Quit?")=="y" else True

driver.quit()
