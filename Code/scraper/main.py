from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from concurrent.futures import ThreadPoolExecutor
import time
import json
import os
import random

DEPT_JSON = 'department_urls.json'

def file_exists(filename):
    """
    Checks if a file with the given filename exists.

    Parameters:
    filename (str): The name of the file to check.

    Returns:
    bool: True if the file exists, False otherwise.
    """
    return os.path.isfile(filename)

def write_list_to_json(data_list, filename):
    """
    Writes a list to a JSON file with the given filename.

    Parameters:
    data_list (list): The list to write to the JSON file.
    filename (str): The name of the JSON file.
    """
    try:
        with open(filename, 'w') as json_file:
            json.dump(data_list, json_file)
        print(f"Data successfully written to {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

def append_list_to_json(data_list, filename):
    """
    Appends a list to a JSON file. If the file does not exist or is empty, it creates the file and writes the list.

    Parameters:
    data_list (list): The list to append to the JSON file.
    filename (str): The name of the JSON file.
    """
    try:
        if os.path.isfile(filename) and os.path.getsize(filename) > 0:
            with open(filename, 'r') as json_file:
                existing_data = json.load(json_file)
                if not isinstance(existing_data, list):
                    raise ValueError(f"The existing data in '{filename}' is not a list.")
                existing_data.extend(data_list)
        else:
            existing_data = data_list

        with open(filename, 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)
        
        print(f"Data successfully appended to {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
def read_json_as_list(filename):
    """
    Reads the contents of a JSON file and returns it as a list.

    Parameters:
    filename (str): The name of the JSON file to read.

    Returns:
    list: The contents of the JSON file as a list.
    """
    try:
        with open(filename, 'r') as json_file:
            data_list = json.load(json_file)
        return data_list
    except Exception as e:
        print(f"An error occurred: {e}")
        return [] 
       
def write_string_to_file(content, filename):
    """
    Writes a string to a text file.

    Parameters:
    content (str): The string content to write to the file.
    filename (str): The name of the text file to write.
    """
    try:
        with open(filename, 'w') as file:
            file.write(content)
        print(f"String content successfully written to {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

def read_string_from_file(filename):
    """
    Reads the contents of a text file and returns it as a string.

    Parameters:
    filename (str): The name of the text file to read.

    Returns:
    str: The contents of the text file.
    """
    try:
        with open(filename, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
def is_file_empty(filename):
    """
    Checks if a file is empty.

    Parameters:
    filename (str): The name of the file to check.

    Returns:
    bool: True if the file is empty, False otherwise.
    """
    try:
        if os.path.isfile(filename):
            return os.path.getsize(filename) == 0
        else:
            raise FileNotFoundError(f"The file '{filename}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

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

"""
Get 'shop all' links by department
"""
def GetDepartmentURLS():
    PAGE = "https://www.homedepot.com/"

    # Launch a headless Chrome browser
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument("user-data-dir=/home/${USER}/.config/google-chrome/Default")

    # Adding argument to disable the AutomationControlled flag 
    options.add_argument("--disable-blink-features=AutomationControlled") 
    
    # Exclude the collection of enable-automation switches 
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    
    # Turn-off userAutomationExtension 
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=options)

    # Navigate to the webpage
    driver.get(PAGE)

    wait = WebDriverWait(driver, 10)

    # Locate the button using its data-testid attribute
    shop_all_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="header-button-Shop All"]')))
    shop_all_btn.click()

    # Wait for the "Shop By Department" button to become clickable
    shop_by_dept_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="menu-item-id-1BDh5E1pOmmWNMc7CHdLxj"]')))
    shop_by_dept_btn.click()

    # Locate the container holding the department buttons
    dept_btn_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.sui-flex-auto.sui-overflow-y-auto.sui-bg-primary')))
    # Find all buttons within the container
    dept_btns = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[role="button"]')))

    # Click each button
    urls = []
    num_of_buttons = len(dept_btns)
    for i in range(num_of_buttons):
        # button.click()
        container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.sui-flex-auto.sui-overflow-y-auto.sui-bg-primary')))
        btn = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[role="button"]')))
        btn[i].click()
        container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.sui-flex-auto.sui-overflow-y-auto.sui-bg-primary')))
        
        # ensure buttons are loaded
        while True:
            btns = container.find_element(By.TAG_NAME, 'ul').find_elements(By.XPATH, './/*') # get child elements of unordered list
            if len(btns) > 0: break
        
        # print(len(btns))
        urls.append(btns[0].get_attribute("href"))
        back_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Click to go back and render previous drawer menus']")))
        back_btn.click()
        rand_time()
        # print(urls)

    print(urls)
    return urls

"""
Gets the links for product pages 

Parameters:
page (string) 'shop all' department page

Returns:
list: urls of data components for a department page
"""
def GetDataComponents(page):
    PAGE = page

    # Launch a headless Chrome browser
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument("user-data-dir=/home/${USER}/.config/google-chrome/Default")
    # Adding argument to disable the AutomationControlled flag 
    options.add_argument("--disable-blink-features=AutomationControlled") 
    
    # Exclude the collection of enable-automation switches 
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    
    # Turn-off userAutomationExtension 
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=options)

    # Navigate to the webpage
    driver.get(PAGE)
    driver.execute_script("document.body.style.zoom='25%'")

    wait = WebDriverWait(driver, 10)
    try:
        placeholder_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class*="placeholder"]')))
        # Once the placeholder is found, wait for it to disappear
        for elem in placeholder_elements:
            wait.until(EC.staleness_of(elem))
    except:
        driver.get(page)
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
        driver.execute_script("document.body.style.zoom='25%'")
            
    try:
        item_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-component-name="VisualNavigation"]')))
        items = item_container.find_elements(By.TAG_NAME, 'a')
    except:
        try:
            side_nav_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-component-name="SideNavigation"]')))
            items = side_nav_div.find_elements(By.TAG_NAME, 'a')
        except:
            print("WARNING: COULD NOT FIND LINKS FOR PAGE\n", page)
            return []
    
    urls = []
    for item in items:
        url = item.get_attribute('href')
        urls.append(url)
        # print(url)
    
    return urls

