"""
Generating a list of UNIPROT IDs from GENOME NAMES
"""

# Importing Libraries
import os
import csv
from tqdm import tqdm 
from typing import List
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 

# Importing CSV File for GENES
def import_csv(filename):
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
        genes = []
        for row in csv_reader:
            genes.append(row[0])

    return genes   

# Configuring Selenium
chromedriver = "/Users/ethandinh/Desktop/Personal/Automated Scripts/chromedriver"
option = webdriver.ChromeOptions()
option.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
option.add_experimental_option("excludeSwitches", ['enable-automation'])
option.headless = True
s = Service(chromedriver)
driver = webdriver.Chrome(service=s, options=option)

def scrape(name) -> List:
    search_area = driver.find_element(By.ID, "query")
    search_area.clear()
    search_area.send_keys(name)
    search_area.send_keys(Keys.RETURN)

    for i in range(1,5):
        entry = driver.find_element(By.XPATH, f"//table/tbody/tr[{i}]/td[3]").text
        if "HUMAN" in entry:            
            return driver.find_element(By.XPATH, f"//table/tbody/tr[{i}]/td[2]").text

def nameChecker(name):
    try:
        name = int(name)
        return name
    except:
        if ".csv" in name:
            return name
        else:
            return name + ".csv"

def create_IDList():
    file_names = []
    with os.scandir('./Data') as entries:
        counter = 1
        for entry in entries:
            print(f"({counter})", entry.name)
            file_names.append(entry.name)
            counter += 1
        print(f"({counter}) Return home\n")
        
    filename = nameChecker(input("Type the filename or select from the options above: "))
    if isinstance(filename, int):
        if filename > len(file_names):
            print()
            return "Exit"
        filename = file_names[filename - 1]

    gene_names = import_csv("./Data/" + filename)
    driver.get("https://legacy.uniprot.org/")

    out_filename = input("Type the filename of the output file: ")

    rows = []
    for i in tqdm(range(len(gene_names))):
        try:
            rows.append([scrape(gene_names[i])])
        except:
            continue

    print("Conversion Completed!")

    with open(out_filename, 'w') as outFile:
        write = csv.writer(outFile)
        write.writerows(rows)

    return "Exit"

def user_control():
    print("Please select from the following: \n (a) Generate UNIPROT ID file from Gene file (.csv) \n (b) A UNIPROT ID file has already been generated \n (c) Exit \n")
    user_input = input("Selection: ")

    if user_input in ['a', 'A']:
        if create_IDList() == "Exit":
            return True
    elif user_input in ['b', 'B']:
        pass
    elif user_input in ['c', 'C']:
        return False
    else:
        print("Invalid option!\n")
        return True
        
# -------------------------------- Main Function --------------------------------
def main():
    _continue = True
    while _continue:
        _continue = user_control()

if __name__ == "__main__":
    main()