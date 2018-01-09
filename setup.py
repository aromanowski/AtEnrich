from setuptools import setup

setup(
      name="atenrich",
      version="0.2.1",
      packages=['atenrich'],
      package_data={'atenrich': ['data/genelists/','data/genelists/*.genelist']},
      install_requires=['Click','numpy','scipy','pandas'],
      scripts=['bin/atenrich'],
)
