
#%% Import statements
import requests
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import html


# %%
# STEP 1: Data Extraction 1
# Save program name and its url

# Download webdriver for a browser and add its path
driver = webdriver.Chrome(executable_path='/Users/alp/Desktop/chromedriver')
driver.get('https://bugcrowd.com/programs')

# After inspecting the website, the elements with the class name: bc-panel__title contain name and urls of the programs
panel_titles = driver.find_elements_by_class_name('bc-panel__title')

p_names = [] # list of program names
p_urls = [] # list of program urls

for item in panel_titles:
    p_names.append(item.text)
    p_urls.append(item.find_element_by_css_selector('a').get_attribute('href'))



# Add names and urls to a dataframe and convert to csv
table = pd.DataFrame()
table['name'] = p_names
table['url'] = p_urls
table.to_csv('data/program-list.csv', index=False)


#%%
# STEP 2: Data Extraction 2
# Read csv file and retrieve program information for each program

df = pd.read_csv('data/program-list.csv') # read again to comply with the task

info_dict = dict()

for index, row in df.iterrows():
    driver.get(row['url']) # Go to url of the program

    try:
        info = driver.find_element_by_class_name('bounty-content')
        info_dict[row['name']] = info.text
    except:
        info = ''
        info_dict[row['name']] = info


#%%
# Quit webdriver
driver.quit()




# %%
