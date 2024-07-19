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
        

def append_dict_to_json(data_dict, filename):
    """
    Appends a dictionary to a JSON file. If the file does not exist or is empty, it creates the file and writes the dictionary.

    Parameters:
    data_dict (dict): The dictionary to append to the JSON file.
    filename (str): The name of the JSON file.
    """
    try:
        if os.path.isfile(filename) and os.path.getsize(filename) > 0:
            with open(filename, 'r') as json_file:
                existing_data = json.load(json_file)
                if not isinstance(existing_data, dict):
                    raise ValueError(f"The existing data in '{filename}' is not a dictionary.")
                existing_data.update(data_dict)
        else:
            existing_data = data_dict

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
    
    try:
        specification_accordion = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[id="product-section-key-feat"]')))
        btn = specification_accordion.find_element(By.CSS_SELECTOR, 'div[role="button"]')
        driver.execute_script("arguments[0].click();", btn)
    except Exception as e:
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        print("Error: Unable to click specification dropdown \n\n", e, "\n\n")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")   
    time.sleep(3)
    
    try:
        table_headers = specification_accordion.find_elements(By.TAG_NAME, 'h4')
        content_tables = specification_accordion.find_elements(By.TAG_NAME, 'table')
    except Exception as e:
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        print("Error: Unable to get Headers and Tables \n\n", e, "\n\n")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-") 
    
    specifications = []
    length = len(content_tables)
    for i in range(length):
        try:
            title = table_headers[i].get_attribute('innerHTML').strip()
            rows = content_tables[i].find_elements(By.TAG_NAME, 'tr')
            content = []
            for row in rows:
                headers = row.find_elements(By.TAG_NAME, "th")
                descriptions = row.find_elements(By.TAG_NAME, "td")
                # Function to check if an element has a class containing "hidden"
                def has_hidden_class(element):
                    class_attribute = element.get_attribute("class")
                    return "hidden" in class_attribute

                # Filter out elements with "hidden" in their class attribute
                filtered_headers = [header for header in headers if not has_hidden_class(header)]
                filtered_descriptions = [description for description in descriptions if not has_hidden_class(description)]
                headers, descriptions= filtered_headers, filtered_descriptions
                try:
                    content_dictionary = dict((obj1.find_element(By.TAG_NAME, 'p').get_attribute('innerHTML').strip(), obj2.find_element(By.TAG_NAME, 'p').get_attribute('innerHTML').strip()) for obj1, obj2 in zip(headers, descriptions))
                    content.append(content_dictionary)
                except Exception as e:
                    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                    print("Error: Creating Dictionary \n\n", e, "\n\n")
                    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                    time.sleep(999)
            
            # Using dictionary comprehension with unpacking
            flattened_dict = {key: value for d in content for key, value in d.items()}
            
            specifications.append((title, flattened_dict))
        except Exception as e:
            print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            print("Error: Within For-Loop\n\n", e, "\n\n")
            print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")       
    
    # GET PRODUCT TITLE
    product_title = None
    while product_title == None:
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-component="ProductDetailsTitle"]')))
            product_title = driver.find_element(By.CSS_SELECTOR, 'span[data-component="ProductDetailsTitle"]').find_element(By.TAG_NAME, 'h1').get_attribute('innerHTML').strip()
            specifications.append(('product', product_title))
        except Exception as e:
            driver.refresh()
    
    # FLATTEN SPECIFICATIONS TO BE A PROPER DICTIONARY
    flattened_dict = {item[0]: item[1] for item in specifications}
    l = {}
    l[product_title] = flattened_dict
    specifications = l
    # specifications = (product_title, flattened_dict)
    
    return specifications

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
    i, total_links = 0, len(product_links)
    for product in product_links:
        i+=1
        if product == last_product_url: skip = False
        if skip: continue
        
        print("\n(",i,",",total_links,")CURRENT PRODUCT:", product, "\n")
        write_string_to_file(product, 'last_product_url.txt')
        specifications = _GetSpecifications(product)
        if len(specifications) > 0:
            append_dict_to_json(specifications, 'product_specifications.json')
        else:
            print("\nEmpty Specifications, Skipping...\n")
        
    write_string_to_file('', 'last_product_url.txt')