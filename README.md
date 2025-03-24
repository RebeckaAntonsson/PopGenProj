
# README

Haplogroup & VIP application\
Rebecka Antonsson\
Version 1, 2025-03-24

## Brief description
This application will open a webpage where the user can input their haplotype.
It will then present to the user their haplogroup, when and where the group originates from, 
plus a world map visualizing the location of the haplogroups origin. 
It will also display which historically significant people (VIP’s) this haplogroup is shared

# Workflow

#### Installations

If you don’t already have conda, install it using the instructions found here:
https://www.anaconda.com/docs/getting-started/miniconda/install#quickstart-install-instructions 

Make a separate conda environment called PopGenProj, and activate it so that you install the software in this environment. 
Later make sure to run the program in this environment to avoid troubles with dependencies. 
```python
conda create -n PopGenProj
conda activate PopGenProj
```

Install necessary packages:\
python version 3.13.2p313\
pandas version 2.2.3\
openpyxl version 3.1.5\
streamlit version 1.43.2\
Install them like this:
```python
conda install anaconda::python
conda install anaconda::pandas
conda install anaconda::openpyxl
conda install conda-forge::streamlit
```

For a complete list of softwear versions and dependencies, check out the complete_list_softwear_versions in 
the GitHub repository for this application: https://github.com/RebeckaAntonsson/PopGenProj

You can check your own version like this, and compare your installed softwears are the same:
```python
conda export > complete_list_softwear_versions
```


#### Download required data files from this Github page:
AADR_Annotations_2025.xlsx\
VIPHaplogroups.xlsx

#### Download theme from this Github page:
Download the .streamlit folder, containing a file named config.toml

#### Run the app

The haplotype_app.py script will open a webpage where the user can input their haplotype.
A haplogroup, from where and when it originates plus VIP with sharing this haplogroup will be printed on the 
webpage as results.

Run the app from the terminal, using the softwear streamlit and the haplogroup_app.py script.
```python
streamlit run haplogroup_app.py
```


