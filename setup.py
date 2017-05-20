from setuptools import setup

setup(
      name="atenrich",
      version="0.2",
      packages=['atenrich'],
      package_data={'atenrich': ['data/genelists/']},
      install_requires=['Click','numpy','scipy','pandas'],
      scripts=['bin/atenrich'],
)
