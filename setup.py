from setuptools import setup, find_packages

setup(
    name='upc_allergy_checker',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
    ],
    entry_points={
        'console_scripts': [
            'allergy_checker=upc_allergy_checker.main:main',
        ],
    },
)

