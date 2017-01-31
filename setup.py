from setuptools import setup, find_packages

setup(
      name="AtEnrich",
      version="0.1",
      packages=['atenrich'],
      package_dir={'atenrich': 'atenrich'},
      package_data={'atenrich': ['data/db/GeneListDB.db','data/config/db_config.json']},
)