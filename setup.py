from setuptools import setup, find_packages

setup(
    name='upc_allergy_checker',
    version='1.1.0',  # Increment version number
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        # No need to include sqlite3 since it's part of the standard library
    ],
    entry_points={
        'console_scripts': [
            'allergy_checker=upc_allergy_checker.main:main',
        ],
    },
)

