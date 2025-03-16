# -*- coding: utf-8 -*-

"""
haplogroup_app.py

Description: This script will open a webpage where the user can input their
haplotype. A haplogroup, from where and when it originates plus VIP with sharing 
this haplogroup will be printed on the webpage as results. 
    
    
User defined functions: 6

load_AADR_data
load_VIP_file
match_haplogroup
match_VIP
output_haplogroup
output_VIP

Non-standard modules: pandas, streamlit

Procedure:
    
Input:
Output:
    
Usage: streamlit run haplogroup.py

Version: 1.00
Date:
Name: Rebecka Antonsson

"""


import streamlit as st
import pandas as pd


# Loads the AADR excel file into a pandas data frame
def load_AADR_data():
    #For the real deal
    AADR_df = pd.read_excel("AADR_Annotations_2025.xlsx", engine="openpyxl", usecols=[8,13,14,15,16,28])
    
    # Rename one of the very long column names plus latidude and longitude
    # so the map function can understand the columns
    AADR_df = AADR_df.rename(columns={"Date mean in BP in years before 1950 CE [OxCal mu for a direct radiocarbon date, and average of range for a contextual date]": "Years before 1950", 
                                      "Lat." : "lat", "Long." : "lon"})

    # Some rows does not have any mtDNA haplogroup information, these rows will 
    # say "n/a". Here the rows without haplgroup information are removed.
    # The code says "if the column contains n/a", but the ~before AADR is an
    # invert operatior for boolean. So the output is everything that does not
    # match the pattern ("n/a")
    filtered_AADR_df = AADR_df[~AADR_df["mtDNA haplogroup if >2x or published"].str.contains("n/a", na=False)]

    # Rename column since it no longer contains n/a values
    filtered_AADR_df = filtered_AADR_df.rename(columns={"mtDNA haplogroup if >2x or published" : "Haplogroup"})
    
    return filtered_AADR_df



# Loads the VIP excel file into a pandas data frame
def load_VIP_file():
    VIP_df = pd.read_excel("VIPHaplogroups.xlsx", sheet_name=0)
    
    # Renaming the columns
    VIP_df = VIP_df.rename(columns={"mtDNA" : "Haplogroup", 
                           "Individual" : "VIP", 
                           "Category" : "Famous for"})
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



# Function that filters out the correct output and writes the output results
# For the AADR haplogroup output
def output_haplogroup(filtered_AADR_df, matched_haplogroup):
    
    #Fixing the output to print
    
    # Get the rows that match to the haplogroup 
    matching_rows = filtered_AADR_df[filtered_AADR_df["Haplogroup"] == matched_haplogroup]
    
    # If there is more than one haplogroup match, get the oldest one
    oldest_match = matching_rows.nlargest(1,"Years before 1950")
    
    # Plus 75 since the age is years before 1950, and its 2025 now
    age_of_match = oldest_match["Years before 1950"].iloc[0]
    age_of_match = int(age_of_match) + 75
    
     
    return oldest_match, age_of_match


# Function that filters out the correct output and writes the output results,
# For the VIP output
def output_VIP(VIP_df, matched_VIP_group):
    
    # Gets all rows from the VIP file that matches with the Haplogroup
    VIP = VIP_df[VIP_df["Haplogroup"] == matched_VIP_group]
    
    return VIP
    


# MAIN script

def main():
    # Start program and print the first information, using streamlit

    st.header("Find your mtDNA haplogroup")
     
    # Ask user to input their hapotype and save it in the hapotype variable
    haplotype = st.text_input("Please enter your haplotype here:")
    st.info("""\nDO NOT enter entire files like no fasta, csv, json etc
    \nDO NOT enter only mutations, for example H1a1 T16093C G16213A.
    \nDO NOT enter your yDNA haplogroup, only mtDNA
    \nEnter your haplotype, for example like "D4b1a2a or "N1b2a" """, icon="ℹ️")
    
    if haplotype:
        
        # Find matching haplogroup
        
        # Call function that loads the AADR excel file, containing haplogroup information
        filtered_AADR_df = load_AADR_data()
        
        # Create list with only the haplotypes, from the AADR filtered dataframe
        haplogroup_list=filtered_AADR_df["Haplogroup"]
        
        # Calls the function that matches users input with a haplogroup
        matched_haplogroup = match_haplogroup(haplotype, haplogroup_list)
        
        # Stops the script and writes error message if the users input does not have a matching haplogroup.
        if not matched_haplogroup:
            st.error("There was no haplogroup match to your haplotype, are you sure you entered it corretly?")
            st.stop()
        
        # Calls function that writes the results for haplogroup matching
        oldest_match, age_of_match = output_haplogroup(filtered_AADR_df, matched_haplogroup)
        
        
        # Find VIP's that share the haplogroup
        
        # Calls function that loads the VIP haplogroup excel file.
        VIP_df = load_VIP_file()
        
        # Create list with only the haplotypes,from the VIP data frame
        VIP_haplogroups_list = VIP_df["Haplogroup"]
        
        # Calls the function that matches the matched haplogroup with a 
        # haplogroup that exits in the VIP excel file
        matched_VIP_group = match_VIP(matched_haplogroup, VIP_haplogroups_list)
        
        # Calls function that writes the results for the VIP matching
        VIP = output_VIP(VIP_df, matched_VIP_group)
        
        # Write the results, using streamlit
        st.header("Your results")
        tab1, tab2 = st.tabs(["Haplogroup","VIP"])
        
        with tab1:
            st.subheader("Haplogroup")
            st.markdown(f"""
            Your haplotype is: {haplotype}\n\n
            This haplotype belongs to the haplogroup:
                <span style="background-color:#3c799c; padding:5px; 
                border-radius:5px;"><b>{matched_haplogroup}</b></span>
            """, unsafe_allow_html=True)
            st.write(
            f"\nThe {matched_haplogroup} haplogroup originates from  {age_of_match} years ago "
            f"in {oldest_match["Political Entity"].iloc[0]},"
            f" see the map below for a more exact location."
            )
            

            # World map showing the coordiates of where the match was found
            st.map(oldest_match, zoom=2, size=100000, color="#1e4e69")
            
        with tab2:
            st.subheader("VIP")
            if VIP.empty:
                st.write("""Oh, It looks like your haplogroup dosen't match to any famous people (in our data base) :/ 
                    \nMaybe you will be the first one? :)""")
            else:
                st.write("Your haplogroup matches with the following VIP's:")
                st.dataframe(VIP, column_order =("Haplogroup","VIP","Famous for"), 
                             hide_index=True)
            
                

if __name__ == "__main__":
    main()