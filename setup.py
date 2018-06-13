from setuptools import setup
setup(
		name='MSIpred',
		version='0.1',
		description='A package to predict microsatellite instability status for tumors from associated mutation annotation files',
		url='https://github.com/bioinfolabmu/MSIpred',
		author='Chen Wang',
		author_email='wangc29@miamioh.edu',
		license='MIT',
		packages=['MSIpred'],
		install_requires=[
			'pandas',
			'intervaltree',
			'sklearn',
		],
		package_data = {'':['best_svm_pipeline.pkl']},
		include_package_data = True,
		zip_safe=False)
