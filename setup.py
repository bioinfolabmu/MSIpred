from setuptools import setup
setup(
		name='MSIpre',
		version='0.1',
		description='A package to predict status of microsatellite instability for tumors from associated mutation annotation files',
		url='',
		author='Chen Wang',
		author_email='wangc29@miamioh.edu',
		license='MIT',
		packages=['MSIpre'],
		install_requires=[
			'pandas',
			'intervaltree',
			'sklearn',
		],
		package_data = {'':['best_svm_pipeline.pkl']},
		include_package_data = True,
		zip_safe=False)