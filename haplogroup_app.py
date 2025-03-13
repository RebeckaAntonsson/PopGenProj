# -*- coding: utf-8 -*-


import streamlit as st
import pandas as pd


# Loads the AADR csv file into a pandas data frame
def load_AADR_data():
    #For the real deal
    AADR_df = pd.read_excel("AADR_Annotations_2025.xlsx", engine="openpyxl", usecols=[0,8,13,14,28])
    # for testing
    #AADR_df = pd.read_excel("test_AADR.xlsx", engine="openpyxl", usecols=[0,8,13,14,28])
    
    return AADR_df

def load_VIP_file():
    VIP_df = pd.read_excel("VIPHaplogroups.xlsx")
    
    return VIP_df

# Function that matches the users input haplotype to the list with hapogroups
def match_haplogroup(haplotype, haplogroup_list):
    # Convert all haplogrpups to strings
    haplogroup_list = [str(hg) for hg in haplogroup_list]
    #Find best matching haplogroup to users haplotype from the haplogroup_list
    matches = [hg for hg in haplogroup_list if haplotype.startswith(hg)]
    
    return max(matches, key=len) if matches else None

# Function that matches the users haplogroup with a haplogroup for VIP's
def match_VIP(matched_haplogroup, VIP_haplogroups_list):
    matches = [hg for hg in VIP_haplogroups_list if matched_haplogroup.startswith(hg)]
    
    return max(matches, key=len) if matches else None
    
AADR_df = load_AADR_data()

# Rename one of the very long column names
AADR_df = AADR_df.rename(columns={"Date mean in BP in years before 1950 CE [OxCal mu for a direct radiocarbon date, and average of range for a contextual date]": "Years before 1950", })

# Some rows does not have any mtDNA haplogroup information, these rows will 
# say "n/a". Here the rows without haplgroup information are removed.
# The code says "if the column contains n/a", but the ~before AADR is an
# invert operatior for boolean. So the output is everything that does not
# match the pattern ("n/a")

filtered_AADR_df = AADR_df[~AADR_df["mtDNA haplogroup if >2x or published"].str.contains("n/a", na=False)]

# Rename column since it no longer contains n/a values
filtered_AADR_df = filtered_AADR_df.rename(columns={"mtDNA haplogroup if >2x or published" : "Haplogroup"})

# Create list with only the haplotypes, from the AADR filtered dataframe
haplogroup_list=filtered_AADR_df["Haplogroup"]

# Ask user to input their hapotype and save it in the hapotype variable
haplotype = st.text_input("""Enter your haplotype, for example like "D4b1a2a"
                  \nDO NOT enter entire files like no fasta, csv, json etc
                  \nDO NOT enter only mutations, for example H1a1 T16093C G16213A.
                  \nPlease enter your haplotype here: """)



if haplotype:
    # Calls the function that matches users input with a haplogroup
    matched_haplogroup = match_haplogroup(haplotype, haplogroup_list)
    
    VIP_df = load_VIP_file()
    VIP_haplogroups_list = VIP_df["mtDNA"]
    matched_VIP_group = match_VIP(matched_haplogroup, VIP_haplogroups_list)
    
    
    #Fixing the output to print
    
    # Get the rows that match to the haplogroup 
    matching_rows = filtered_AADR_df[filtered_AADR_df["Haplogroup"] == matched_haplogroup]
    # If there is more than one haplogroup match, get the oldest one
    oldest_match = matching_rows.nlargest(1,"Years before 1950")
    # Plus 75 since the age is years before 1950, and its 2025 now
    age_of_match = oldest_match["Years before 1950"].iloc[0]
    age_of_match = int(age_of_match) + 75
    
    # VIP print
    VIP = VIP_df[VIP_df["mtDNA"] == matched_VIP_group]
    #Reset the index column to remove row numbers, to not display when printing
    #VIP = VIP.reset_index(drop=True)
    
    
    
    # Write to the output using streamlit
    st.write("Your haplotype is", haplotype)
    st.write("You have matched with the haplogroup ", matched_haplogroup)
    st.write("Your haplogroup is from ", age_of_match, 
             " years ago, and originated from", oldest_match["Political Entity"].iloc[0])
    st.write("Your haplogroup matches with the following VIP's:")
    st.dataframe(VIP, column_order =("mtDNA","Individual","Category"), hide_index=True)
