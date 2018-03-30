#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
MSIpre.tagged_maf
~~~~~~~~~~~~~~~~~

This module provides the class 'MSIpre.raw_maf.Raw_Maf'
class for creating feature table used for Microsatellite
Instability classification.
'''

from pandas import read_table
from pandas import concat
from pandas import DataFrame as df
import pandas as pd

def reduce_maf_df(tagged_maf_file):
    '''
    Return a datafame with 15 essential columns of a tagged .maf file.
    '''

    # read maf file through chunks
    chunks=[]
    chunksize=10000
    used_col = ['Hugo_Symbol','Entrez_Gene_Id','Chromosome','Start_Position','End_Position','Strand',
                'Variant_Classification','Variant_Type','Reference_Allele','Tumor_Seq_Allele1',
                'Tumor_Seq_Allele2','Tumor_Sample_Barcode','Matched_Norm_Sample_Barcode',
                'TRANSCRIPT_STRAND','In_repeats'
    ]
    maf_reader = read_table(tagged_maf_file,low_memory = False,comment='#',chunksize=chunksize,usecols = used_col)
    for chunk in maf_reader:
        chunks.append(chunk)
    reduced_maf_df = concat(chunks,axis=0)
    return reduced_maf_df



def count_vt_all(rd_df,exome_size):
    '''
    This function is used to return a feature dataframe that holds features as variant type
    including 'Tumor','SNP','INS','DEL','SNP_R','INS_R','DEL_R'.
    Input: 
            rd_df: a dataframe generated by function reduce_maf_df 
            exome_size:  exome size in Mb
    Output: 
            a dataframe holding features(counts/Mb) belong to three variant types
            and features of the ratio values (counts proportion, in repeatscounts over total) for all tumors|.
    
    '''
    megalist =[]                                                                # a megalist that hold all records
    grouped = rd_df[['Variant_Type','In_repeats']].groupby(rd_df['Tumor_Sample_Barcode'])       # a groupby object: index is tumor barcode, values is a series holding Variant_Type for that group(index) 
    for tumor,group in grouped:
        exon_region = exome_size # this data is from a reference article
        vt_list = [i for i in group['Variant_Type']]
        in_repeats_rows = group[group['In_repeats']==1]
        in_repeats_vt = [i for i in in_repeats_rows['Variant_Type']]
        inner_list = [tumor, vt_list.count('SNP')/float(exon_region), 
                      vt_list.count('INS')/float(exon_region), 
                      vt_list.count('DEL')/float(exon_region),
                      in_repeats_vt.count('SNP')/float(exon_region),
                      in_repeats_vt.count('INS')/float(exon_region),
                      in_repeats_vt.count('DEL')/float(exon_region), 
        ]
        megalist.append(inner_list)
    label = ['Tumor','SNP','INS','DEL','SNP_R','INS_R','DEL_R']
    mega_df = df.from_records(megalist, columns = label)                        # create and return a dataframe of previous created megalist as mega_df
    return mega_df
    


# In[3]:


def count_vc_all(rd_df,exome_size):
    '''
    This function is used to return a feature dataframe that holds features as variant class
    including 
    ['Frame_Shift_Del', 'Frame_Shift_Ins',
    'In_Frame_Del', 'In_Frame_Ins', 'Missense_Mutation', 
    'Nonsense_Mutation', 'Silent', 'Splice_Site', 
    '3\'UTR', '3\'Flank', '5\'UTR', '5\'Flank','Intron'] for each tumor
    
    Input: 
            rd_df: a dataframe generated by function reduce_maf_df 
            exome_size:  exome size in Mb
    Output: 
            a data frame holding features belong to different varaint classes for all tumors
            
    '''
    
    
    megalist=[]
    variant_class=['Frame_Shift_Del', 'Frame_Shift_Ins',
    'In_Frame_Del', 'In_Frame_Ins', 'Missense_Mutation', 
    'Nonsense_Mutation', 'Silent', 'Splice_Site', 
    '3\'UTR', '3\'Flank', '5\'UTR', '5\'Flank','Intron'
    ]
    grouped = rd_df[['Variant_Classification','In_repeats']].groupby(rd_df['Tumor_Sample_Barcode'])
    for tumor,group in grouped:
        exon_region = exome_size
        inner_list=[tumor]
        vc_list = [i for i in group['Variant_Classification']]
        in_repeats_rows = group[group['In_repeats']==1]
        in_repeats_vc = [i for i in in_repeats_rows['Variant_Classification']]
        for item in variant_class:
            counts = vc_list.count(item)/float(exon_region)
            inner_list.append(counts)
            
        megalist.append(inner_list)
        label = ['Tumor']
        label.extend(variant_class)
    mega_df = df.from_records(megalist, columns=label)
    return mega_df





class Tagged_Maf(object):
    """tagged ('In_repeats info labeled') .maf file class"""
    def __init__(self, tagged_maf_path):
    	'''
    	initiate a Tagged_Maf class with a path to your tagged(.maf file with 'In_repeats' info labeled) .maf file
    	'''
        self.tagged_maf_path = tagged_maf_path

    def make_feature_table(self,exome_size):
    
        '''
        This function is used to return a dataframe that contain all features and composite features that
        will be used for further model training
    
        param exome_size: length of captured exome sequence (Mb)
    
        output:
                a dataframe that holds all feature for every tumor
    
        '''
        tagged_maf_file = self.tagged_maf_path
        
        rd_df = reduce_maf_df(tagged_maf_file)
        vt_feature = count_vt_all(rd_df,exome_size)
        vc_feature = count_vc_all(rd_df,exome_size)
        vt_feature['INDEL'] =  vt_feature['INS']+vt_feature['DEL']
        vt_feature['t_mutation'] = vt_feature['SNP']+vt_feature['INDEL'] 
        vt_feature['INDEL_R'] = vt_feature['INS_R']+vt_feature['DEL_R']
        vt_feature['t_mutation_R'] = vt_feature['SNP_R']+vt_feature['INDEL_R']
        vt_feature['SNP_R/SNP']=vt_feature['SNP_R']/vt_feature['SNP']
        vt_feature['INDEL_R/INDEL'] = vt_feature['INDEL_R']/vt_feature['INDEL']
        vt_feature['tm_R/tm']= vt_feature['t_mutation_R']/vt_feature['t_mutation']
    
        vt_feature = vt_feature[['Tumor','SNP','INDEL','SNP_R','INDEL_R',
                                 't_mutation','t_mutation_R','SNP_R/SNP',
                                 'INDEL_R/INDEL','tm_R/tm',
                             
                                ]
                     ]
        merged_feature = pd.merge(vt_feature,vc_feature,how='inner',left_on='Tumor',right_on='Tumor')
        merged_feature.set_index('Tumor',inplace= True)
        return merged_feature