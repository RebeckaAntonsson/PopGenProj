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

# Some rows does not have any mtDNA haplogroup information, these rows will 
# say "n/a". Here the rows without haplgroup information are removed.
# The code says "if the column contains n/a", but the ~before AADR is an
# invert operatior for boolean. So the output is everything that does not
# match the pattern ("n/a")
filtered_AADR_df = AADR_df[~AADR_df["mtDNA haplogroup if >2x or published"].str.contains("n/a")]

# Create list with only the haplotypes, from the AADR filtered dataframe
haplogroup_list=filtered_AADR_df["mtDNA haplogroup if >2x or published"]

# Ask user to input their hapotype and save it in the hapotype variable
#st.title("Haplogroup")
#haplogroup = st.text_input("Enter Haplogroup (e.g., R1b, H1): ")
haplotype = input("Enter your haplotype for example R1b, D4b1a2a. \nDO NOT enter entire files like no fasta, csv, json etc \nDO NOT enter only mutations for example H1a1 T16093C G16213A. \nPlease enter your haplotype here: ")
print("Haplotype",haplotype)

# Calls the function that matches users input with a haplogroup
matched_haplogroup = match_haplogroup(haplotype, haplogroup_list)
print("Matched haplogroup", matched_haplogroup)

# Get the rows that match to the haplogroup 
matching_row = filtered_AADR_df[filtered_AADR_df["mtDNA haplogroup if >2x or published"] == matched_haplogroup]
print(matching_row)
