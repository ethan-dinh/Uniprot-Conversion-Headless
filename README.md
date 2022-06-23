# Converting Gene Names to UniProt IDs

This is a headless python implementation to convert a list of gene names to their respective UniProt IDs. The program works by contacting the UniProt API to scrape their database for similar matches. 

## Overview

There are two main conversion programs: a selenium implementation and an API implementation.
a. Selenium Implementation – This program utilizes selenium to perform a query search and an HTML analysis to scrape data. However, since UNIPROT updated their website, the selenium implementation no longer works.
b. API Implementation – This program communicates with the UNIPROT API in order to send and recieve information. 
