from setuptools import setup, find_packages

setup(
    name='jobusa',          
    version='0.1',               
    packages=find_packages(),
    install_requires=[
        'psycopg2-binary==2.9.3',
        'pandas==1.0.0',
        'requests==2.27.1',
        'dbt==0.21.0',
        'jinja2==2.11.3',
        'python-dotenv==0.20.0',
        'markupsafe==2.0.1',
    ],
    entry_points={
        'console_scripts': [
            'utils = utils:main', 
        ],
    }
)