def _GetProductURLS(page):
    # Launch a headless Chrome browser
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    
    driver.get(page)
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
    driver.execute_script("document.body.style.zoom='25%'")

    wait = WebDriverWait(driver, 10)
    
    try:
        urls = []
        i = 1
        seen_all_products = False
        while not seen_all_products:
            product_divs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-component^="product-pod:ProductPod:"]')))
            
            for prod in product_divs:
                url = prod.find_element(By.TAG_NAME, "a").get_attribute('href')
                urls.append(url)
            
            pagination_lis = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[class=hd-pagination__item]')))
            next_page_found = False
            for li in pagination_lis:
                if li.text != '...' and int(li.text) > i:
                    # next_page = 
                    btn = li.find_element(By.TAG_NAME, 'a')
                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(3)
                    wait = WebDriverWait(driver, 10)
                    # btn.click()#.get_attribute('href')
                    i += 1
                    # driver.get(next_page)
                    next_page_found = True
                    break # end for-loop

            if not next_page_found:
                seen_all_products = True  # All pages have been seen
        
        print("\n\n(i, len(urls))", i, len(urls), "\n\n")
        # print(urls)
        
        return urls
    except:
        print("WARNING: Page Does Not Have Product Grid.\n", page, "\nSkipping...\n")
        return None
