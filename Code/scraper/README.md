# SETUP
```shell
# install pip is local enviornment does not have it
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

# RUNNING
```shell
python3 main.py
```