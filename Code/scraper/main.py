from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
import time
import json
import os

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
    # options.add_argument("--disable-site-isolation-trials")
    # prefs = {
    #         "profile.managed_default_content_settings.images": 2,
    #         "profile.default_content_setting_values.notifications": 2,
    #         "profile.managed_default_content_settings.stylesheets": 2,
    #         "profile.managed_default_content_settings.cookies": 2,
    #         "profile.managed_default_content_settings.javascript": 1,
    #         "profile.managed_default_content_settings.plugins": 1,
    #         "profile.managed_default_content_settings.popups": 2,
    #         "profile.managed_default_content_settings.geolocation": 2,
    #         "profile.managed_default_content_settings.media_stream": 2
    #     }

    # options.add_experimental_option("prefs", prefs)
    options.add_argument("user-data-dir=/home/sam/.config/google-chrome/Default")
    # Adding argument to disable the AutomationControlled flag 
    options.add_argument("--disable-blink-features=AutomationControlled") 
    
    # Exclude the collection of enable-automation switches 
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    
    # Turn-off userAutomationExtension 
    options.add_experimental_option("useAutomationExtension", False)
    # Changing the property of the navigator value for webdriver to undefined 
    # options.add_argument("--disable-extensions")
    # options.add_argument('--blink-settings=imagesEnabled=false')
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 

    for group_of_products in links:
        for product in group_of_products:
            link = product[-1]
            print(link)
            driver.get(link)
            print("LOADED!")
            wait = WebDriverWait(driver, timeout=2, poll_frequency=0.2)
            # Open the Specification accordion element
            wait.until(EC.element_to_be_clickable((By.ID, "product-section-key-feat"))).click()

            # Find elements in the Specification section
            headers = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.kpf__name")))
            print(len(headers))
            for header in headers:
                print(header.text)
            return 
            # _OutputHTML(driver)

            print("LOADING PAGE...")
            time.sleep(100000)
            time.sleep(3)  # Adjust as needed
            reached_page_end = False
            last_height = driver.execute_script("return document.body.scrollHeight")

            print("SCROLLING DOWN...")
            while not reached_page_end:
                driver.find_element(By.XPATH, '//body').send_keys(Keys.END)   
                time.sleep(2)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if last_height == new_height:
                        reached_page_end = True
                else:
                        last_height = new_height
            print("-=- Reached End of Page -=-")
            # time.sleep(3) # allow remaining page to load

            # div_main_specs = driver.find_elements(By.CSS_SELECTOR, "div[class='kpf__specs']")
            # try:
            #     # Wait for the alert to appear
            #     alert = driver.switch_to.alert

            #     # Check the alert text
            #     if "Share your location?" in alert.text:
            #         # If the alert is for location sharing, click on "Block"
            #         alert.dismiss()  # This clicks on the "Block" button
            #     else:
            #         # Handle other alerts if needed
            #         alert.dismiss()  # Dismiss the alert

            # except:
            #     # No alert found or other exception occurred
            #     pass
            # try:
            #     # Execute JavaScript to remove both elements
            #     driver.execute_script("""
            #         var inputElement = document.getElementById('typeahead-search-field-input');
            #         if (inputElement) {
            #             inputElement.parentNode.removeChild(inputElement);
            #         }
                    
            #         var divElement = document.querySelector('[data-testid="search-field-container"]');
            #         if (divElement) {
            #             divElement.parentNode.removeChild(divElement);
            #         }
                    
            #         var formElement = document.querySelector('[data-testid="search-field-root"]');
            #         if (formElement) {
            #             formElement.parentNode.removeChild(formElement);
            #         }
                    
            #         var typeaheadElement = document.getElementById('typeahead-container');
            #         if (typeaheadElement) {
            #             typeaheadElement.parentNode.removeChild(typeaheadElement);
            #         }

            #         var divElement2 = document.querySelector('.sui-flex.sui-font-regular.sui-items-center.sui-bg-primary.sui-text-primary.sui-px-4.sui-pt-4.sui-pb-12.sui-gap-2.sui-bg-primary.lg:sui-pb-4.lg:sui-gap-6');
            #         if (divElement2) {
            #             divElement2.parentNode.removeChild(divElement2);
            #         }
            #     """)

            #     # Now you can continue with your normal workflow, e.g., clicking on elements, scraping data, etc.

            # except Exception as e:
            #     print("Error In Element Removal:", e)
            # _OutputHTML(driver)
            try:
                # Wait for the element to be clickable
                # element = WebDriverWait(driver, 10).until(
                #     EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/section[1]/div/div[2]/div/div[1]"))
                # )
                element = driver.find_element(By.XPATH, "//*[@id='product-section-key-feat']")

                # Execute JavaScript to click on the element
                # driver.execute_script("arguments[0].click();", element)

                # Click on the element
                element.click()
                time.sleep(2)

            except Exception as e:
                print("Error in Clicking Element:", e)
            _OutputHTML(driver)
            # dropdown = driver.find_element(By.CSS_SELECTOR, "div[id='specifications']")
            dropdown = driver.find_element(By.XPATH, "//*[@id='product-section-specifications']")
            dropdown.click()
            headers = dropdown.find_elements(By.CSS_SELECTOR, "div[class='kpf__name']")
            print(len(headers))
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
