"""
Cross-Referencing to CSV
"""

# Importing Libraries
import pandas as pd
from typing import List
import csv

# Importing CSV File for UNIPROT IDs
def import_csv(filename) -> List:
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
        ID = []
        for row in csv_reader:
            ID.append(row[0])
    return ID

# Pandas Processing
def pandas(uniprot):
    df = pd.read_csv("data.csv")
    custom_count = df[['UniProt ID', 'Count for Custom Panel']]
    custom_count = custom_count[~custom_count["Count for Custom Panel"].isnull()]
    
    list_all = df['UniProt ID'].tolist()
    list_custom = custom_count["UniProt ID"].tolist()
    output_all = [] # 
    not_in = [] # List of IDs that were converted but not in the custom count

    # Produces a list of all the UNIPROT IDs that overlap between the SOMA panel and the converted list
    for ID in uniprot:
        if ID in list_all:
            output_all.append(ID)

    # The list of converted IDs that are not in the custom panel but in the SOMA panel
    for ID in uniprot:
        if ID not in list_custom:
            if ID in output_all: 
                not_in.append(ID)
    
    print(len(not_in))

    return not_in 

def main():
    uniprot = import_csv("MEN_data.csv") 
    not_in = pandas(uniprot)
    with open("not_in_MEN_1.csv", "w") as output_file:
        write = csv.writer(output_file)
        for item in not_in:
            write.writerow([item])

if __name__ == "__main__":
    main()