def _GetSpecifications(page):
    # Launch a headless Chrome browser
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument("user-data-dir=/home/${USER}/.config/google-chrome/Default")
    # Adding argument to disable the AutomationControlled flag 
    options.add_argument("--disable-blink-features=AutomationControlled") 
    
    # Exclude the collection of enable-automation switches 
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    
    # Turn-off userAutomationExtension 
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=options)

    # Navigate to the webpage
    driver.get(page)
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
    driver.execute_script("document.body.style.zoom='25%'")
    time.sleep(3)
    
    wait = WebDriverWait(driver, 10)
    
    specification_accordion = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[id="product-section-key-feat"]')))
    btn = specification_accordion.find_element(By.CSS_SELECTOR, 'div[role="button"]')
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(3)
        
    table_headers = specification_accordion.find_elements(By.TAG_NAME, 'h4')
    # print(len(table_headers))
    content_tables = specification_accordion.find_elements(By.TAG_NAME, 'table')
    
    specifications = []
    length = len(content_tables)
    # print("Length:", length)
    for i in range(length):
        try:
            title = table_headers[i].get_attribute('innerHTML').strip()
            # print("TITLE:", title)
            rows = content_tables[i].find_elements(By.TAG_NAME, 'tr')
            # print("Number of Rows: ", len(rows))
            content = []
            for row in rows:
                headers = row.find_elements(By.TAG_NAME, "th")
                descriptions = row.find_elements(By.TAG_NAME, "td")
                content_dictionary = dict((obj1.find_element(By.TAG_NAME, 'p').get_attribute('innerHTML').strip(), obj2.find_element(By.TAG_NAME, 'p').get_attribute('innerHTML').strip()) for obj1, obj2 in zip(headers, descriptions))
                content.append(content_dictionary)
            specifications.append((title, content))
            # print(content)
        except Exception as e:
            print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            print("Error: .\n\n", e, "\n\n")
            print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")       
    
    # print(specifications)
    product_title = driver.find_element(By.CSS_SELECTOR, 'span[data-component="ProductDetailsTitle"]').find_element(By.TAG_NAME, 'h1').get_attribute('innerHTML').strip()
    specifications.append(('product', product_title))
    # print(product_title)
    return specifications

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
        nav_tag = driver.find_element(By.CSS_SELECTOR, "nav[aria-label='Pagination Navigation']")
        li_tags = nav_tag.find_elements(By.TAG_NAME, "button")
        print(len(li_tags))
        if li_tags[-1].is_enabled():
            print(li_tags[-1].get_attribute("aria-label"))
            print("Current Page:", driver.current_url)
            # ActionChains(driver).click(li_tags[-1]).perform()
            elem = li_tags[-1]

            # Use JavaScript to click
            driver.execute_script("arguments[0].click();", elem)

            elem.click()
            rand_time(mode=2)
            CURRENT_PAGE = driver.current_url
            print("Moving to New Page:", CURRENT_PAGE)
            with open('links_mem.txt', 'a') as f:
                f.write(str(CURRENT_PAGE+'\n'))
            # driver.get(CURRENT_PAGE)
        else:
            REACHED_END = True

        # FIXME: check if it loops arounds
        # if a_tags[-1].get_attribute("aria-label") == None or a_tags[-1].get_attribute("aria-label") != "Next":
        #     REACHED_END = True
        # else:
        #     CURRENT_PAGE = a_tags[-1].get_attribute("href")
        #     with open('links_mem.txt', 'a') as f:
        #         f.write(str(CURRENT_PAGE+'\n'))
        #     driver.get(CURRENT_PAGE)

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

    # TODO: group_index and product index memory
    # """
    MEM_GROUP_INDEX = 0
    MEM_PRODUCT_INDEX = 0
    if os.path.exists('product_page_mem.txt'):
        # Read the existing content from the file
        with open('product_page_mem.txt', 'r') as f:
            content = f.readlines()
        if len(content) > 0 and content[-1] != None:
            MEM_GROUP_INDEX = int(content[0])
            MEM_PRODUCT_INDEX = int(content[1])
            print('[NOTICE] Continuing from Group Index:', MEM_GROUP_INDEX, 'At Product Index:', MEM_PRODUCT_INDEX)
        else:
            print('[WARNING] nothing in memory, getting product index info from the very beginning')
    else:
        print('[WARNING] nothing in memory, getting product index info from the very beginning')
    # """

    FIRST_ITERATION = True
    MAX_CONTINUES = 10
    CONTINUE_COUNT = 0
    for group_index, group_of_products in enumerate(links[MEM_GROUP_INDEX:] if FIRST_ITERATION else links):
        for product_index, product in enumerate(group_of_products[MEM_PRODUCT_INDEX:] if FIRST_ITERATION else group_of_products):

            print(product)
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
                        
                        if CONTINUE_COUNT >= MAX_CONTINUES:
                            print("REFRESHING...")
                            CONTINUE_COUNT = 0
                            driver.refresh()
                            continue
                        
                        driver.find_element(By.XPATH, '//body').send_keys(Keys.END)   # Scroll down
                        CONTINUE_COUNT += 1
                        
                        continue
                    else:
                        if os.path.exists("specifications.json"):
                            # Read the existing content from the file
                            with open("specifications.json", 'r') as f:
                                content = f.read()
                            if not len(content) > 0:
                                content = '[]'
                        else:
                            content = '[]'  # Initialize with an empty list if the file doesn't exist
                        # Load existing JSON content into a Python list
                        data = json.loads(content)

                        # Append the new JSON object to the existing list
                        data.append(all_th_td_pairs)

                        with open('specifications.json', 'w') as f:
                            json.dump(data, f)

                        # TODO: Update index memory here
                        """
                        FIX MEEEEEEEEEEE!!!!!!!! RRRRRREEEEEEEEEEEEE
                        """
                        with open('product_page_mem.txt', 'w') as f:
                            if FIRST_ITERATION:
                                f.write(str(group_index + MEM_GROUP_INDEX) + '\n' + str(product_index + MEM_PRODUCT_INDEX) + '\n')
                            else:
                                f.write(str(group_index) + '\n' + str(product_index) + '\n')

                        UNSUCCESSFUL = False
                except Exception as e:
                    # print("ERROR:", e)
                    print("ERROR -- REFRESHING")
                    driver.refresh()
                    time.sleep(rand_time(mode=3))
                    print("CONTINUING...")
        FIRST_ITERATION = False if FIRST_ITERATION else FIRST_ITERATION # turn off flag

