from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from pandas import DataFrame

def svm_training (training_X,training_y):
	'''
	Input:
	training_X: a dataframe of feature matrix created by Tagged_Maf.make_feature_table
	training_Y: a list of corresponding MSI classes for all tumors in training_X dataframe,
	1 denotes MSI-H
	0 denotes MSS	
	'''
	labels = DataFrame(zip(training_X.index,training_y),columns=["Tumor","MSI_class"]).set_index("Tumor")
	best_estimators = []
	best_estimators.append(('normalizer',StandardScaler()))
	best_estimators.append(('classifier',SVC(C=1000,gamma=0.001)))
	best_pipeline = Pipeline(best_estimators)
	best_pipeline.fit(X=training_X,y=labels)
	return best_pipeline