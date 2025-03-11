# -*- coding: utf-8 -*-


#import streamlit as st
import pandas as pd


# Loads the AADR csv file into a pandas data frame
def load_AADR_data():
    #For the real deal
    #AADR_df = pd.read_excel("AADR Annotations 2025.xlsx")
    # for testing
    AADR_df = pd.read_excel("test_AADR.xlsx", engine="openpyxl")
    
    
    return AADR_df

# Function that matches the users input haplotype to the list with hapogroups
def match_haplogroup(haplotype, haplogroup_list):
    # Convert all haplogrpups to strings
    haplogroup_list = [str(hg) for hg in haplogroup_list]
    #Find best matching haplogroup to users haplotype from the haplogroup_list
    matches = [hg for hg in haplogroup_list if haplotype.startswith(hg)]
    
    return max(matches, key=len) if matches else None
    
    
AADR_df = load_AADR_data()
print(AADR_df.head())
print(AADR_df.columns)
# Some rows does not have any mtDNA haplogroup information, these rows will 
# just say "..". Here the rows without haplgroup information are removed.
#filtered_AADR_df = AADR_df[AADR_df["mtDNA haplogroup if >2x or published"] != ".."]
# Also (or maybe change to removing n/a (<2x))
#print(filtered_AADR_df.head())

# Create list with only the haplotypes, from the AADR filtered dataframe
#haplogroup_list=filtered_AADR_df["mtDNA haplogroup if >2x or published"]

#st.title("Haplogroup")
#haplogroup = st.text_input("Enter Haplogroup (e.g., R1b, H1): ")
#haplotype = input("Enter your haplotype (e.g., R1b, H1): ")

# Calls the function that matches users input with a haplogroup
#matched_haplogroup = match_haplogroup(haplotype, haplogroup_list)
#print(matched_haplogroup)

#matching_row = filtered_AADR_df[filtered_AADR_df["mtDNA haplogroup if >2x or published"] == matched_haplogroup]
#print(matching_row)
