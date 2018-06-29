# MSIpred

A python 2 package computes 22 important somatic mutation features from tumor MAF (mutation annotation format) data. Subsequently, these 22 features are used to predict binary tumor microsatellite instability (MSI) status using a support vector machine (SVM) classifier.

## Getting Started

These instructions will help you install MSIpred on your machine, and build a bioinformatics pipeline for tumor MSI status prediction from tumor MAF files.

### Prerequisites
python 2 >=  2.7
pandas >= 0.20.3
intervaltree >=2.1.0
sklearn >=  0.19.1

### Installation
Linux & OS X

Download source code and move to the directory where downloaded source code is located, then simply run

```sh
python setup.py install
```
## Examples
### Example Data
A toy MAF data containing somatic mutation annotations of three colon tumors (COAD) named as toy.maf, and an reference file named as 'simpleRepeat.txt' annotating loci of simple repeats throughout genome for GRCh38 (Genome Reference Consortium Human Reference 38), which can be obtained from UCSC genome annotation database at [http://hgdownload.cse.ucsc.edu/goldenPath/hg38/database/simpleRepeat.txt.gz](http://hgdownload.cse.ucsc.edu/goldenPath/hg38/database/simpleRepeat.txt.gz)
### Build a bioinformatics pipeline for tumor MSI prediction
* Initialization of a MAF file object using a tumor MAF file

``` python
>>> import MSIpred as mp
>>> toy_maf = mp.Raw_Maf(maf_path='toy.maf')
```

* Generate an annotated MAF file named as 'tagged_toy.maf' for further analysis by adding one extra column called “In_repeats”, which indicates whether mutation events happen in simple repeats region, to the original MAF file given a 'simpleRepeats.txt' file.
(if the second argument tagged_maf_file is omitted, a pandas dataframe of annotated MAF will be returned)

```python
>>> toy_maf.create_tagged_maf(ref_repeats_file='simpleRepeat.txt',tagged_maf_file = 'tagged_toy.maf')
```

* Initialization of an annotated MAF file object using the annotated MAF file ('tagged_toy.maf') generated in last step.

```python
>>> tagged_toy_maf = mp.Tagged_Maf(tagged_maf_path='tagged_toy.maf')
```



* Create a feature dataframe used for further MSI prediction given size (Mb) of captured exome sequence from which MAF file is generated.
(for COAD project, exome size is 44Mb)

```python
>>> toy_features = tagged_toy_maf.make_feature_table(exome_size=44)
```

* Predict tumor MSI status (MSS or MSI-H) using a SVM classifier given the feature dataframe obtained in last step. A pandas dataframe containing predicted MSI status for all tumors in the very begining MAF file ('toy.maf') will be obtained. If not specified (svm_model=None), the default svm model will be used for prediction, otherwise you can specify a different svm model by giving a different svm model object to the svm_model argument

```python
>>> predicted_MSI = mp.msi_prediction(feature_table=toy_features,svm_model=None)
```
* Train a new svm model with new MAF data. MSIpred allows users to train their own svm model using newly obtained tumor MAF data and their corresponding MSI status. To train a new svm classifier, a dataframe containing mutation features of all tumors in new MAF data is required. This dataframe can be obtained from new MAF data according to the bioinformatics pipeline mentioned above. MSI status for these new tumors are also required, and they should be given as a python list where 0 denotes MSS tumors while 1 denotes MSI-H tumors.
```python
>>> new_model=mp.svm_training(training_X=toy_features,training_y=[0,1,1])
```
The returned svm model object, new_model, can then be used for MSI prediction by specifying svm_model argument of mp.msi_prediction function
## Authors

**Chen Wang**

## License

This project is licensed under the MIT License, see [LICENSE](LICENSE) for more information.
[https://github.com/bioinfolabmu/MSIpred/blob/master/LICENSE](https://github.com/bioinfolabmu/MSIpred/blob/master/LICENSE)
