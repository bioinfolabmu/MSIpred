# MSIpred

A python 2 package computes 22 important somatic mutation features from tumor MAF (mutation annotation format) data. Subsequently, these 22 features are used to predict binary tumor microsatellite instability (MSI) status using a support vector machine (SVM) classifier.

## Getting Started

These instructions will help you install MSIpred on your machine, and to build a bioinformatics pipeline for tumor MSI status prediction from tumor MAF files.

### Prerequisites
python 2 >=  2.7
pandas >= 0.20.3
intervaltree >=2.1.0
sklearn >=  0.19.1

### Installation
Linux & OS X

Download source code and move to the directory of downloaded source code, then simply run

```sh
python setup.py install
```
## Examples
### Example Data
A toy MAF data containing somatic mutation annotations of three colon tumors (COAD)  named as toy.maf, and an reference file of exome annotating loci of simple repeats for GRCh38 (Genome Reference Consortium Human Reference 38) obtained from UCSC genome annotation database at [http://hgdownload.cse.ucsc.edu/goldenPath/hg38/database/](http://hgdownload.cse.ucsc.edu/goldenPath/hg38/database/)
### Build a bioinformatics pipeline for tumor MSI prediction
* Initialization of a MAF file object using a tumor MAF file

``` python
>>> import MSIpred as mp
>>> toy_maf = mp.Raw_Maf(maf_path='toy.maf')
```

* Generate an annotated MAF file named as 'tagged_toy.maf' by adding one extra column called “In_repeats”, which indicates whether mutation events happen in simple repeats region, given a 'simpleRepeats.txt' file.
(if the second argument tagged_maf_file is omitted, a pandas dataframe of annotated MAF will be returned)

```python
>>> toy_maf.create_tagged_maf('simpleRepeat.txt',tagged_maf_file = 'tagged_toy.maf')
```

* Initialization of an annotated MAF file object using annotated MAF file ('tagged_toy.maf') generated in last step

```python
>>> tagged_toy_maf = mp.Tagged_Maf('tagged_toy.maf')
```



* Create a feature dataframe used for further MSI prediction given size (Mb) of captured exome sequence from which MAF file is generated.
(for COAD project, exome size is 44Mb)

```python
>>> toy_features = tagged_toy_maf.make_feature_table(exome_size=44)
```

* Predict tumor MSI status (MSS of MSI-H) using a SVM classifier given the feature dataframe obtained in last step. A pandas dataframe containing predicted MSI status for all tumors in the very begining MAF file ('toy.maf') will be obtained.

```python
>>> predicted_MSI = mp.msi_prediction(toy_features)
```

## Authors

**Chen Wang**

## License

This project is licensed under the MIT License, see [LICENSE](LICENSE) for more information.
[https://github.com/wangc29/MSIpred/blob/master/LICENSE](https://github.com/wangc29/MSIpred/blob/master/LICENSE)


