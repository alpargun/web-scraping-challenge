
# %% STEP 1: Data Extraction 1
# Save program name and its url

import requests
import pandas as pd
import json


source_url = "https://bugcrowd.com"
json_url = source_url + "/programs.json"

content = requests.get(json_url).text
parsed_json = json.loads(content)

p_names = [] # list of program names
p_urls = [] # list of program urls

for idx, val in enumerate(parsed_json['programs']):
    p_names.append(val['name'])
    p_urls.append(source_url + val['program_url'])

# Add names and urls to a dataframe and convert to csv
table = pd.DataFrame()
table['Name'] = p_names
table['URL'] = p_urls
table.to_csv('data/program-list.csv', index=False)


# -------------------------------------------------------------------------------
#%% STEP 2: Data Extraction 2
# Read csv file and retrieve program information for each program

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Download webdriver for a browser and add its path
driver = webdriver.Chrome(executable_path='/Users/alp/Desktop/chromedriver')

df = pd.read_csv('data/program-list.csv') # read again to comply with the task

info_dict = dict() # Keep the info as a dictionary to see corresponding program name for convenience

for index, row in df.iterrows():
    driver.get(row['URL']) # Go to url of the program

    time.sleep(0.2) # wait to load all content
    info = driver.find_element(By.CLASS_NAME, 'bounty-content')
    info_dict[row['Name']] = info.text


#--------------------------------------------------------------------------------
#%% STEP 3: Data Analysis
# Read program information and extract min and max dollar amounts. 

import re
import numpy as np

min_amounts = []
max_amounts = []

for key in info_dict:
    print(key)
    dollars = [x[0] for x in re.findall('(\$[0-9]+(\,[0-9]+)?)', info_dict[key])]

    # Remove '$' and ',' from amounts    
    for idx, val in enumerate(dollars):
        dollars[idx] = float(val.replace('$', '').replace(',', ''))
    print(dollars)
    # Find min and max values
    if dollars:
        min_amounts.append(np.min(dollars))
        max_amounts.append(np.max(dollars))
    else:
        min_amounts.append(np.nan)
        max_amounts.append(np.nan)  

# Add max and min amounts to the table
table['MinBounty'] = min_amounts
table['MaxBounty'] = max_amounts


#%% STEP 4: Result Processing
# Histogram graph for min and max amounts

import plotly.express as px

px.histogram(table, x="MinBounty")





#%%
# Quit webdriver
driver.quit()




# %%