if __name__ == '__main__':
    # GET DEPARTMENT URLS
    if file_exists(DEPT_JSON):
        deps = read_json_as_list(DEPT_JSON)
    else: 
        deps = GetDepartmentURLS()
        write_list_to_json(deps, DEPT_JSON)
    
    
    
    # GET PRODUCT LISTING URLS FROM DEPARTMENTS
    if file_exists('last_dept.txt') and is_file_empty('last_dept.txt'):
        product_grid_urls = read_json_as_list('prod_grid.json')
    else:
        last_dept = read_string_from_file('last_dept.txt')
        skip = True if last_dept != None else False
        
        for dep in deps:
            if dep == last_dept: skip = False
            if skip: continue
            
            write_string_to_file(dep, 'last_dept.txt')
            print("\n\nCURRENT DEPARTMENT LINK:\n", dep, "\n\n\n")
            prod_urls = GetDataComponents(dep)
            print(prod_urls)
            append_list_to_json(prod_urls, 'prod_grid.json')
        
        write_string_to_file('', 'last_dept.txt')
        product_grid_urls = read_json_as_list('prod_grid.json')
    
    
    
    # GET PRODUCT URLS FROM LISTINGS
    last_grid_url = read_string_from_file('last_grid_url.txt')
    skip = True if last_grid_url != None else False
    for link in product_grid_urls:
        if link == last_grid_url: skip = False
        if skip: continue
        
        write_string_to_file(link, 'last_grid_url.txt')
        product_links = _GetProductURLS(link)
        if product_links != None:
            append_list_to_json(product_links, 'links.json')
    write_string_to_file('', 'last_grid_url.txt')


    # GET PRODUCT SPECIFICATIONS
    last_product_url = read_string_from_file('last_product_url.txt')
    skip = True if last_product_url != None else False
    product_links = read_json_as_list('links.json')
    for product in product_links:
        if product == last_product_url: skip = False
        if skip: continue
        
        print("CURRENT PRODUCT:", product)
        specifications = _GetSpecifications(product)
        if len(specifications) > 0:
            append_list_to_json(specifications, 'product_specifications.json')
        else:
            print("Empty Specifications, Skipping...")
        write_string_to_file(product, 'last_product_url.txt')
    write_string_to_file('', 'last_product_url.txt')