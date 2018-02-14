#!/usr/bin/env python2
# -*- coding: utf-8 -*-


'''
MSIpre.raw_maf
~~~~~~~~~~~~~~

This module provides the class: 'MSIpre.raw_maf.Raw_Maf'
class for adding 'In_repeats' info to each annotation term
of a .maf(mutation annotation format) file.
'''

from intervaltree import Interval, IntervalTree
import pandas as pd


def create_repeats_tree(chromosome,ref_repeats_df):
	'''
	Return interval_tree from ref_repeats dataframe of selected chromosome

	'''
	target_ref_repeats = ref_repeats_df[ref_repeats_df['chrom']==chromosome]
	interval_tuples = target_ref_repeats.apply(lambda row: (row['chromStart'],row['chromEnd']+1),axis=1)
	target_interval_tree = IntervalTree.from_tuples(interval_tuples)
	return target_interval_tree
    
def tag_maf_row(maf_row,repeats_tree):
	'''
	Return a series (a row of mutation annotation format (maf)) tagged with 'In_repeats' info
	'''
	query_tuple = (maf_row['Start_Position'],maf_row['End_Position']+1)
	if len(repeats_tree[query_tuple[0]:query_tuple[1]])>=1:
		maf_row['In_repeats'] = 1
		return maf_row
	elif len(repeats_tree[query_tuple[0]:query_tuple[1]])==0:
		maf_row['In_repeats'] = 0
		return maf_row
def tag_maf_table (maf_file_df,ref_repeats_df):

	'''
	Return a dataframe of a maf file tagged with 'In_repeats' info at the end of each row

	'''
	tagged_group_frame = []
	grouped_maf_file = maf_file_df.groupby('Chromosome')
	for name,group_df in grouped_maf_file:
		ref_repeats_tree = create_repeats_tree(chromosome=name,ref_repeats_df=ref_repeats_df)
		tagged_group_df = group_df.apply(lambda row: tag_maf_row(row,ref_repeats_tree),axis =1)
		tagged_group_frame.append(tagged_group_df)
	return pd.concat(tagged_group_frame,ignore_index=True,axis=0)


class Raw_Maf(object):
	""".maf (mutation annotation format) file class"""
	def __init__(self, maf_path):
		'''
		initiate a Raw_Maf class with a path to your .maf file 

		'''
		self.maf_path = maf_path

	def create_tagged_maf(self,ref_repeats_file,**tagged_maf_file):
		'''
		Add a column to a .maf file with 'In_repeats' info. In_repeats = 1 denotes that 
		this muation annotation term belongs to a simple repeats region, vice versa.

		param ref_repeats_file : path of reference simpleRepeats text file.
		param tagged_maf_file : if not given, a pandas dataframe of a 'In_repeats' info tagged .maf file
		will be returned. If given as: tagged_maf_file = 'your specified output path of tagged_maf file',
		then a tagged .maf file with the given name will be created.
		'''



		maf_file = self.maf_path

	
	#File read and DataFrame creation
		column_list =[	"bin","chrom","chromStart","chromEnd","name_tag",
        	    		"period_size","copyNUM","consensusSize","perMatch",
        	       		"perIndel","score","A","C","G","T","entropy","unit_sequence"
		]


		candidate_chrom = [ 'chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8',
        	            	'chr9', 'chr10', 'chr11', 'chr12', 'chr13', 'chr14', 'chr15',
        	            	'chr16', 'chr17', 'chr18', 'chr19', 'chr20', 'chr21', 'chrX',
        	            	'chr22', 'chrY'
		]


		try:
			ref_repeats = pd.read_table(ref_repeats_file,names=column_list)
			ref_repeats = ref_repeats[(ref_repeats['chrom'].isin(candidate_chrom)) & (ref_repeats['period_size'] <= 5)][['chrom','chromStart','chromEnd']]
			# read in maf file by chunks
			chunksize = 10000
			chunks = []
			maf_table_reader = pd.read_table(maf_file,low_memory=False,comment='#',chunksize = chunksize)
			for chunk in maf_table_reader:
				chunks.append(chunk)
			maf_table = pd.concat(chunks,axis=0)
		except IOError:
			print 'Check README for correct usage'
		else:
	#Create tagged('In_repeats' info annotated) maf file dataframe
			annotated_maf= tag_maf_table(maf_table,ref_repeats)
			if not tagged_maf_file:
				return annotated_maf
			else :
				file_path = tagged_maf_file['tagged_maf_file']
				annotated_maf.to_csv(file_path.strip(),sep ='\t',index=False)