#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
This module provide a function: 'MSIpred.predict_msi.msi_prediction'.
Function for the prediction of Microsatellite Instability (MSI) status with
features generated from a .maf file. 
'''


from sklearn.externals import joblib
from pandas import DataFrame
import os
def msi_prediction(feature_table,svm_model=None):
	'''
	Input:
	feature_table : a pandas dataframe created by Tagged_Maf.make_feature_table
	svm_model: when not given(svm_model=none), the default model will be used; otherwise the given model will be used
	
	Output:
	a dataframe with MSI status for each tumor.
	'''
	feature_table = feature_table.fillna(0)
	if svm_model==None:
		current_path = os.path.dirname(__file__)
		model_path = os.path.join(current_path,'best_svm_pipeline.pkl')
		best_pipeline = joblib.load(model_path)
	else:
		best_pipeline=svm_model

	predicted_msi =best_pipeline.predict(feature_table)
	predicted_msi = ['MSS' if result == 0 else 'MSI-H' for result in predicted_msi]
	return DataFrame(zip(feature_table.index,predicted_msi),columns=['Tumor','Predicted_MSI_Status'])
