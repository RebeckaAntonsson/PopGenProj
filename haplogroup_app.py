# -*- coding: utf-8 -*-


#import streamlit as st
import pandas as pd


# Loads the AADR csv file into a pandas data frame
def load_AADR_data():
    #For the real deal
    #AADR_df = pd.read_excel("AADR Annotations 2025.xlsx")
    # for testing
    AADR_df = pd.read_excel("test_AADR.xlsx", engine="openpyxl", usecols=[0,8,13,14,28])
    
    return AADR_df

# Function that matches the users input haplotype to the list with hapogroups
def match_haplogroup(haplotype, haplogroup_list):
    # Convert all haplogrpups to strings
    haplogroup_list = [str(hg) for hg in haplogroup_list]
    #Find best matching haplogroup to users haplotype from the haplogroup_list
    matches = [hg for hg in haplogroup_list if haplotype.startswith(hg)]
    
    return max(matches, key=len) if matches else None
    
    
AADR_df = load_AADR_data()
# Rename one of the very long column names
AADR_df = AADR_df.rename(columns={"Date mean in BP in years before 1950 CE [OxCal mu for a direct radiocarbon date, and average of range for a contextual date]": "Years before 1950", })

# Some rows does not have any mtDNA haplogroup information, these rows will 
# say "n/a". Here the rows without haplgroup information are removed.
# The code says "if the column contains n/a", but the ~before AADR is an
# invert operatior for boolean. So the output is everything that does not
# match the pattern ("n/a")
filtered_AADR_df = AADR_df[~AADR_df["mtDNA haplogroup if >2x or published"].str.contains("n/a")]
# Rename column since it no longer contains n/a values
filtered_AADR_df = filtered_AADR_df.rename(columns={"mtDNA haplogroup if >2x or published" : "Haplogroup"})

# Create list with only the haplotypes, from the AADR filtered dataframe
haplogroup_list=filtered_AADR_df["Haplogroup"]

# Ask user to input their hapotype and save it in the hapotype variable
#st.title("Haplogroup")
#haplogroup = st.text_input("Enter Haplogroup (e.g., R1b, H1): ")
haplotype = input("Enter your haplotype for example R1b, D4b1a2a. \nDO NOT enter entire files like no fasta, csv, json etc \nDO NOT enter only mutations for example H1a1 T16093C G16213A. \nPlease enter your haplotype here: ")
print("Haplotype",haplotype)

# Calls the function that matches users input with a haplogroup
matched_haplogroup = match_haplogroup(haplotype, haplogroup_list)
print("Matched haplogroup", matched_haplogroup)

# Get the rows that match to the haplogroup 
matching_rows = filtered_AADR_df[filtered_AADR_df["Haplogroup"] == matched_haplogroup]

oldest_match = matching_rows.nlargest(1,"Years before 1950")

print(matching_rows)
print(oldest_match)