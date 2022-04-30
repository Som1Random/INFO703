### signor2.0 data extract, transform and load ###
# https://signor.uniroma2.it/APIs.php
import re
import numpy as np
import pandas as pd
import requests


class SIGNOR():
    def __init__(self):
        # Links to API for SIGNOR
        self.SIGNOR_link_pathway = "https://signor.uniroma2.it/getPathwayData.php?relations"
        self.SIGNOR_link_description = "https://signor.uniroma2.it/getPathwayData.php?description"

    def GET_HUMAN_SIGNOR_PATHWAY(self, **kwargs):
        # requests for relations and turning it into dataframe
        response = requests.get(
            self.SIGNOR_link_pathway
        )
        pd_signor_pathway_map = pd.DataFrame(response.text.split("\n"))[0].str.split('\t', expand = True)
        pd_signor_pathway_map = pd_signor_pathway_map.drop(pd_signor_pathway_map.tail(1).index)
        pd_signor_pathway_map.columns = pd_signor_pathway_map.head(1).values[0]
        pd_signor_pathway_map = pd_signor_pathway_map.drop(pd_signor_pathway_map.head(1).index)
        pd_signor_pathway_map = pd_signor_pathway_map.iloc[:, :-1]
        
        # Filtering for human and proteins
        option = ['protein']
        pd_signor_pathway_map = pd_signor_pathway_map[pd_signor_pathway_map['tax_id'] == '9606']
        
        pd_signor_pathway_map1 = pd_signor_pathway_map[pd_signor_pathway_map['typea'].isin(option)]
        pd_signor_pathway_map1 = pd_signor_pathway_map1[['pathway_id', 'entitya']]
        pd_signor_pathway_map1.rename(columns={'entitya': 'SYMBOL'}, inplace = True)
        
        pd_signor_pathway_map2 = pd_signor_pathway_map[pd_signor_pathway_map['typeb'].isin(option)]
        pd_signor_pathway_map2 = pd_signor_pathway_map2[['pathway_id', 'entityb']]
        pd_signor_pathway_map2.rename(columns={'entityb': 'SYMBOL'}, inplace = True)
        
        pd_signor_pathway_map = pd_signor_pathway_map1.append(pd_signor_pathway_map2, ignore_index = True)
        pd_signor_pathway_map.drop_duplicates(inplace = True, ignore_index = True)
        # End up with a table of pathway_id and the protein symbol

        return(pd_signor_pathway_map)

    def GET_SIGNOR_DETAILS(self, **kwargs):
        # requests for relations and turning it into dataframe
        response = requests.get(
            self.SIGNOR_link_pathway
        )
        pd_signor_pathway_map = pd.DataFrame(response.text.split("\n"))[0].str.split('\t', expand = True)
        pd_signor_pathway_map = pd_signor_pathway_map.drop(pd_signor_pathway_map.tail(1).index)
        pd_signor_pathway_map.columns = pd_signor_pathway_map.head(1).values[0]
        pd_signor_pathway_map = pd_signor_pathway_map.drop(pd_signor_pathway_map.head(1).index)
        pd_signor_pathway_map = pd_signor_pathway_map.iloc[:, :-1]
        
        # Filtering for human and proteins
        option = ['protein']
        pd_signor_pathway_map = pd_signor_pathway_map[pd_signor_pathway_map['tax_id'] == '9606']
        
        pd_signor_pathway_map1 = pd_signor_pathway_map[pd_signor_pathway_map['typea'].isin(option)]
        pd_signor_pathway_map1 = pd_signor_pathway_map1[['pathway_id', 'entitya']]
        pd_signor_pathway_map1.rename(columns={'entitya': 'SYMBOL'}, inplace = True)
        
        pd_signor_pathway_map2 = pd_signor_pathway_map[pd_signor_pathway_map['typeb'].isin(option)]
        pd_signor_pathway_map2 = pd_signor_pathway_map2[['pathway_id', 'entityb']]
        pd_signor_pathway_map2.rename(columns={'entityb': 'SYMBOL'}, inplace = True)
        
        pd_signor_pathway_map = pd_signor_pathway_map1.append(pd_signor_pathway_map2, ignore_index = True)
        pd_signor_pathway_map.drop_duplicates(inplace = True, ignore_index = True)
        
        # Requests for pathways and turning it into a dataframe
        description = requests.get(
            self.SIGNOR_link_description
        )
        pd_signor_description_map = pd.DataFrame(description.text.split("\n"))[0].str.split('\t', expand = True)
        pd_signor_description_map = pd_signor_description_map.drop(pd_signor_description_map.tail(1).index)
        pd_signor_description_map.columns = pd_signor_description_map.head(1).values[0]
        pd_signor_description_map = pd_signor_description_map.drop(pd_signor_description_map.head(1).index)
        pd_signor_description_map = pd_signor_description_map.iloc[:, :-1]
        
        # Filtering, changing column names, and creating new columns for entry
        pd_signor_description_map.rename(columns = {'sig_id': 'pathway_id'}, inplace = True)
        pd_signor_description_map = pd_signor_description_map[pd_signor_description_map['pathway_id'].isin(
            pd_signor_pathway_map['pathway_id'])]
        pd_signor_description_map['LINK'] = self.SIGNOR_link_description
        pd_signor_description_map = pd_signor_description_map[[
            'pathway_id', 'path_name', 'path_description', 'LINK']]
        pd_signor_description_map.drop_duplicates(inplace = True, ignore_index = True)

        return(pd_signor_description_map)
