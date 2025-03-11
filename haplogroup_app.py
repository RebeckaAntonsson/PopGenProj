# -*- coding: utf-8 -*-


#import streamlit as st
import pandas as pd


#st.title("Haplogroup")
#haplogroup = st.text_input("Enter Haplogroup (e.g., R1b, H1):")


# Loads the AADR csv file into a pandas data frame
def load_AADR_data():
    AADR_df = pd.read_csv("AADR_Annotation(Sheet1).csv", sep=';', encoding='ISO-8859-1', usecols=[0,8,13,14,28])
    return AADR_df

# Function that matches the users input haplotype to the list with hapogroups
#def match_haplogroup(haplotype, haplogroup_list):
    
    
    
AADR_df = load_AADR_data()
haplogroup_list=AADR_df["mtDNA haplogroup if >2x or published"]
print(haplogroup_list.head())