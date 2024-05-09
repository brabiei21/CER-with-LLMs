from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def has_reached_bottom(driver):
    # Get the current scroll position
    current_scroll_position = driver.execute_script("return window.pageYOffset;")
    
    # Get the maximum scroll height of the page
    max_scroll_height = driver.execute_script("return document.body.scrollHeight;")
    
    # Check if the current scroll position is at the bottom
    return current_scroll_position == max_scroll_height
def scroll_to_end(driver):
    # Scroll to the end of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
def GetAllProductURLS():
    # Launch a headless Chrome browser
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    # Navigate to the webpage
    driver.get("https://www.homedepot.com/b/Home-Decor/N-5yc1vZas6p?catStyle=ShowProducts")

    # Wait for the page to load fully
    print("LOADING PAGE...")
    time.sleep(3)  # Adjust as needed
    num_scrolls = 15  # You may need to adjust this based on the page's structure
    # # body = driver.find_element(By.TAG_NAME, "body")
    # # for _ in range(num_scrolls):
    # #     #body.send_keys(Keys.PAGE_DOWN)
    # #     time.sleep(1)  # Adjust the sleep time as needed
    # #     scroll_to_end(driver)
    # #     print("SCROLL", str(_+1), "/", num_scrolls)
    # while not has_reached_bottom(driver):
    #     scroll_to_end(driver)
    #     time.sleep(1)
    #     print("SCROLLING...")
    reached_page_end = False
    last_height = driver.execute_script("return document.body.scrollHeight")

    while not reached_page_end:
        driver.find_element(By.XPATH, '//body').send_keys(Keys.END)   
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if last_height == new_height:
                reached_page_end = True
        else:
                last_height = new_height
    time.sleep(3) # allow remaining page to load

    # Find all <div> elements with data-testid="product-header"
    target_divs = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='product-header']")

    # Iterate through each <div> and find the <a> tag within it
    links = []
    for div in target_divs:
        # Find the <a> tag within the <div>
        span_tag = div.find_element(By.TAG_NAME, "span")
        a_tag = div.find_element(By.TAG_NAME, "a")
        if a_tag:
            # Extract the href attribute
            href = a_tag.get_attribute("href")
            links.append(href)
            print("Title:", span_tag.text, "\thref:", href)
    

    # TODO: Move to next page of the product page -- currently does 1

    # Close the browser
    driver.quit()

    return links

if __name__ == '__main__':
    GetAllProductURLS()
    # for each link, get specifications
