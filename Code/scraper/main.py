from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
import time
import json
import os
import random

def rand_time(A=0, B=0, mode=1):
    """
    Returns a random number between A and B (inclusive) based on the mode.
    
    Parameters:
    A (int): The lower bound of the range.
    B (int): The upper bound of the range.
    mode (str): The mode of operation. Can be 'fast', 'short', or 'long'.
    
    Returns:
    int: A random number between A and B (inclusive).
    """
    if mode in ['fast', 1, 'short', 2, 'long', 3]:
            wait_times = {
                'fast': (0.5, 3), 
                'short': (3, 6),
                'long': (6, 15),
                1: (0.5, 3), 
                2: (3, 6),
                3: (6, 15)
            }
            
            # Get a random wait time within the specified range for the mode
            wait_time = random.uniform(*wait_times[mode])
            return wait_time
    
    # Return a random number between A and B (inclusive)
    return random.randint(A, B)

def _OutputHTML(driver):
    # Open a file to write the HTML content
    with open("page_content.html", "w", encoding="utf-8") as f:
        # Iterate over all elements on the page
        for element in driver.find_elements(By.XPATH, "//*"):
            # Get the HTML content of each element
            html_content = element.get_attribute("outerHTML")
            # Write the HTML content to the file
            f.write(html_content + "\n")

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

    # # Define the proxy server 
    # PROXY = "18.223.25.15:80"
    # # Add the proxy as argument 
    # options.add_argument("--proxy-server=%s" % PROXY)

    options.add_argument("user-data-dir=/home/sam/.config/google-chrome/Default")
    # Adding argument to disable the AutomationControlled flag 
    options.add_argument("--disable-blink-features=AutomationControlled") 
    
    # Exclude the collection of enable-automation switches 
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    
    # Turn-off userAutomationExtension 
    options.add_experimental_option("useAutomationExtension", False)
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 

    # Initializing a list with two Useragents 
    useragentarray = [ 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36", 
    ] 

    for i in range(len(useragentarray)): 
        # Setting user agent iteratively as Chrome 108 and 107 
        driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": useragentarray[i]}) 
        print(driver.execute_script("return navigator.userAgent;")) 

    for group_of_products in links:
        for product in group_of_products:
            link = product[-1] # get last element in link tuple (href link)
            print(link)
            driver.get(link)
            wait = WebDriverWait(driver, timeout=5)
            UNSUCCESSFUL = True
            while UNSUCCESSFUL:
                time.sleep(rand_time(mode=2)) 
                # Open the Specification accordion element
                try:
                    # element = driver.find_element(By.XPATH, "//*[@id='product-section-key-feat']")
                    element = wait.until(EC.element_to_be_clickable((By.ID, "product-section-key-feat")))
                    element.click()
                    # headers = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[class='kpf__name']")))
                    time.sleep(rand_time(mode=1)) 
                    all_th_td_pairs = {}  # Initialize an empty dictionary to store all key-value pairs
                    th_td_pairs = {}  # Initialize an empty dictionary for the current grid

                    grids = element.find_elements(By.TAG_NAME, "table")
                    time.sleep(1)
                    for grid in grids:
                        th_tags = grid.find_elements(By.TAG_NAME, "th")
                        td_tags = grid.find_elements(By.TAG_NAME, "td")
                        
                        # th_td_pairs = {}  # Initialize an empty dictionary for the current grid

                        for th_tag, td_tag in zip(th_tags, td_tags):
                            th_p_tags = th_tag.find_elements(By.TAG_NAME, "p")
                            td_p_tags = td_tag.find_elements(By.TAG_NAME, "p")

                            th_texts = [p.text for p in th_p_tags]
                            td_texts = [p.text for p in td_p_tags]

                            th_td_pairs.update(dict(zip(th_texts, td_texts)))  # Update the dictionary with new pairs for each iteration

                        all_th_td_pairs.update(th_td_pairs)  # Update the main dictionary with pairs for the current grid

                    print(all_th_td_pairs)
                    print(th_td_pairs)
                    if not all_th_td_pairs:
                        print("Dictionary Empty! Trying Again ... ")
                        continue
                    else:
                        UNSUCCESSFUL = False
                        # for th_tag, td_tag in zip(th_tags, td_tags):
                        #     th_p_tags = th_tag.find_elements(By.TAG_NAME, "p")
                        #     td_p_tags = td_tag.find_elements(By.TAG_NAME, "p")
                            
                        #     for p in th_p_tags:
                        #         print(p.text, '\t')
                            
                        #     for p in td_p_tags:
                        #         print(p.text)
                except Exception as e:
                    # print("ERROR:", e)
                    print("ERROR -- REFRESHING")
                    driver.refresh()
                    time.sleep(rand_time(mode=3))
                    print("CONTINUING...")
                    # element = driver.find_element(By.XPATH, "//*[@id='product-section-key-feat']")
                    # element.click()
                    # time.sleep(3)
                    # grids = element.find_elements(By.TAG_NAME, "table")
                    # print("Grid Length", len(grids))
                    # for grid in grids:
                    #     th_tags = grid.find_elements(By.TAG_NAME, "th")
                    #     td_tags = grid.find_elements(By.TAG_NAME, "td")

                    #     for th_tag, td_tag in zip(th_tags, td_tags):
                    #         th_p_tags = th_tag.find_elements(By.TAG_NAME, "p")
                    #         td_p_tags = td_tag.find_elements(By.TAG_NAME, "p")

                    #     th_texts = [p.text for p in th_p_tags]
                    #     td_texts = [p.text for p in td_p_tags]
                    #     print(th_texts, '\n', td_texts)
                    #     th_td_pairs = dict(zip(th_texts, td_texts))
                    #     print(th_td_pairs)

if __name__ == '__main__':
    # GetAllProductURLS()
    # for each link, get specifications
    GetSpecifications()
