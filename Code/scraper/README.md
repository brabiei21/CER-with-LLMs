# SETUP
Using Python 3.10
```shell
# install pip if local enviornment does not have it, otherwise skip to next step
python3 -m ensurepip --upgrade

# install virtual enviornment package and create enviornment
python3 -m pip install virtualenv
python3 -m venv .env # rename folder to be hidden if needed

# to start enviornment
source .env/bin/activate
# for Windows 
env/Scripts/activate.bat # In CMD
env/Scripts/Activate.ps1 # In Powershell

# install required packages
pip install -r requirements.txt
# take a look at the installed packages
pip list

# to deactiviate when no longer working on scraper
deactivate
```

By default, Selenium 4 is compatible with Chrome v75 and greater. Note that the version of the Chrome browser and the version of chromedriver must match the major version.
Drivers can be found here: https://chromedriver.storage.googleapis.com/index.html
However, you really just need Chrome to be installed:
https://www.google.com/chrome/?platform=mac
https://www.google.com/chrome/?platform=linux
https://www.google.com/chrome/?platform=windows

# RUNNING
```shell
python3 main.py
```

# INFO
The prupose of this section is to provide additional information about particular descisions in designing the scraper.

There is an anti-bot protection on the product webpage. To circumvent this, it was found that the prtoection used was based on indicator WebDriver flags.
https://www.zenrows.com/blog/selenium-avoid-bot-detection#disable-automation-indicator-webdriver-flags

It also seems that adding the user configuration is required to be udetected:
- Linux `options.add_argument("user-data-dir=/home/${USER}/.config/google-chrome/Default")`
- Windows `options.add_argument("user-data-dir=C:\Users\<username>\AppData\Local\Google\Chrome\User Data\Default")`
- Mac `options.add_argument("user-data-dir=Users/<username>/Library/Application Support/Google/Chrome/Default")`

It should also be noted that **if the scraper is ran too many times in short time span, the anti-bot will be in effect**. One way to circumvent this is using a proxy. Another is simply waiting a while, which isn't the best option.

The function `rand_time()` was implemented to simulate user input (to an extent). Some websites can detect if a bot is being used if the user interaction is too consistent (i.e everything is clicked within 1/100 of a second). There is a docstring explaing how to function works, but there are 3 presets and the developer can choose a time between `A` and `B` (inclusive) to input for `time.sleep` 