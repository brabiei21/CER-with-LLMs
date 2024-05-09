from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
import os

def GetAllProductURLS():
    
    CURRENT_PAGE = 'https://www.homedepot.com/b/Home-Decor/N-5yc1vZas6p?catStyle=ShowProducts'
    REACHED_END = False
    # Check if the file exists
    if os.path.exists('links_mem.txt'):
        # Read the existing content from the file
        with open('links_mem.txt', 'r') as f:
            content = f.readlines()
        if len(content) > 0 and content[-1] != None:
            CURRENT_PAGE = content[-1]
            print('[NOTICE] Continuing from the following page:', CURRENT_PAGE)
        else:
            print('[WARNING] nothing in memory, getting links from the very beginning')
    else:
        print('[WARNING] nothing in memory, getting links from the very beginning')

    # Launch a headless Chrome browser
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    # Navigate to the webpage
    driver.get(CURRENT_PAGE)

    while not REACHED_END:
        links = []
        # Wait for the page to load fully
        print("LOADING PAGE...")
        time.sleep(3)  # Adjust as needed
        num_scrolls = 15  # You may need to adjust this based on the page's structure

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
        results_grid = driver.find_element(By.CSS_SELECTOR, "div[class='results-wrapped']")
        target_divs = results_grid.find_elements(By.CSS_SELECTOR, "div[data-testid='product-header']")

        # Iterate through each <div> and find the <a> tag within it
        for div in target_divs:
            # Find the <a> tag within the <div>
            span_tag = div.find_element(By.TAG_NAME, "span")
            a_tag = div.find_element(By.TAG_NAME, "a")
            if a_tag:
                # Extract the href attribute
                href = a_tag.get_attribute("href")
                links.append(('title', span_tag.text, 'href', href))
                print("Title:", span_tag.text, "\thref:", href)
        
        # TODO: Fix json to be contiguous
        # dump links into file
        # Write the list of tuples to a JSON file
        # Check if the file exists
        if os.path.exists("links.json"):
            # Read the existing content from the file
            with open("links.json", 'r') as f:
                content = f.read()
            if not len(content) > 0:
                content = '[]'
        else:
            content = '[]'  # Initialize with an empty list if the file doesn't exist
        # Load existing JSON content into a Python list
        data = json.loads(content)

        # Append the new JSON object to the existing list
        data.append(links)

        with open('links.json', 'w') as f:
            json.dump(data, f)

        # Move to next page of the product page
        a_tags = driver.find_elements(By.CSS_SELECTOR, "a[class='hd-pagination__link ']")
        # FIXME: check if it loops arounds
        if a_tags[-1].get_attribute("aria-label") == None or a_tags[-1].get_attribute("aria-label") != "Next":
            REACHED_END = True
        else:
            CURRENT_PAGE = a_tags[-1].get_attribute("href")
            with open('links_mem.txt', 'a') as f:
                f.write(str(CURRENT_PAGE+'\n'))
            driver.get(CURRENT_PAGE)

    # Close the browser
    driver.quit()

    return links

def GetSpecifications():
    REACHED_END = False
    links = None
    # Check if the file exists
    if os.path.exists('links.json'):
        # Read the existing content from the file
        with open('links.json', 'r') as f:
            content = f.read()
            links = json.loads(content)
        if not (len(content) > 0 and content[-1] != None):
            print('[ERROR] No links found')
            return
    else:
        print('[ERROR] file not found, exiting function ...')
        return 

    # Launch a headless Chrome browser
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    for group_of_products in links:
        for product in group_of_products:
            link = product[-1]
            print(link)
            driver.get(link)

            print("LOADING PAGE...")
            time.sleep(3)  # Adjust as needed
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

            div_main_specs = driver.find_elements(By.CSS_SELECTOR, "div[class='kpf__specs']")
            headers = driver.find_elements(By.CSS_SELECTOR, "div[class='kpf__name']")
            print(headers[0].text)
            return 

    # Navigate to the webpage
    print(links[0][0][-1])
    return
    driver.get()

    print("LOADING PAGE...")
    time.sleep(3)  # Adjust as needed

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

if __name__ == '__main__':
    # GetAllProductURLS()
    # for each link, get specifications
    GetSpecifications()
