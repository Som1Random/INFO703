from connection import DB_connect
import pandas as pd
import re

#import matplotlib.pyplot as plt
#import numpy as np
#import datetime
#import math
#import sys
#import os
#sys.path.append(os.getcwd())

class extract_data():
    def __init__(self):
        self.dataset = ""
        account = 'nick95'
        pwd = 'NickSumpter'
        self.oraDB = DB_connect.DB_connect()
        self.oraDB.setID('infoinst-02.rc.uab.edu', '1521', 'BIODB.RC.UAB.EDU')
        self.oraDB.getConn(account, pwd)
        self.PAG_input = []
        self.PAG_SOURCE_input = []
        self.PAG_TYPE_input = []
        self.PAG_GENE_input = []

    def GET_HUMAN_GENE(self):
        # retrieve the existing PAGs from PAGER3 human
        sql = 'select * from GENE_HUMAN'
        GENE_HUMAN_TABLE = self.oraDB.getValue(sql, self.oraDB.db)
        GENE_HUMAN_TABLE = pd.DataFrame(GENE_HUMAN_TABLE)
        GENE_HUMAN_TABLE.columns = ["TAX_ID", "GENEID", "SYMBOL", "LOCUSTAG", "SYNONYMS", "DBXREFS", "CHROMOSOME", "MAP_LOCATION", "DESCRIPTION", "TYPE_OF_GENE", "SYMBOL_FROM_NOMENCLATURE", "FULL_NAME_FROM_NOMENCLATURE", "NOMENCLATURE_STATUS", "OTHER_DESIGNATIONS", "MODIFICATION_DATE", "FEATURE_TYPE"]
        ### end retrieve GENE table ###
        self.GENE_HUMAN_TABLE = GENE_HUMAN_TABLE
        return(GENE_HUMAN_TABLE)

    def CLEAN_CONTENT(self, context):
        context = re.sub(u'é', 'e', context)
        context = re.sub(u'ö', 'oe', context)
        context = re.sub(u'Å', 'A', context)
        context = re.sub('‐', '-', context)
        context = re.sub(' $', '', context)
        context = re.sub('\n', ' ', context)
        context = re.sub(u'\xa0', ' ', context)
        context = re.sub(u'\u2030', '&quote', context)
        context = re.sub(u'\u2033', '&quote', context)
        context = re.sub(u'\xef', u'', context)
        context = re.sub(u'\xe4', u'', context)

    def SET_ATTRIBUTES(self, **kwargs):
        self.three_letter = kwargs['three_letter'] if 'three_letter' in kwargs.keys() else ''
        self.PAG_SOURCE = kwargs['PAG_SOURCE'] if 'PAG_SOURCE' in kwargs.keys() else ''
        self.PAG_DESCRIPTION = kwargs['PAG_DESCRIPTION'] if 'PAG_DESCRIPTION' in kwargs.keys() else ''
        self.PAG_TYPE = kwargs['PAG_TYPE'] if 'PAG_TYPE' in kwargs.keys() else ''
        self.PAG_NAME_PREFIX = kwargs['PAG_NAME_PREFIX'] if 'PAG_NAME_PREFIX' in kwargs.keys() else ''
        self.PAG_NAME_SUFFIX = kwargs['PAG_NAME_SUFFIX'] if 'PAG_NAME_SUFFIX' in kwargs.keys() else ''
        self.REFERENCE = self.CLEAN_CONTENT(kwargs['REFERENCE']) if 'REFERENCE' in kwargs.keys() else ''
        self.PUBMED_ID = self.CLEAN_CONTENT(kwargs['PUBMED_ID']) if 'PUBMED_ID' in kwargs.keys() else ''
        self.CONTRIBUTOR = self.CLEAN_CONTENT(kwargs['CONTRIBUTOR']) if 'CONTRIBUTOR' in kwargs.keys() else ''
        self.CURATOR = self.CLEAN_CONTENT(kwargs['CURATOR']) if 'CURATOR' in kwargs.keys() else ''
        self.CURATOR_CONTACT = self.CLEAN_CONTENT(kwargs['CURATOR_CONTACT']) if 'CURATOR_CONTACT' in kwargs.keys() else ''
        self.LINK = self.CLEAN_CONTENT(kwargs['LINK']) if 'LINK' in kwargs.keys() else ''
        self.STATUS = kwargs['STATUS'] if 'STATUS' in kwargs.keys() else ''
        self.RECORD_DATE = kwargs['RECORD_DATE'] if 'RECORD_DATE' in kwargs.keys() else ''

    def GET_NEW_ID_NUMBER(self, three_letter):
        sql = 'select max(GS_ID) from DS_GS_ALL where GS_ID like \'' + three_letter + '%\''
        res = self.oraDB.getValue(sql, self.oraDB.db)
        if(res[0][0]):
            new_num = int(res[0][0][-6:]) + 1
        else:
            new_num = 1
        return(new_num)

    def GENERATE_PAG_SIGNOR(self, **kwargs):
        # input: pd_signor_pathway_map, pd_signor_description_map
        pd_signor_pathway_map = kwargs['pd_signor_pathway_map'] if 'pd_signor_pathway_map' in kwargs.keys() else ''
        pd_signor_description_map = kwargs['pd_signor_description_map'] if 'pd_signor_description_map' in kwargs.keys() else ''
        
        PAG_GENE_pd_input = pd.DataFrame()
        new_num = self.GET_NEW_ID_NUMBER(self.three_letter)
        
        for signor_idx in range(0, pd_signor_description_map.shape[0]):
            signor_row = pd_signor_description_map.iloc[signor_idx,]
            PAG_ID = self.three_letter + ''.join([str(0)] * (6 - len(str(new_num)))) + str(new_num)
            pag_gene_pd = pd_signor_pathway_map[pd_signor_pathway_map['pathway_id'].isin([signor_row['pathway_id']])][['GENEID','SYMBOL']]
            
            #print(pag_gene_pd)
            pag_gene_pd['PAG_ID'] = PAG_ID
            pag_gene_pd = pag_gene_pd[['PAG_ID', 'GENEID', 'SYMBOL']]
            PAG_GENE_pd_input = PAG_GENE_pd_input.append(pag_gene_pd)
            PAG_NAME = signor_row['path_name']
            PAG_SIZE = pag_gene_pd.shape[0]
            PAG_ORGANISM = 'Homo sapiens'
            PAG_DESCRIPTION = signor_row['path_description']
            PAG_LINK = signor_row['LINK']
            PAG_REFERENCE = ""
            PAG_PUBMED_ID = ''
            PAG_CATEGORY = ""  # only for MsigDB catergories
            PAG_CONTRIBUTOR = ''
            PAG_FLAG = ''
            PAG_COCO_V2 = 0
            PAG_GO_FLAG = ''
            PAG_VERSION = 3.0
            PAG_REF_OLD_ID = ''  # linkage to the old database v2
            # linage to the original data source
            PAG_ORIGINAL_ID = signor_row['pathway_id']
            self.PAG_input.append(
                (
                    PAG_ID, PAG_NAME, PAG_SIZE, PAG_ORGANISM, PAG_DESCRIPTION, PAG_LINK,
                    PAG_REFERENCE, PAG_PUBMED_ID, PAG_CATEGORY, self.STATUS,
                    self.CURATOR, self.CURATOR_CONTACT, PAG_CONTRIBUTOR,
                    PAG_FLAG, PAG_COCO_V2, PAG_GO_FLAG, PAG_VERSION,
                    PAG_REF_OLD_ID, PAG_ORIGINAL_ID, self.RECORD_DATE
                )
            )
            self.PAG_SOURCE_input.append((PAG_ID, self.PAG_SOURCE))
            self.PAG_TYPE_input.append((PAG_ID, self.PAG_TYPE))
            new_num += 1
        
        self.PAG_GENE_input = PAG_GENE_pd_input.to_records(index = False).tolist()

    def check_data(self, num):
        print(self.PAG_input[num])
        print(self.PAG_GENE_input[num])
        print(self.PAG_SOURCE_input[num])
        print(self.PAG_TYPE_input[num])
    
    def insert_records(self, table_name, params, values, db):
        # construct an insert statement that add a new row to the table
        sql = ('insert into ' + table_name + '(' + ','.join(params) + ') values(:' + ',:'.join(params) + ')')
        # create a cursor
        cursor = db.cursor()
        # execute the insert statement
        cursor.executemany(sql, values)
        # commit work
        db.commit()

    def insert_data(self):
        PAG_source_map_name = 'DS_GS_ALL_SOURCE'
        PAG_source_map_params = ['GS_ID', 'SOURCE']
        self.insert_records(PAG_source_map_name, PAG_source_map_params, self.PAG_SOURCE_input, self.oraDB.db)

        PAG_table_name = 'DS_GS_ALL'
        PAG_table_params = ['GS_ID', 'NAME', 'GS_SIZE', 'ORGANISM', 'DESCRIPTION', 'LINK', 'REFERENCE', 'PUBMED_ID', 'CATEGORY', 'STATUS', 'CURATOR', 'CURATOR_CONTACT', 'CONTRIBUTED_BY', 'FLAG', 'COCO_V2', 'GO_FLAG', 'VERSION', 'REF_OLD_ID', 'ORIGINAL_ID', 'RECORD_DATE']
        self.insert_records(PAG_table_name, PAG_table_params, self.PAG_input, self.oraDB.db)

        PAG_type_map_name = 'DS_GS_ALL_TYPE'
        PAG_type_map_params = ['GS_ID', 'TYPE']
        self.insert_records(PAG_type_map_name, PAG_type_map_params, self.PAG_TYPE_input, self.oraDB.db)

        PAG_gene_map_name = 'DS_GS_ALL_GENE'
        PAG_gene_map_params = ['GS_ID', 'GENE_ID', 'GENE_SYM']
        self.insert_records(PAG_gene_map_name, PAG_gene_map_params, self.PAG_GENE_input, self.oraDB.db) 

    
