"""
Generating a list of UNIPROT IDs from GENOME NAMES

In order to generate the list, the code below contacts the Uniprot API 
to receive data regarding associated UNIPROT names
"""

# Importing Libraries
import os
import csv
from tqdm import tqdm 
from typing import List
import requests

# Importing CSV File for GENES
def import_csv(filename):
    """
    Imports the a csv file containing a list of genes and returns the 
    genes as a list object
    """
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        genes = []
        for row in csv_reader:
            genes.append(row[0])

    return genes

def nameChecker(name):
    """
    Determines if a filename contains .csv extension. If it does not, the
    program will fix it automatically. 
    """
    try:
        name = int(name)
        return name
    except:
        if ".csv" in name:
            return name
        else:
            return name + ".csv"

def API_response(gene_name):
    """
    Interprets the response from the UNIPROT API
    """
    api_url = f"https://rest.uniprot.org/uniprotkb/search?query=reviewed:true+AND+organism_id:9606+AND+gene:{gene_name}&format=tsv"
    response = requests.get(api_url)

    index = 0
    results = []
    for row in response.iter_lines():
        result = row.decode("utf-8").split("\t")
        if index != 0:
            results.append(result[0])
        index += 1
    return results

def create_IDList():
    """
    Calls upon the API response function to general a list of UNIPROT IDs
    based on the given list of gene names.
    """
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
    
    out_filename = input("Type the filename of the output file: ")

    rows = []
    for gene_name in tqdm(gene_names):
        try:
            for protein_name in API_response(gene_name):
                rows.append([protein_name])
        except KeyboardInterrupt: break
        except Exception as e:
            print(e)
            continue

    print("Conversion Completed!") 

    with open(out_filename, 'w') as outFile:
        write = csv.writer(outFile)
        write.writerows(rows)

    return "Exit"

def user_control():
    """
    Enables the text user interface for the API conversion process
    """
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